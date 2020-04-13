# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:33:15 2020

@author: muril
"""

def run_JULES(exec_fn :str,
              wd      :str):

    #-------------------------------------------------------#
    #---------------------- run_JULES ----------------------# 
    #-------------------------------------------------------#
    #--- Goal: 
    #---    Run JULES from the shell
    #--- Parameters: 
    #---    exec_fn : JULES Executable (e.g. jules.exe)
    #---    wd      : Working Directory
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #-------------------------------------------------------#

    import shutil
    from subprocess import run
    from time import time
    
    #--- Copy the executable to running folder
    shutil.copy2(wd+'/sim_db/'+exec_fn, wd+'/jules_run/')
    
    #--- Prepare running args
    #--- Note: Setup for Monsoon
    run_args = ['cd '+wd+'/jules_run/namelists/',               # get into run folder
                'chmod +x ../'+exec_fn,                         # allow executable permission
                'module swap PrgEnv-cray PrgEnv-cray/5.2.40',   # swap module for jules
                'module load cray-netcdf-hdf5parallel/4.3.2',   # load module for jules
                'module load cray-snplauncher/7.0.4',           # load module for jules 
                'mpiexec ../'+exec_fn]                          # run jules with mpi
    
    print('\n!---------------------!'+
          '\n!--- Running JULES ---!'+
          '\n!---------------------!\n')
    
    #--- Track progress
    start_time = time()    
    
    #--- Run JULES
    res = run("; ".join(run_args), shell = True)
    
    if res.returncode == 0:    
        print('\n!---------------------------!'+
              '\n!--- Simulation Complete ---!'+
              '\n!---------------------------!\n')
    else:
        print('\n!------------------------!'+
              '\n!--- Simulation Error ---!'+
              '\n!------------------------!\n')
            
    print("Elapsed time: --- %.3f seconds ---" % (time() - start_time))
    
    return(res)
    
    