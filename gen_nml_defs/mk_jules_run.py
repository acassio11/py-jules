# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 09:52:13 2020

@author: muril
"""
 
def mk_jules_run(wd:str):
    
    #--------------------------------------------------------------#
    #------------------------ mk_jules_run ------------------------# 
    #--------------------------------------------------------------#
    #--- Goal: 
    #---    Create/Update a folder for running jules
    #--- Parameters: 
    #---    wd      : Path where the folder will be created/updated
    #--- Author:
    #---    Murilo Vianna (murilodsv@gmail.com)
    #----------------------------------------------------------------# 
    
    import os
    
    #--- Erase old data
    try:
        if os.path.exists(wd+'/'+'jules_run'): os.remove(wd+'/'+'jules_run')
    except:
        import shutil
        shutil.rmtree(wd+'/'+'jules_run')
            
    #--- Create clean folder
    os.mkdir(wd+'/'+'jules_run')
    os.mkdir(wd+'/'+'jules_run/namelists')
    os.mkdir(wd+'/'+'jules_run/namelists/data')
    os.mkdir(wd+'/'+'jules_run/namelists/output')
    