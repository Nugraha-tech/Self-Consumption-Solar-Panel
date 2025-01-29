import numpy as np

def print_analysis(pv, demand , param, E ):
    
    timestep = param['timestep']
    SelfConsumption = np.sum(E['self_consumption']) * timestep * 6
    PV_Load = np.sum(E['inv_load']) * timestep * 6
    TotalFromGrid = np.sum(E['grid_load']) * timestep * 6
    TotalToGrid = np.sum(E['batt_grid']) * timestep * 6 
    TotalLoad = demand.sum() * timestep * 6
    TotalPV = pv.sum() * timestep * 6
    TotalBatteryGeneration  = np.sum(E['batt_load']) * timestep * 6
    TotalBatteryCharge = np.sum(E['inv_batt']) * timestep * 6
    SisaBeban = np.sum(E['res_loadPV']) * timestep * 6
    SisaPV    = np.sum(E['res_pv']) * timestep * 6
    SisaBebanSetelahDariBaterai = np.sum(E['res_loadbatt']) * timestep * 6    
    pengecasanbaterai = np.sum(E['inv_batt']) * timestep * 6
    pengeluaranbaterai = np.sum(E['batt_load']) * timestep * 6
    Inverter2LoadLosses = (TotalPV ) * (1 - param['HybridInverterEfficiency'])
    Inverter2Batt2InverterLosses = pengecasanbaterai * (1 - param['HybridInverterEfficiency']) + pengeluaranbaterai * (1 - param['HybridInverterEfficiency'])
    HybridInveterLosses = Inverter2LoadLosses + Inverter2Batt2InverterLosses
    BatteryLosses = (TotalBatteryCharge) * (1 - param['BatteryEfficiency'])
    SelfConsumptionRate = SelfConsumption / TotalPV * 100
    SelfSufficiencyRate = SelfConsumption / TotalLoad * 100
    AverageDepth = (TotalBatteryGeneration + TotalBatteryCharge + TotalToGrid) / (1780 * 365) #(365 *(param['BatteryCapacity']))
    Lifetime = 365 * AverageDepth 
    Nfullcycles = 4000/Lifetime
   
    print('Total kebutuhan beban pertahun         : {:.10g} kWh'.format(TotalLoad))
    print('Total produksi PV pertahun             : {:.10g} kWh'.format(TotalPV))
    print('Self Consumption                       : {:.9g} kWh'.format(SelfConsumption))
    print('PV ke Beban                            : {:.8g} kWh'.format(PV_Load))
    print('Sisa PV                                : {:.10g} kWh'.format(SisaPV))
    print('Sisa Beban setelah disuplai PV         : {:.9g} kWh'.format(SisaBeban))
    print('jumlah energi dari PV ke baterai       : {:.8g} kWh'.format(TotalBatteryCharge))    
    print('Jumlah energi baterai ke beban         : {:.7g} kWh'.format(TotalBatteryGeneration))      
    print('Sisa Beban setelah disuplai Baterai    : {:.9g} kWh'.format(SisaBebanSetelahDariBaterai))
    print('Total daya impor dari grid pertahun    : {:.9g} kWh'.format(TotalFromGrid)) 
    print('Total daya ekspor ke grid pertahun     : {:.7g} kWh'.format(TotalToGrid))      
    print('Self consumption rate (SCR)            : {:.3g}%'.format(SelfConsumptionRate))
    print('Self sufficiency rate (SSR)            : {:.3g}%'.format(SelfSufficiencyRate))     
    print('Average depth perday                   : {:.3g}'.format(AverageDepth))
    print('Average depth peryear                  : {:.6g}'.format(Lifetime))
    print('LifeCycle                              : {:.6g}Tahun'.format(Nfullcycles))
    print('Total rugi-rugi Hybridinverter         : {:.6g} kWh'.format(HybridInveterLosses))   
    print('Total rugi-rugi baterai                : {:.6g} kWh'.format(BatteryLosses))
    
   
    