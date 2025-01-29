import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_dispatch(pv, demand, E1, day=1):
    # Hitung jumlah data per 24 jam
    data_per_day = 24
    start_index = (day - 1) * data_per_day
    end_index = start_index + data_per_day
    
    # Potong data sesuai dengan indeks
    pv_sliced        = pv[start_index:end_index]
    demand_sliced    = demand[start_index:end_index]
    charge_battery   = E1['inv_batt'][start_index:end_index]
    batt_grid        = E1['batt_grid'][start_index:end_index]
    pv_load          = E1['inv_load'][start_index:end_index]
    res_pv_sliced    = E1['res_pv'][start_index:end_index]
    grid_load_sliced = E1['grid_load'][start_index:end_index]
    batt_load_sliced = E1['batt_load'][start_index:end_index]
    SOC              = E1['SOC'][start_index:end_index]
    inv_batt         = E1['inv_batt'][start_index:end_index]
    grid_load        = E1['grid_load'][start_index:end_index]
    self_consumption = E1['self_consumption'][start_index:end_index]
    
    # Buat array indeks waktu untuk x-axis, dimulai dari pukul 00.00
    time_index = pd.date_range(start='2023-01-02 00:00', periods=data_per_day, freq='60min')
    
    
    # Buat figure dan axes
    fig, axes = plt.subplots(nrows=10, ncols=1, sharex=True, figsize=(40, 60), frameon=False,
                             gridspec_kw={'height_ratios': [3, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'hspace': 0.01})

    # Plot data pada setiap axes
    axes[0].fill_between(time_index, demand_sliced, color='black', lw=2, hatch= '//' , alpha=.5)
    axes[0].fill_between(time_index, 0, pv_load, color='orange', alpha=.5)
    axes[0].fill_between(time_index, pv_load, pv_sliced , color='green', alpha=1)
    axes[0].fill_between(time_index, charge_battery, color='yellow', alpha=.5)
    axes[0].fill_between(time_index, batt_load_sliced, color='blue', alpha=.5, hatch='//')
    #axes[0].fill_between(time_index, pv_sliced + batt_load_sliced, grid_load_sliced + pv_sliced + batt_load_sliced,color='grey', alpha=.2)
    axes[0].plot(time_index, batt_grid, color='gold', ls=":", lw=4)
    axes[0].plot(time_index, grid_load_sliced, color='red', ls=":", lw=4)
    #axes[0].plot(time_index, SOC, color='indigo', ls=":", lw=4)
    #axes[0].set_ylim([0, axes[0].get_ylim()[1]])
    axes[0].set_ylabel('Power (kW)', fontsize=24)

    axes[1].fill_between(time_index, pv_sliced, color='green', lw=2)
    axes[1].set_ylabel('Produksi PV (kW)', fontsize=24)

    axes[2].fill_between(time_index, demand_sliced, color='black', lw=2)
    axes[2].set_ylabel('Beban (kW)', fontsize=24)

    axes[3].fill_between(time_index, 0, pv_load, color='orange', alpha=.5)
    axes[3].set_ylabel('PV ke Beban (kW)', fontsize=24)

    axes[4].fill_between(time_index, charge_battery, color='yellow', alpha=.5)
    axes[4].set_ylabel('Battery Charge (kW)', fontsize=24)

    axes[5].fill_between(time_index, batt_load_sliced, 0, color='blue', alpha=1)
    axes[5].set_ylabel('Battery Consumption (kWh)', fontsize=18)

    axes[6].fill_between(time_index, 0, SOC, color='indigo', alpha=1)
    axes[6].set_ylabel('State of Charge (kWh)', fontsize=18)
    
    axes[7].fill_between(time_index, batt_grid, color='gold', lw=4)
    axes[7].set_ylabel('baterai ke grid (kWh)', fontsize=18) 

    axes[8].fill_between(time_index, grid_load_sliced, color='red', ls=":", lw=1)
    axes[8].set_ylabel('Grid ke Beban (kWh)', fontsize=18)

    axes[9].fill_between(time_index, self_consumption, color='purple', ls=":", lw=1)
    axes[9].set_ylabel('Self Consumption (kWh)', fontsize=18)
    
    # Mengganti sumbu x dengan indeks 24 jam
    axes[-1].set_xticks(time_index[::3])
    axes[-1].set_xticklabels([t.strftime('%H:%M') for t in time_index[::3]], rotation=45, fontsize=25)
    
    axes[0].legend(['Demand', 'PV to Load', 'PV Production', 'battery charge', 'battery discharge', 'battery to grid', 'grid to load'], fontsize=24)
    axes[1].legend(['PV Production'], fontsize=24)
    axes[2].legend(['Demand'], fontsize=24)
    axes[3].legend(['PV to Load'], fontsize=24)
    axes[4].legend(['Battery charge'], fontsize=24)
    axes[5].legend(['Battery discharge'], fontsize=24)
    axes[6].legend(['SOC'], fontsize=24)
    axes[7].legend(['Battery to grid'], fontsize=24)
    axes[8].legend(['Grid to Load'], fontsize=24)
    axes[9].legend(['Self consumption'], fontsize=24)
        
    plt.show()
    
def plot_dispatc(pv, demand, E2, day=1):
    
    # Hitung jumlah data per 24 jam
    data_per_day = 24
    start_index = (day - 1) * data_per_day
    end_index = start_index + data_per_day
    
    
    # potongan data sesuai indeks
    pv_sliced        = pv[start_index:end_index]
    demand_sliced    = demand[start_index:end_index]
    pv_load          = E2['inv_load_ongrid'][start_index:end_index]
    pv_grid          = E2['inv_grid_ongrid'][start_index:end_index]
    grid_load        = E2['grid_load_ongrid'][start_index:end_index]
    self_consumption = E2['self_consumption_ongrid'][start_index:end_index]
    res_load         = E2['res_load_ongrid'][start_index:end_index]
    
    # Buat array indeks waktu untuk x-axis, dimulai dari pukul 00.00
    time_index = pd.date_range(start='2023-01-02 00:00', periods=data_per_day, freq='60min')

    fig, axes = plt.subplots(nrows=7, ncols=1, sharex=True, figsize=(40, 60), frameon=False,
                             gridspec_kw={'height_ratios': [3, 1, 1, 1, 1, 1, 1], 'hspace': 0.01})

    axes[0].fill_between(time_index, demand_sliced, color='black', lw=2, hatch = '//', alpha =.5)
    axes[0].fill_between(time_index, 0, pv_load, color='orange', alpha=.5)
    axes[0].fill_between(time_index, pv_load, pv_sliced , color='green', alpha=1)    
    axes[0].plot(time_index, pv_grid, color='gold', ls= ":", lw=4)
    axes[0].plot(time_index, grid_load, color='red', ls= ":", lw=4)
    #axes[0].fill_between(time_index, self_consumption, color='purple', ls=":", lw=1)
    #axes[0].fill_between(time_index, res_load, color='indigo', alpha=1)
    axes[0].set_ylabel('Power (kW)', fontsize=24)

    axes[1].fill_between(time_index, pv_sliced, color='green', lw=2)
    axes[1].set_ylabel('Produksi PV (kW)', fontsize=24)

    axes[2].fill_between(time_index, demand_sliced, color='black', lw=2)
    axes[2].set_ylabel('beban(kW)', fontsize=24)

    axes[3].fill_between(time_index, 0, pv_load, color='orange', alpha=.5)
    axes[3].set_ylabel('PV ke beban (kW)', fontsize=24)

    axes[4].fill_between(time_index, pv_grid, color='gold', alpha=1)
    axes[4].set_ylabel('PV ke grid (kW)', fontsize=24)

    axes[5].fill_between(time_index, grid_load, color='red', alpha=1)
    axes[5].set_ylabel('grid ke beban (kW)', fontsize=24)

    axes[6].fill_between(time_index, self_consumption, color='purple', ls=":", lw=1)
    axes[6].set_ylabel('self consumption (kW)', fontsize=18)

    # Mengganti sumbu x dengan indeks 24 jam
    axes[-1].set_xticks(time_index[::3])
    axes[-1].set_xticklabels([t.strftime('%H:%M') for t in time_index[::3]], rotation=45, fontsize=25)
    
    axes[0].legend(['Demand', 'PV to Load', 'PV Production','PV to grid', 'grid to load'], fontsize=24)
    axes[1].legend(['PV Production'], fontsize=24)
    axes[2].legend(['Demand'], fontsize=24)
    axes[3].legend(['PV to Load'], fontsize=24)
    axes[4].legend(['PV to Grid'], fontsize=24)
    axes[5].legend(['Grid to Load'], fontsize=24)
    axes[6].legend(['Self Consumption'], fontsize=24)
   
    plt.show()
