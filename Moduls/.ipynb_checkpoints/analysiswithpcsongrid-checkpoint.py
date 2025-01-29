import numpy as np

def print_analysis(pv, demand, param, E):
    
    timestep = param['timestep']
    SelfConsumption = np.sum(E['inv_load_ongrid'])  * timestep * 6
    TotalFromGrid = np.sum(E['grid_load_ongrid']) * timestep * 6
    TotalToGrid = np.sum(E['inv_grid_ongrid']) * timestep * 6
    TotalLoad = demand.sum()  * timestep * 6
    TotalPV = pv.sum()  * timestep * 6
    InverterLosses = (TotalPV ) * (1 - param['InverterEfficiency'])
    SelfConsumptionRate = SelfConsumption / TotalPV * 100
    SelfSufficiencyRate = SelfConsumption / TotalLoad * 100
    

    print ('Total konsumsi pertahun         : {:.8g} kWh'.format(TotalLoad))
    print ('Total produksi pv pertahun      : {:.8g} kWh'.format(TotalPV))
    print ('Self Consumption                : {:.8g} kWh'.format(SelfConsumption))
    print ('Total daya ekspor ke grid       : {:.8g} kWh'.format(TotalToGrid))
    print ('Total daya impor dari grid      : {:.8g} kWh'.format(TotalFromGrid))
    print ('Self consumption rate (SCR)     : {:.8g}%'.format(SelfConsumptionRate))
    print ('Self sufficiency rate (SSR)     : {:.8g}%'.format(SelfSufficiencyRate))
    print ('Total rugi-rugi inverter        : {:.6g} kWh'.format(InverterLosses))