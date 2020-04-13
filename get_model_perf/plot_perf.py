# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:27:52 2020

@author: muril
"""

def plot_perf(run_id,
              run_perf,
              x_nm:str,
              fv_nm:str,
              fn_out:str,
              l_p_idx = ['r2','d','ef','rmse']):

    #----------------------------------------------------------#
    #---------------------- plot_perf -------------------------# 
    #----------------------------------------------------------#
    #--- Goal: 
    #---    Plot model performance
    #--- Parameters:     
    #--- 	run_id     	: Running ID code
    #---    run_perf    : Performance results dictionary (e.g. outputs from get_mp())
    #--- 	x_nm    	: Name of df_plot column to use as X axis
    #--- 	fv_nm   	: Name of df_plot column to be split in different facets
    #--- 	fn_out   	: Filename of figure output
    #---    l_p_idx     : list of performance indexes to be ploted
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------#
    
    print('\n!----------------------------!'+
          '\n!--- Plotting Performance ---!'+
          '\n!----------------------------!\n')
    
    import pandas as pd
    import get_model_perf as mp
    
    for key in run_perf[run_id+'.sim'].keys():
        if type(run_perf[run_id+'.sim'][key]) != type(None):
            
            #--- Prepare dataframe for the plot
            df_plot             = run_perf[run_id+'.sim'][key]
            df_plot             = df_plot.reindex()
            df_plot['type']     = 'sim'
            df_plot['run_id']   = run_id    
            df_plot = df_plot.rename(columns = {'sim_value':'value',
                                                'sim_units':'units'})    
            #--- add observations    
            sim_obs = run_perf[run_id+'.sim_obs'][key]
            obs_dfp = run_perf[run_id+'.sim_obs'][key]
            obs_dfp = obs_dfp.rename(columns = {'obs_value':'value',
                                                'sim_units':'units',
                                                'date_sim' : 'date'})
            obs_dfp = obs_dfp.reindex()
            obs_dfp['type']     = 'obs'
            obs_dfp['run_id']   = run_id
            
            #--- append all
            df_plot = df_plot.append(obs_dfp[df_plot.keys()])
            
            #--- Add variable and label names
            add_dt = sim_obs[['sim_code','variable','label_var']].drop_duplicates()
            df_plot = pd.merge(df_plot,add_dt, how = 'left', on = 'sim_code')
            
            #--- Output filename
            fn_out_comp = fn_out+'.'+key
            
            #--- plot values in all
            y_nm = 'value'
            
            #--- Verbose
            print('Plotting Comparison for '+key)
            
            #------------------------#
            #--- Comparison plots ---#
            #------------------------#
            mp.model_comp_plot(df_plot,
                                x_nm,
                                y_nm,
                                fv_nm,
                                fn_out_comp,
                                save_fig = True,
                                size_p   = 8,
                                t_fsize  = 20,
                                t_ypos   = 0.93,
                                dpi_fig  = 300)
            
            #--- Prepare df for scatter plots                        
            sim_obs = run_perf[run_id+'.sim_obs'][key]
            perf    = run_perf[run_id+'.perf'][key]
            
            for key_p in sim_obs['variable'].unique():
                
                sim     = sim_obs['sim_value'][sim_obs['variable'] == key_p]
                obs     = sim_obs['obs_value'][sim_obs['variable'] == key_p]
                perf_k  = perf[:][perf['model'] == key_p]
                p_idx   = perf_k[l_p_idx]
                units   = sim_obs['sim_units'][sim_obs['variable'] == key_p].values[0]
                vnam    = key_p 
                
                fn_out_scat = fn_out+'.'+key+'.'+key_p
                
                #--- Verbose
                print('Plotting Scatter for '+key+': '+key_p)
                
                #---------------------#
                #--- Scatter plots ---#
                #---------------------#
                mp.scatter_plot(sim,
                                 obs,
                                 p_idx   = p_idx,
                                 fn_out  = fn_out_scat,
                                 vnam    = vnam,
                                 units   = units,
                                 p_index = True,
                                 save_fig= True,
                                 p_size  = 5)
