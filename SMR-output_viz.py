import matplotlib.pyplot as plt
    
def daily_water_plot(model_data, jday):
    ### This function plots and prints the data returned by the SMR model on a daily graph
    ### and in a list form.
    
    #Set up the plot
    plt.figure(figsize=(10,7))
    plt.xlim(jday[0],jday[-1]+1)
    plt.xlabel('day')
    plt.ylabel('volume, cubic centimeters')
            
    #Plot data
    plt.plot(jday, model_data['SoilWater'], 'black', label='Soil water storage')
    plt.plot(jday, model_data['LateralFlow'], 'blue', label='Lateral water export')
    plt.plot(jday, model_data['Runoff'], 'green', label='Overland runoff contribution')
    plt.plot(jday, model_data['Recharge'], 'purple', label='Contribution to groundwater')
    plt.plot(jday, model_data['Baseflow'], 'yellow', label='Groundwater contribution to stream')
    plt.plot(jday, model_data['Groundwater'], 'red', label='Groundwater storage')
    plt.plot(jday, model_data['Streamflow'], 'orange', label='Streamflow')
    
    plt.legend(loc='best')
    
    #Print values in list form
    print "Soil Water, cm3", model_data['SoilWater']
    print "Lateral Water Flow, cm3", model_data['LateralFlow']
    print "Runoff, cm3", model_data['Runoff']
    print "Contribution to Groundwater, cm3", model_data['Recharge']
    print "Groundwater Contribution to Stream, cm3", model_data['Baseflow']
    print "Groundwater Storage, cm3", model_data['Groundwater']
    print "Streamflow, cm3", model_data['Streamflow']
    
def water_balance_check(model_data, jday, initial_storage):
    ### This function checks that water inputs, outputs, and storage balance each day for
    ### the watershed. It'll be most useful when the watershed has more than one cell.
    import numpy  
    
    print "Daily Water Balance Check" 
    for day in range(1, len(jday)):
        atmospheric_exchange = model_data['AtmExchg'][day]
        streamflow_exchange = model_data['LateralFlow'][day]+model_data['Runoff'][day]+model_data['Baseflow'][day]
        storage_change = (model_data['SoilWater'][day]-model_data['SoilWater'][day-1])+(model_data['Groundwater'][day]-model_data['Groundwater'][day-1])
        
        if numpy.round(atmospheric_exchange, 2)-numpy.round(storage_change, 2)-numpy.round(streamflow_exchange, 2)!=0:
            print "Day", day
            print "Net Precipitation:", atmospheric_exchange, "Export to Streamflow:", streamflow_exchange, "Net Storage Change:", storage_change
        else:
            print "Day", day
            print "Okay"