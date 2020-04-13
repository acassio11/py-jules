# py-jules
Wrapper in python3 for running JULES-crop namelists

![framework](https://github.com/Murilodsv/py-jules/blob/master/framework.png)



## Description:
This wrapper uses a collection of CSV files to run JULES-crop namelists and compare with field observations. For doing that, python3 scripts re-creates the JULES-crop namelists, run the model and compare results with observations.

- An example is ready to run for maize crop in file [run_dash.py](https://github.com/Murilodsv/py-jules/blob/master/run_dash.py)

### Detailed Description:
From the example above, simulations are set up by the [dashboard_db.csv](https://github.com/Murilodsv/py-jules/blob/master/dashboard_db.csv) and in [Running Settings](https://github.com/Murilodsv/py-jules/blob/a98ab77a9da17737b23b683ea601cd70c46fbf13/run_dash.py#L16-L29). Each line of [dashboard_db.csv](https://github.com/Murilodsv/py-jules/blob/master/dashboard_db.csv) that has the column value 'run_jules' as 'TRUE' will be selected to run the py-jules framework. The file [dashboard_db.csv](https://github.com/Murilodsv/py-jules/blob/master/dashboard_db.csv) must also provide the indexers names for driving, soil, crop and base data for each simulations, that are located into the folder [sim_db](https://github.com/Murilodsv/py-jules/tree/master/sim_db). Using information provided in both [dashboard_db.csv](https://github.com/Murilodsv/py-jules/blob/master/dashboard_db.csv) and [sim_db](https://github.com/Murilodsv/py-jules/tree/master/sim_db) the script [py_jules_run](https://github.com/Murilodsv/py-jules/blob/master/py_jules_run.py) will:
- Create/update the 'jules_run' folder
- Create namelists and data needed in the 'jules_run'
- Run JULES
- Read netCDF output files
- Convert results in CSV
- Save results in the [results](https://github.com/Murilodsv/py-jules/tree/master/results) folder with the corresponding run_id

The file [meta_var](https://github.com/Murilodsv/py-jules/blob/master/meta_var.csv) links the variable names and units between simulated and observed values. Model performance and plots are also saved into the [results](https://github.com/Murilodsv/py-jules/tree/master/results) folder.
