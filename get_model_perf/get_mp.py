# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:14:35 2020

@author: muril
"""



def get_mp(run_id,
           wd,
           meta,
           res,
           obs_type  = 'avg',
           time_idx  = ['year','doy','dap','das','date'],
           merge_idx = ['year','doy','sim_code'],
           save_res  = True):
    
    #-------------------------------------------------------#
    #------------------------ get_mp -----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Merge simulated and observed data and compute model performance
    #--- Parameters: 
    #---    run_id      : Running ID
    #---    wd          : Working Directory
    #---    meta        : Meta information linking observed and simulated data      [dataframe]
    #---    res         : Results from JULES (e.g output from read_JULES_out())     [dictionary]
    #---    obs_type    : Type of observation to be used in the comparison
    #---    time_idx    : Time indexers
    #---    merge_idx   : Indexers used to merge simulated and observed data
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#    

    print('\n!-------------------------!'+
          '\n!--- Model Performance ---!'+
          '\n!-------------------------!\n')
    
    import pandas as pd
    import gen_nml_defs as gn
    from get_model_perf import mperf
    
    #--- Read observations
    obs     = gn.read_obs(run_id,wd)
        
    #--- Filter observations to be compared with JULES
    sim = {}
    for k in obs.keys():
        if type(obs[k]) != type(None):
            
            obs[k] = pd.merge(obs[k], meta, on = 'variable')
            
            if 'valid'      in obs[k].keys(): obs[k] = obs[k][:][obs[k]['valid']    == 1]
            if 'obs_type'   in obs[k].keys(): obs[k] = obs[k][:][obs[k]['obs_type'] == obs_type]
            
            obs[k] = obs[k][:][~obs[k]['JULES_sim_code'].isnull()]
            
            if len(obs[k]) == 0:
                #--- There is observation but is not associated with any jules outputs
                obs[k] = None
                sim    = {**sim, **{k:None}}
                continue
            
            #--- Rename columns
            obs[k] = obs[k].rename(columns = {'JULES_sim_code':'sim_code',
                                              'JULES_unit_fac':'unit_fac'})
    
            #--- List all JULES outputs found
            l_obs_JULES = obs[k]['sim_code'].unique()
                        
            #--- Find variables in simulation results
            ini_res = True
            for v in l_obs_JULES:
                
                lookup_res = True
                for k_r in res.keys():
                    if not '.info' in k_r:                        
                        if v in res[k_r].keys():
                                                                                     
                            #--- found results ---#
                            if lookup_res:
                                
                                print('Variable '+v+' found in simulation output '+k_r)
                                df_res_k = res[k_r][time_idx + [v]]
                                df_res_k = df_res_k.rename(columns = {v:'sim_value'})
                                df_res_k['sim_code'] = v
                                
                                #--- Convert units to the same of observations
                                u_meta = meta[['JULES_sim_code','JULES_unit_fac','units']]
                                u_meta = u_meta[['units','JULES_unit_fac']][u_meta['JULES_sim_code'] == v]
                                len_u  = len(u_meta.drop_duplicates())
                                
                                if len_u == 0:
                                    print('Warning: No conversion factor found in meta file for converting simulated results of "'+v+'" to the same units of observations.\n - A value of 1 will be assumed.')
                                    conv_factor = 1
                                    unit_lab    = None 
                                elif len_u > 1:
                                    print('Warning: More than one conversion factor found in meta file for converting simulated results of "'+v+'" to the same units of observations.\n - Only the first ocurrence will be assumed.')
                                    conv_factor = u_meta['JULES_unit_fac'].values[0]
                                    unit_lab    = u_meta['units'].values[0]
                                else:
                                    conv_factor = u_meta['JULES_unit_fac'].values[0]
                                    unit_lab    = u_meta['units'].values[0]
                                
                                #--- convert units
                                df_res_k['sim_value'] = df_res_k['sim_value'] * conv_factor
                                df_res_k['sim_units'] = unit_lab
                                
                                #--- Stop looking up
                                lookup_res = False
                                
                                if ini_res:
                                    df_res  = df_res_k
                                    ini_res = False
                                else:
                                    df_res = df_res.append(df_res_k)
                            else:
                                print('Warning: Variable '+v+' also found in simulation output '+k_r+', but only the first match will be used.\nPlease check meta information or output profile setup.')
                                    
                if lookup_res:
                    print('Warning: Variable '+v+' not found in any simulation outputs.\nPlease check meta information or output profile setup.')
            
            #--- Append to a dic
            sim    = {**sim, **{k:df_res}}
        else:
            #--- None Observations for this key
            sim    = {**sim, **{k:None}}    
    
    #------------------------------------------------------------------#
    #--- Merge simulated and observed data for performance analysis ---#
    #------------------------------------------------------------------#
    
    sim_obs = {}
    perf    = {}        
    for k in obs.keys():
        if type(obs[k]) != type(None):
            if k in sim.keys():
                            
                #--- Merge simulated and observed data
                sim_obs_df = pd.merge(obs[k],sim[k], how = 'left', on = merge_idx, suffixes=('_obs', '_sim'))
                                                
                #--- Drop any missing value
                sim_obs_df = sim_obs_df[:][~sim_obs_df['sim_value'].isnull()]                
                
                if len(sim_obs_df) == 0:
                    print('Warning: There is observed data for this run but dates do not match.\n - Please check if simulation dates match with observations.')
                    sim_obs = {**sim_obs, **{k:None}}
                    perf    = {**perf   , **{k:None}}
                    continue                    
                                
                #--- List of variables
                l_var = sim_obs_df['variable'].unique()
                
                #--- Calculate model performance for each variable
                init_perf = True
                for v in l_var:
                    
                    #--- Get performance as df
                    perf_v = pd.DataFrame(mperf(sim_obs_df['sim_value'][sim_obs_df['variable'] == v],
                                                sim_obs_df['obs_value'][sim_obs_df['variable'] == v],
                                                v,
                                                False), index=[0])
                    
                    if init_perf:
                        perf_df   = perf_v
                        init_perf = False        
                    else:
                        perf_df = perf_df.append(perf_v)
                
                #--- Add run_id index
                perf_df['run_id'] = run_id
                
                #--- Store all results
                sim_obs = {**sim_obs, **{k:sim_obs_df}}
                perf    = {**perf   , **{k:perf_df}}
                
            else:                
                print('Warning: Simulations outputs does not have '+k+' results.\n - Failed to merge '+k+' simulated and observed data.')
                sim_obs = {**sim_obs, **{k:None}}
                perf    = {**perf   , **{k:None}}
        else:
            sim_obs = {**sim_obs, **{k:None}}
            perf    = {**perf   , **{k:None}}
    
    #--- Check status of performance run
    perf_stat = 1
    for k_s in sim_obs.keys():
        if type(sim_obs[k_s]) != type(None): perf_stat = 0
        
    #--- Gather Results
    results = {str(run_id)+'.obs'     : obs,
               str(run_id)+'.sim'     : sim,
               str(run_id)+'.sim_obs' : sim_obs,
               str(run_id)+'.perf'    : perf,
               str(run_id)+'.status'  : perf_stat}
    
    #--- Save results
    if save_res:
        for k in results.keys():
            if type(results[k]) != type(None) and k != str(run_id)+'.status':
                for k_r in results[k].keys():
                    if type(results[k][k_r]) != type(None):                        
                        results[k][k_r].to_csv(wd+'/jules_run/namelists/output/'+k+'.csv', index = None, header=True)
                
    #--- return
    return(results)
