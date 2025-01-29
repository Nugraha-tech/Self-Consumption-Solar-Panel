from __future__ import division
import numpy as np
import pandas as pd

def dispatch_max_sc(pv, demand, param, return_series=False):
   
    batt_size         = param['BatteryCapacity']    
    eff_batt          = param['BatteryEfficiency']
    eff_hyinv         = param['HybridInverterEfficiency']   
    timestep          = param['timestep']
    LimitSOC          = param['LimitSOC']

    nsteps           = len(pv)
    SOC              = np.zeros(nsteps) # energi yang tersisa dari baterai baik ketika penuh maupun ketika digunakan
    inv_load         = np.zeros(nsteps) # produksi energi PV ke beban
    batt_grid        = np.zeros(nsteps) # energi baterai ke grid atau expor listrik    
    inv_batt         = np.zeros(nsteps) # residu PV ke baterai atau pengecasan
    batt_pcs         = np.zeros(nsteps) # energi baterai ke biderectional inverter
    usable_energy    = np.zeros(nsteps) # energi baterai yang dapat digunakan     
    res_batt_pcs     = np.zeros(nsteps) # sisa energi baterai setelah digunakan    
    res_loadPV       = np.zeros(nsteps) # sisa beban setelah di suplai oleh PV
    batt_load        = np.zeros(nsteps) # energi dari baterai ke beban
    res_loadbatt     = np.zeros(nsteps) # sisa beban setelah di suplai oleh beban
    res_pv           = np.zeros(nsteps) # sisa energi PV setelah menyuplai beban
    pv_inv           = np.zeros(nsteps) # energi PV ke inverter    
    grid_load        = np.zeros(nsteps) # suplai grid ke beban atau impor listrik
    self_consumption = np.zeros(nsteps) # konsumsi sendiri
    
    #Daya dari panel surya
    pv_inv = pv # energi PV ke inverter   
    for i in range(1, nsteps):         
        if pv_inv[i] >= demand[i]: #jika PV lebih besar dari beban maka 
        #if pv_inv.loc[pv_inv.index[i]] >= demand.loc[demand.index[i]].Power:
            inv_load[i] = demand[i] * eff_hyinv #daya dari inverter ke beban adalah besar beban itu sendiri
            res_pv[i] = pv_inv[i] - demand[i] #daya residu PV setelah menyuplai daya ke beban
            inv_batt [i] = res_pv[i] * eff_hyinv #daya residu PV ke biderectional inverter            
            res_loadPV[i] = 0 # sisa daya beban setelah di suplai oleh PV
           
        else:# jika sebaliknya
            inv_load[i] = pv_inv[i] * eff_hyinv #daya dari inverter ke beban adalah besar beban itu sendiri            
            res_pv[i] = 0 #daya residu PV setelah menyuplai daya ke beban 
            inv_batt[i] = 0 #daya residu PV ke biderectional inverter           
            res_loadPV[i] = demand[i] - inv_load[i] # sisa daya beban setelah di suplai oleh PV
            
  

    # timestep pertama = Kapasitas maksimal Baterai
    SOC[0] = batt_size # pada timestep pertama, SOC = kapasitas baterainya
    
    
    
    
    
    # (pengecasan baterai)
    for i in range(1, nsteps):        
        if SOC[i-1] >= batt_size and pv_inv[i] < demand[i]:  # Jika Baterai Penuh dan jika daya produksi pv < kebutuhan beban
            inv_batt[i] = 0  # daya dari biderectional inverter ke baterai 0 dikarenakan baterai penuh
        else: # jika baterai tidak penuh maka
            inv_batt[i] = inv_batt[i] * eff_batt # daya dari biderectional inverter ke baterai = daya residu PV ke biderectional inverter
    
    # terdapat 1 kondisi dimana ketika SOC baterai penuh dan produksi pv < kebutuhan beban maka pengecasan ke baterai = 0 dikarenakan baterai sudah penuh dan tidak ada residu dari pv. jika sebaliknya maka pengecasan ke baterai yaitu residu dari PV nya
            
            
            
            
    # (pengeluaran baterai) 
        usable_energy[i] = SOC[i-1] - LimitSOC # merupakan daya baterai yang dapat digunakan atau daya baterai yang melebihi limit SOCnya, parameter ini digunakan agar pengeluaran baterai tidak 100% untuk menjaga lifecycle baterai
        
        if usable_energy[i] >= res_loadPV[i]: # jika daya baterai yang dapat digunakan >= sisa beban setelai disuplai oleh PV  maka
            res_batt_pcs[i] = usable_energy[i] - res_loadPV[i] # sisa baterai setelah digunakan = daya baterai yang dapat digunakan - sisa beban setelai disuplai oleh PV           
        else: # jika daya baterai yang dapat digunakan - sisa beban setelai disuplai oleh PV < 0 maka
            res_batt_pcs[i] = 0 # sisa baterai setelah digunakan 0          
        
        if SOC[i-1] > LimitSOC : # jika SOC > limit SOC maka
            batt_load[i] = usable_energy[i] - res_batt_pcs[i] #baterai ke beban = baterai yang dapat digunakan - sisa baterai setelah digunakan           
        else: # jika SOC < limit SOC maka
            batt_load[i] = 0 # baterai ke beban = 0
        
     # terdapat 2 kondisi dari pengeluaran baterai di atas, 
     # (1) kondisi ini dipakai untuk memastikan sisa energi baterai atau res_batt_pcs yang digunakan untuk menghitung berapa baterai ke beban, jika iya maka ada sisa energi baterai jika tidak maka = 0. 
        
     # (2) untuk memastikan jika ada sisa energi baterai maka SOCnya sudah pasti di atas Limit SOC nya karena res_loadPV lebih <= usable energy sehingga energi baterai ke beban = usable energi - sisa energi baterai, jika tidak ada sisa energi baterai maka SOCnya sudah pasti di bawah limit SOC sehingga sisa baterai ke beban = 0
        
        
        
     # (Energi grid ke beban impor listrik) 
        res_loadbatt[i] = res_loadPV[i] - batt_load[i] # sisa beban setelah disuplai baterai = sisa beban setelah di suplai PV - baterai ke beban
        grid_load[i] = res_loadbatt[i] # grid ke beban = sisa beban setelah di suplai baterai 
     
     # impor listrik atau suplai dari grid ke beban,  dengan cara menghitung sisa beban setelah di suplai oleh baterai (res_loadbatt)


           
            
     # (SOC Baterai dan baterai ke grid     
        if SOC[i-1] + (inv_batt[i] - batt_load[i]) >= batt_size: # jika SOC + (pengecasan baterai - pengeluaran baterai ke beban) >= kapasitas baterai maka           
            SOC[i] = batt_size # SOC = kapasitas baterai
            batt_grid[i] = SOC[i-1] + (inv_batt[i] - batt_load[i]) - SOC[0] # baterai ke grid atau expor daya = SOC waktu sebelumnya + (pengecasan baterai - pengeluaran baterai ke beban) - SOC atau kapasitas baterainya
        else: # jika sebaliknya maka
            SOC[i] = SOC[i-1] + (inv_batt[i] - batt_load[i]) # SOC= SOC waktu sebelumnya + (pengecasan baterai - pengeluaran baterai ke beban)
            batt_grid[i] = 0 # baterai ke grid = 0
            
     # untuk SOC baterai dan energi dari baterai ke grid memiliki kondisi :
     # jika iya maka SOC baterainya = kapasitas baterai, dan baterai ke grid(Batt_grid) = SOC timstep sebelumnya + (pengecasan baterai - pengeluaran baterai ke beban) - SOC timestep saat ini, dikarenakan ada kelebihan daya yang masuk ke baterai yang tidak dikonsumsi oleh beban, jika tidak maka SOC timestep saat ini = SOC waktu sebelumnya + (pengecasan baterai - pengeluaran baterai ke beban), baterai ke grid (batt_grid) = 0 dikarenakan tidak ada kelebihan daya yang masuk ke baterai



            
    # self consumption    
        self_consumption = inv_load + batt_load  # konsumsi sendiri = produksi energi PV ke beban + energi baterai ke beban
        
    # dikarenakan self consumption merupakan energi dari produksi PV yang disuplai ke beban dengan menggunakan baterai maka residu PV akan di simpan ke baterai untuk menuplai beban pada timestep berikutnya.   

    out = {'pv_inv'          : pv_inv,           
           'res_loadPV'      : res_loadPV,
           'res_pv'          : res_pv,           
           'inv_batt'        : inv_batt, 
           'usable_energy'   : usable_energy,           
           'inv_load'        : inv_load,
           'grid_load'       : grid_load,
           'batt_pcs'        : batt_pcs,
           'res_batt_pcs'    : res_batt_pcs,
           'SOC'             : SOC,
           'batt_load'       : batt_load,
           'res_loadbatt'    : res_loadbatt,
           'self_consumption': self_consumption,
           'batt_grid'       : batt_grid}

    if not return_series:
        out_pd = {}
        for k, v in out.items():  # Membuat 'dictionary' dari pandas series (pd.series) dengan index yang sama dengan input Panel Surya
            out_pd[k] = pd.Series(v, index=pv.index)
        out = out_pd
    return out


