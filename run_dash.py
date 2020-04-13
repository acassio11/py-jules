# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#----------------------#
#--- Load libraries ---#
#----------------------#
import os
import gen_nml_defs as gn
import util         as u
from py_jules_run import py_jules_run

#------------------------#
#--- Running Settings ---#
#------------------------#
sim_id      = 'pj_run'
dash_nm     = 'dashboard_db.csv'        # Filename of Dashboard CSV 
meta_nm     = 'meta_var.csv'            # Filename of Meta-info CSV 
calc_perf   = True                      # Flag to Calculate model performance
clean_res   = True                      # Flag to Get clean results
save_res    = True                      # Flag to save results in 'results' folder
save_all    = False                     # Flag to save all simulations files in 'results' folder
res_CSV     = True                      # Flag to save simulation results as CSV files
ftime_idx   = True                      # Flag to compute time indexers in simulation results (e.g. date, year, doy)
verb        = True                      # Flag for verbose
exec_fn     = 'jules.exe'               # JULES ecxecutable filename
    
#----------------------#
#--- Read dashboard ---#
#----------------------#

#--- get run wd
wd   = os.getcwd().replace('\\','/')

#--- Open CSVs
dash = u.df_csv(wd+'/'+dash_nm)
meta = u.df_csv(wd+'/'+meta_nm)

#--- Filter sites flagged to run
dash_run = dash[:][dash['run_jules']]

#--- Initalize results
all_res = {}
all_per = {}

#--- Run for all treatments
for run_id in dash_run['run_id']:
    
    base_nml_fn     = dash_run['sim_base'][dash_run['run_id'] == run_id].values[0]
    driv_id         = dash_run['driv_id'][dash_run['run_id']  == run_id].values[0]
    soil_id         = dash_run['soil_id'][dash_run['run_id']  == run_id].values[0]
    crop_id         = dash_run['crop_id'][dash_run['run_id']  == run_id].values[0]
    crop_nm         = dash_run['crop_nm'][dash_run['run_id']  == run_id].values[0]    
    
    #--------------------#
    #--- Run py-JULES ---#
    #--------------------#
    res = py_jules_run(run_id,
                       base_nml_fn,
                       driv_id,
                       soil_id,
                       crop_id,
                       crop_nm,
                       wd,
                       exec_fn,
                       verb     = verb,
                       res_CSV  = res_CSV,
                       time_idx = ftime_idx,
                       clean_res= clean_res)
        
    #--- Compute performance?
    if calc_perf:        
        import get_model_perf as mp        
        
        #---------------------------------#
        #--- Compute model performance ---#
        #---------------------------------#
        run_perf = mp.get_mp(run_id,
                             wd,
                             meta,
                             res,
                             obs_type  = 'avg',
                             time_idx  = ['year','doy','dap','das','date'],               
                             merge_idx = ['year','doy','sim_code'],
                             save_res  = True)
        
        if run_perf[str(run_id)+'.status'] == 0:
            
            #------------------------#
            #--- Plot performance ---#
            #------------------------#            
            mp.plot_perf(run_id,
                         run_perf,
                         x_nm   = 'dap',        # X-axis
                         fv_nm  = 'label_var',  # Facets
                         fn_out = wd+'/jules_run/namelists/output/'+str(run_id),
                         l_p_idx = ['r2','d','ef','rmse'])
                            
            all_per = {**all_per, **run_perf}
        
        else:
            print('Warning: There is observed data for this run but dates do not match for any of observations.\n --- Please check if simulation dates match with observations ---')
    
    #--- Store all results
    all_res = {**all_res, **res}
    
    #--- save results
    if save_res: gn.save_res(wd, run_id, save_all)

#--- Compute overall performance
if calc_perf:
    mp.get_mp_all(sim_id,
                  all_per,
                  wd,
                  v_f      = 'variable',
                  save_res = True)