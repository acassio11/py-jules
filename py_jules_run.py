# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 10:36:56 2020

@author: muril
"""

def py_jules_run(run_id,
                 base_nml_fn,
                 driv_id,
                 soil_id,
                 crop_id,
                 crop_nm,
                 wd,
                 exec_fn,
                 verb     = True,
                 res_CSV  = True,
                 time_idx = True,
                 clean_res= True):
    
    #-------------------------------------------------------#
    #------------------- py_jules_run ----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Run py-jules simulation
    #--- Parameters: 
    #---    run_id      : Running ID
    #---    wd          : Working Directory
    #---    base_nml_fn : Base namelist filename
    #---    driv_id     : Drive data ID
    #---    soil_id     : Soil data ID
    #---    crop_id     : Crop parameters ID
    #---    crop_nm     : Crop name (e.g. Maize, Rice, Soybean)
    #---    exec_fn     : Name of the JULES executable file (e.g. jules.exe)
    #---    verb        : Verbose flag
    #---    time_idx    : Compute time indexers for outputs (e.g. date,year,doy...)
    #---    clean_res   : Retrieve clean results. if true all cpft and pft dimensions that are for the target crop will be ruled out
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#    
    
    import gen_nml_defs as gn
    
    #--- Create Running Environment    
    base_nml = gn.gen_jules_run(run_id,
                                base_nml_fn,
                                driv_id,
                                soil_id,
                                crop_id,
                                crop_nm,
                                wd,
                                verb = True)
    
    #--- Run JULES    
    run_status = gn.run_JULES(exec_fn,wd)
    
    #--- Read Outputs (if simulation succeeded)    
    if run_status.returncode == 0:
        res = gn.read_JULES_out(base_nml,
                                run_id,
                                res_CSV,
                                wd,
                                time_idx,
                                clean_res)
        
        return(res)
    else:
        return(None)
    