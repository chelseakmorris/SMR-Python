def run_smr(initial_storage, precip, pet, awc, sat, ksat, ksat_perc, slope, cell_width, soil_depth, base_coeff, b=1, lateral_in=0):
    
    # Initialize a few things first
    storage=initial_storage
    netP=[0]
    SW=[initial_storage] #Soil Water
    L=[0]   #Lateral Outflow
    RO=[0]  #Runoff
    RC=[0]  #Groundwater Recharge
    BF=[0]  #Baseflow Contribution
    GW=[0]  #Groundwater Storage
    SF=[0]  #Streamflow
    
    for t in range(0,len(precip)):
        
        # Add Precipitation
        if precip[t]>pet[t]:
            #Wetting Conditions
            precip_net=precip[t]-pet[t]
            et_net=0
            storage += precip_net
        else:
            #Drying Conditions
            precip_net=0
            et_net=pet[t]-precip[t]
            storage =storage**(-et_net/awc)
        netP.append(precip_net-et_net)
        
        # Calculate Excess and Runoff fractions
        if storage<awc:
            excess=0
            runoff=0
        elif storage>awc and storage<sat:
            excess=storage-awc
            runoff=0
        else:
            excess=sat-awc
            runoff=storage-sat
        
        # Determine effective hydraulic conductivity
        eff_k=ksat*(storage/sat)**(2*b+3)
        
        # Move excess fraction laterally & vertically
        if excess>0:
            lateral_out=min(excess, slope*cell_width*soil_depth*eff_k/(cell_width**2))
            excess-=lateral_out
            if excess>0:
                perc=min(excess, ksat_perc)
            else:
                perc=0
        else:
            lateral_out=0
            perc=0
        
        # Balance the storage. Each list will have the initial conditions at index zero and 
        # the result at the end of each day will appear in index d, where d=day #.
        storage = storage-runoff-perc+(lateral_in-lateral_out)
        
        # We execute the wetting/drying loop in units of depth, but the record of water
        # movement is in terms of volume. Here, it's cm3/d.
        SW.append(storage*cell_width**2)
        L.append(lateral_out*cell_width**2)
        RO.append(runoff*cell_width**2)
        RC.append(perc*cell_width**2)
        
        # Calculate the baseflow delivered to the stream from groundwater. Groundwater from
        # the previous day contributes to today's baseflow.
        BF.append(GW[t]*base_coeff)
        
        # Deliver the runoff, lateral flow, and groundwater to the stream. 
        SF.append(RO[t+1]+L[t+1]+BF[t+1])
        
        #Deliver the groundwater recharge to groundwater storage. Subtract the loss to baseflow.
        GW.append(GW[t]+RC[t+1]-BF[t+1])

        
    model_output={'AtmExchg':netP, 'SoilWater':SW, 'LateralFlow':L, 'Runoff':RO, 'Recharge':RC, 'Baseflow':BF, 'Groundwater':GW, 'Streamflow':SF}
    return model_output