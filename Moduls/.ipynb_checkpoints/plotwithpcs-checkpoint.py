import matplotlib.pyplot as plt
import pandas as pd
def plot_dispatch(pv, demand, E1, week=30):
    
    sliced_index     = (pv.index.isocalendar().week==week)
    pv_sliced        = pv[sliced_index]
    demand_sliced    = demand[sliced_index]
    charge_battery   = E1['inv_batt'][sliced_index] 
    batt_grid        = E1['batt_grid'][sliced_index]
    pv_load          = E1['inv_load'][sliced_index]
    res_pv_sliced    = E1['res_pv'][sliced_index]
    grid_load_sliced = E1['grid_load'][sliced_index]
    batt_load_sliced = E1['batt_load'][sliced_index]
    SOC              = E1['SOC'][sliced_index]
    inv_batt         = E1['inv_batt'][sliced_index]
    grid_load        = E1['grid_load'][sliced_index]
    self_consumption = E1['self_consumption'][sliced_index]
      
       
    fig, axes = plt.subplots(nrows=10, ncols=1, sharex=True, figsize=(40, 60), frameon=False,
                             gridspec_kw={'height_ratios': [3, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'hspace': 0.01})

    #fig, ax = plt.subplots(figsize=(17, 4))
    axes[0].fill_between(demand_sliced.index, demand_sliced, color='black', lw=2, hatch= '//' , alpha=.5)
    axes[0].fill_between(pv_load.index, 0, pv_load, color='orange', alpha=.5)
    axes[0].fill_between(res_pv_sliced.index, pv_load, pv_sliced , color='green', alpha=1)
    axes[0].fill_between(charge_battery.index, charge_battery, color='yellow', alpha=.5)
    axes[0].fill_between(batt_load_sliced.index, batt_load_sliced , color='blue',alpha=.5, hatch='//')
    #axes[0].fill_between(grid_load_sliced.index, pv_sliced + batt_load_sliced, grid_load_sliced + pv_sliced + batt_load_sliced, color='grey', alpha=.2)
    axes[0].plot(batt_grid.index, batt_grid, color='gold', ls=":", lw=4)
    axes[0].plot(grid_load_sliced.index, grid_load_sliced, color='red', ls=":", lw=4)
    #axes[0].set_ylim([0, axes[0].get_ylim()[1] ])
    axes[0].set_ylabel('Power (kW)', fontsize=24)

    
    axes[1].fill_between(pv_sliced.index, pv_sliced, color='green', lw=2)
    axes[1].set_ylabel('Produksi PV (kW)', fontsize=24)
    
    axes[2].fill_between(demand_sliced.index, demand_sliced, color='black', lw=2)
    axes[2].set_ylabel('beban(kW)', fontsize=24)
    
    axes[3].fill_between(pv_load.index, 0, pv_load, color='orange', alpha=.5)
    axes[3].set_ylabel('PV ke beban (kW)', fontsize=24)
    
    axes[4].fill_between(charge_battery.index, charge_battery, color='yellow', alpha=.5)
    axes[4].set_ylabel('battery charge (kW)', fontsize=18)
    
    axes[5].fill_between(batt_load_sliced.index, batt_load_sliced, color='blue', alpha=1)
    axes[5].set_ylabel('Battery Consumption (kWh)', fontsize=18)
    
    axes[6].fill_between(SOC.index, 0, SOC, color='indigo', alpha=1)
    axes[6].set_ylabel('State of Charge (kWh)', fontsize=18)    
    
    axes[7].fill_between(batt_grid.index, batt_grid, color='gold', lw=4)
    axes[7].set_ylabel('baterai ke grid (kWh)', fontsize=18) 
    
    axes[8].fill_between(grid_load_sliced.index, grid_load_sliced, color='red', lw=1)
    axes[8].set_ylabel('grid ke beban (kWh)', fontsize=18)
    
    axes[9].fill_between(self_consumption.index, self_consumption, color='purple', ls=":", lw=1)
    axes[9].set_ylabel('self consumption (kWh)', fontsize=18)
    
    axes[0].legend(['Demand', 'PV to Load', 'PV Residual', 'Battery Charge', 'Battery Discharge', 'Battery Grid', 'Grid Load'], fontsize=24)
    axes[1].legend(['PV Production'], fontsize=24)
    axes[2].legend(['Demand'], fontsize=24)
    axes[3].legend(['PV to Load'], fontsize=24)
    axes[4].legend(['Battery Charge'], fontsize=24)
    axes[5].legend(['Battery Discharge'], fontsize=24)
    axes[6].legend(['State of Charge'], fontsize=24)
    axes[7].legend(['Battery to Grid'], fontsize=24)
    axes[8].legend(['Grid to Load'], fontsize=24)
    axes[9].legend(['Self Consumption'], fontsize=24)

    plt.show()
    
    return

def plot_dispatc(pv, demand, E2, week=30):
    sliced_index = (pv.index.isocalendar().week == week)
    pv_sliced = pv[sliced_index]
    demand_sliced = demand[sliced_index]
    pv_load = E2['inv_load_ongrid'][sliced_index]
    pv_grid = E2['inv_grid_ongrid'][sliced_index]
    grid_load = E2['grid_load_ongrid'][sliced_index]
    self_consumption = E2['self_consumption_ongrid'][sliced_index]
    res_load = E2['res_load_ongrid'][sliced_index]

            
    fig, axes = plt.subplots(nrows=7, ncols=1, sharex=True, figsize=(40, 60), frameon=False,
                             gridspec_kw={'height_ratios': [3, 1, 1, 1, 1, 1, 1], 'hspace': 0.01})

    axes[0].fill_between(demand_sliced.index, demand_sliced, color='black', lw=2, hatch = '//' , alpha=.5)
    axes[0].fill_between(pv_load.index, 0, pv_load, color='orange', alpha=.5)
    axes[0].fill_between(pv_sliced.index, pv_load, pv_sliced , color='green', alpha=1)
    axes[0].plot(pv_grid.index, pv_grid, color='gold', ls= ":", lw=4)
    axes[0].plot(grid_load.index, grid_load, color='red', ls= ":", lw=4)
    #axes[0].fill_between(self_consumption.index, self_consumption, color='purple', ls=":", lw=1)
    #axes[0].fill_between(res_load.index, res_load, color='indigo', alpha=1)
    axes[0].set_ylabel('Power (kW)', fontsize=24)

    axes[1].fill_between(pv_sliced.index, pv_sliced, color='green', lw=2)
    axes[1].set_ylabel('Produksi PV (kW)', fontsize=24)

    axes[2].fill_between(demand_sliced.index, demand_sliced, color='black', lw=2)
    axes[2].set_ylabel('beban(kW)', fontsize=24)

    axes[3].fill_between(pv_load.index, 0, pv_load, color='orange', alpha=.5)
    axes[3].set_ylabel('PV ke beban (kW)', fontsize=24)

    axes[4].fill_between(pv_grid.index, pv_grid, color='gold', alpha=1)
    axes[4].set_ylabel('PV ke grid (kW)', fontsize=24)

    axes[5].fill_between(grid_load.index,grid_load, color='red', alpha=1)
    axes[5].set_ylabel('grid ke beban (kW)', fontsize=24)

    axes[6].fill_between(self_consumption.index, self_consumption, color='purple', ls=":", lw=1)
    axes[6].set_ylabel('self consumption (kW)', fontsize=18)

    axes[0].legend(['Demand', 'PV to Load', 'PV Production', 'PV to Grid', 'Grid to Load'], fontsize=24)
    axes[1].legend(['PV Production'], fontsize=24)
    axes[2].legend(['Demand'], fontsize=24)
    axes[3].legend(['PV to Load'], fontsize=24)
    axes[4].legend(['PV to grid'], fontsize=24)
    axes[5].legend(['grid to Load'], fontsize=24)
    axes[6].legend(['Self Consumption'], fontsize=24)
    
    plt.show()
    
    return




