# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:43:32 2020

@author: muril
"""

def model_comp_plot(df_plot,
                    x_nm,
                    y_nm,
                    fv_nm,
                    fn_out,
                    save_fig = True,
                    v_sub    = None,
                    p_sub    = ["#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7"],
                    size_p   = 8,
                    t_fsize  = 20,
                    t_ypos   = 0.93,
                    dpi_fig  = 300):
    
    #-------------------------------------------------------#
    #-------------------- model_comp_plot ------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Plot Simulated (lines) and Observed (markers) data against time
    #--- Parameters: 
    #--- 	df_plot 	: dataframe with simulated and observed data for one or more variables
    #--- 	x_nm    	: Name of df_plot column to use as X axis
    #--- 	y_nm    	: Name of df_plot column to use as Y axis
    #--- 	fv_nm   	: Name of df_plot column to be split in different facets
    #--- 	fn_out  	: Filename of output figure
    #--- 	save_fig	: Save Figure (True/False)
    #--- 	size_p  	: Size of plot
    #--- 	t_fsize 	: Title fontsize
    #--- 	t_ypos  	: Title vertical position
    #--- 	dpi_fig 	: Figure Resolution 
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#    
    
    import matplotlib.pyplot as plt
    
    #--- Get run_id
    try:
        ID = df_plot['run_id'].unique()[0]
    except:
        ID = 'Model Comparison'
    
    #--- Get sim and obs data
    df_obs = df_plot[:][df_plot['type'] == 'obs']
    df_sim = df_plot[:][df_plot['type'] == 'sim']
    
    #--- get unique var and units
    df_uvar = df_plot[[fv_nm,'units']].drop_duplicates() 
    v_nm = df_uvar[fv_nm].unique()  
    
    #--- compute squared grid
    nf = len(v_nm)
    if not nf % 2 == 0: nf += 1
    
    #--- Initilize plot grid
    fig, axs = plt.subplots(int(nf/2), int(nf/2), figsize=(size_p, size_p))   
    
    v = 0
    for r_f in range(0, int(nf/2)):
        for c_f in range(0,int(nf/2)):
            
            #--- get variable
            var = v_nm[v]
            
            #--- get units
            u   = df_uvar['units'][df_uvar[fv_nm] == var].values[0]
            
            #--- plot simulations as lines
            axs[r_f, c_f].plot(df_sim[x_nm][df_sim[fv_nm] == var],
                               df_sim[y_nm][df_sim[fv_nm] == var],
                               c = 'black', 
                               linewidth=1)
            
            #--- plot observations as markers
            axs[r_f, c_f].scatter(df_obs[x_nm][df_obs[fv_nm] == var],
                                  df_obs[y_nm][df_obs[fv_nm] == var],
                                  edgecolors='black', 
                                  facecolors='green',
                                  linewidths= 0.5)
            
            #--- Axis
            axs[r_f, c_f].set(xlabel = x_nm, 
                              ylabel = var+' ('+str(u)+')')
            
            v += 1
    
    fig.suptitle(str(ID),fontsize=t_fsize, y=t_ypos)
    
    #--- save results
    if save_fig:
        plt.savefig(fn_out+'.comp_plot.png', dpi = dpi_fig)
    
    #plt.show()
    plt.close()
