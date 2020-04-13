# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 13:33:47 2020

@author: muril
"""

def get_mp_all(sim_id,
               all_per,
               wd,
               v_f      = 'variable',
               save_res = True):

    print('\n!---------------------------------!'+
          '\n!--- Overall Model Performance ---!'+
          '\n!---------------------------------!\n')
    
    #--- Overall Performance
    l_sim_obs = [all_per[s] for s in all_per.keys() if ".sim_obs" in s]
    
    #--- Bind all sim_obs
    init_all_sim_obs = True
    for so in l_sim_obs:
        
        if init_all_sim_obs:
            all_sim_obs      = so
            init_all_sim_obs = False
        else:
            
            for k_so in so.keys():
                if type(so[k_so]) != type(None):                
                    
                    try:
                        if type(all_sim_obs[k_so]) == type(None):
                            all_sim_obs[k_so] = so[k_so]
                        else:
                            all_sim_obs[k_so] = all_sim_obs[k_so].append(so[k_so])
                    except KeyError:
                        all_sim_obs[k_so] = so[k_so]
    
    from get_model_perf import mperf
    import get_model_perf as mp
    import pandas as pd
    
    init_perf = True
    for k in all_sim_obs.keys():
        if type(all_sim_obs[k]) != type(None):
            
            #--- Sim and Obs data
            sim_obs_df = all_sim_obs[k]
            
            #--- list of variables
            l_var = sim_obs_df[v_f].unique()
            
            for v in l_var:
                
                print('Computing overall performance of '+v)
                
                #--- Units
                u = sim_obs_df['sim_units'][sim_obs_df[v_f] == v].values[0]
                
                #-----------------------------#
                #--- Get performance as df ---#
                #-----------------------------#
                perf_v = pd.DataFrame(mperf(sim_obs_df['sim_value'][sim_obs_df[v_f] == v],
                                            sim_obs_df['obs_value'][sim_obs_df[v_f] == v],
                                            v,
                                            False), index=[0])
                
                #--------------------#
                #--- plot results ---#
                #--------------------#
                mp.scatter_plot(sim     = sim_obs_df['sim_value'][sim_obs_df[v_f] == v],
                                obs     = sim_obs_df['obs_value'][sim_obs_df[v_f] == v],                         
                                fn_out  = wd+'/results/'+sim_id+'.'+str(k)+'.'+str(v),
                                vnam    = v,
                                units   = u,
                                p_index = False,
                                p_idx   = None,
                                save_fig= True,
                                v_sub   = sim_obs_df['run_id'][sim_obs_df[v_f] == v],
                                p_size  = 5)
                
                #--- Bind performance results
                if init_perf:
                    perf_df   = perf_v
                    init_perf = False        
                else:                
                    perf_df   = perf_df.append(perf_v)
            
            #--- Add key ID
            perf_df['key'] = k
    
    if save_res:
        perf_df.to_csv(wd+'/results/'+sim_id+'.model_performance.csv', index = None, header=True)
