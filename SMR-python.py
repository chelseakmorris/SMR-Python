def run_smr(initial_storage, precip, pet, awc, sat, ksat, ksat_perc, slope, cell_width, soil_depth, b=1, lateral_in=0):
    # Initialize a few things first
    storage=initial_storage
    SW=[] #Soil Water
    L=[]  #Lateral Outflow
    R=[]  #Runoff
    GW=[] #Groundwater Storage
    
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
        # Balance the storage
        storage = storage-runoff-perc+(lateral_in-lateral_out)
        #
        SW.append(storage)
        L.append(lateral_out)
        R.append(runoff)
        GW.append(perc)
        
    model_output={'SoilWater':SW, 'LateralFlow':L, 'Runoff':R, 'Groundwater':GW}
    return model_output