def dispatch_max_sc_grid_pf(pv, demand, param_tech, return_series=False):
    

    eff_inv      = param_tech['InverterEfficiency']
    timestep     = param_tech['timestep']

    nsteps                    = len(pv)
    pv_inv_ongrid             = np.zeros(nsteps) # produksi PV
    inv_load_ongrid           = np.zeros(nsteps) # produksi energi PV ke beban 
    inv_grid_ongrid           = np.zeros(nsteps) # residu Produksi PV dari inverter ke grid
    res_load_ongrid           = np.zeros(nsteps) # sisa beban setelah di suplai PV
    grid_load_ongrid          = np.zeros(nsteps) # energi dari grid ke beban
    self_consumption_ongrid   = np.zeros(nsteps) # konsumsi sendiri   
    
    #Daya dari panel surya
    pv_inv_ongrid = pv   
    
    
    #Daya ke beban dan ke grid    
    for i in range(1, nsteps):        
        #if pv_inv_ongrid[i] > demand[i]: # jika produksi PV > dari beban maka
        if pv_inv_ongrid[i] >= demand[i]:
            inv_load_ongrid[i] = demand[i] * eff_inv # inverter ke beban(produksi energi PV ke beban) = kebutuhan beban
            inv_grid_ongrid[i] = pv_inv_ongrid[i] - demand[i] # inverter ke grid atau ekspor listrik, dari sisa produksi PV setelah dari beban
        else:
            inv_load_ongrid[i] = pv_inv_ongrid[i] * eff_inv # inverter ke beban(produksi energi PV ke beban)
            inv_grid_ongrid[i] = 0 # inverter ke grid atau ekspor listrik 
     # terdapat kondisi jika produksi PV > kebutuhan beban maka, produksi energi PV ke beban yaitu = kebutuhan beban , ekspor listriknya = produksi energi PV ke beban - kebutuhan beban. Jika sebaliknya maka, produksi energi PV ke beban yaitu = produksi PV, ekspor listriknya = 0 dikarenakan dikarenakan tidak ada sisa produksi PV setelah dari beban
            
            
            
     # (self consumption, sisa kebutuhan beban, energi dari grid ke beban)       
        self_consumption_ongrid = inv_load_ongrid # self consumption merupakan energi dari produksi PV yang disuplai ke beban     
        res_load_ongrid[i] = demand[i] - inv_load_ongrid[i] # sisa kebutuhan beban setelah disuplai oleh PV
        grid_load_ongrid[i] = res_load_ongrid[i] # grid ke beban = sisa beban setelah di suplai baterai 
        
     
    
    out = {'pv_inv_ongrid'          : pv_inv_ongrid,           
           'inv_load_ongrid'        : inv_load_ongrid,
           'inv_grid_ongrid'        : inv_grid_ongrid,
           'res_load_ongrid'        : res_load_ongrid,
           'grid_load_ongrid'       : grid_load_ongrid,
           'self_consumption_ongrid': self_consumption_ongrid     
            }
     
    if not return_series:
        out_pd = {}
        for k, v in out.items():  #Membuat 'dictionary' dari pandas series (pd.series) dengan index yang sama dengan input Panel Surya
            out_pd[k] = pd.Series(v, index = pv.index)
        out = out_pd
    return out
