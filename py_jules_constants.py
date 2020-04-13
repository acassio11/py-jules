# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:58:20 2020

#--------------------------------------------------------------#
#------------------ py_jules_constants ------------------------# 
#--------------------------------------------------------------#
#--- Goal: 
#---    Declare all constants for py_jules simulations
#--- Author:
#---    Murilo Vianna (murilodsv@gmail.com)
#--------------------------------------------------------------#

"""

import pandas as pd

#--- Corresponding Crop ID number for pft arrays
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/jules_surface_types.nml.html#JULES_SURFACE_TYPES::ncpft
id_crop_pft  = pd.DataFrame({'n_id'     : [6,7,8,9],                                       
                             'crop'     : ['Wheat','Soybean','Maize','Rice'],
                             'namelist' : ['jules_pftparm'] * 4})

#--- Corresponding Crop ID number for tile fractions order
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/jules_surface_types.nml.html#JULES_SURFACE_TYPES::ncpft
n_tile_frac  = pd.DataFrame({'n_id'     : [1     ,     2,     3,     4,     5,      6,        7,      8,     9,     10,     11,     12,    13],                                       
                             'crop'     : ['pft1','pft2','pft3','pft4','pft5','Wheat','Soybean','Maize','Rice','pft10','pft11','pft12','pft13']})

#--- Corresponding Crop ID number for crop parameters arrays
#--- Following same order published before ['Wheat','Soybean','Maize','Rice'] Tab 3 of https://doi.org/10.5194/gmd-8-1139-2015
#--- Source: https://jules-lsm.github.io/latest/namelists/crop_params.nml.html
id_crop_par  = pd.DataFrame({'n_id'     : [1,2,3,4],
                             'crop'     : ['Wheat','Soybean','Maize','Rice'],
                             'namelist' : ['jules_cropparm'] * 4})

#--- Crop Codes
crop_codes   = pd.DataFrame({'crop_code': ['WT','SB','MZ','RC'],
                             'crop'     : ['Wheat','Soybean','Maize','Rice']})

#--- Constant formats for jules driving data
fmt_driv_jules = pd.DataFrame({'val'    : [ 'sw_down', 'lw_down',  'precip',       't',    'wind',   'pstar',       'q', 'diff_rad'],
                               'fmt'    : ['{:16.2f}','{:16.2f}','{:12.4e}','{:16.2f}','{:16.2f}','{:16.1f}','{:16.8f}', '{:16.2f}']})
