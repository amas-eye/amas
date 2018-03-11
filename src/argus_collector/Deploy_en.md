# The Deployment of collector and collector manager

notice: in a cluster, a single collector manager is fullfilled our need , but you can set up more than one to in case fail over

# collector manager deployment
0. check your system time is correct 
1. add argus-collector in your PYTHONPATH(no matter is virtual environment or python in system or python you install )
2. use this command to start 
   ``` nohup python app.py --start &  ``` 
    or use supervisor to start 


# colector deployment
0. check your system time is correct 
1. add argus-collector in your PYTHONPATH (no matter is virtual environment or python in system or python you install )
2. configurate the conf/settings.py
   0. OPEN_TSDB_HOST and OPEN_TSDB_PORT 
   1. AGENT_MANAGER_HOSTi and AGENT_MANAGER_PORTi & AGENT_MANAGER_TOTAL (i in here refers to the num of agent,which start from 1)
   2. PUSH_STATUS_FREQUENCY 
   3. LOGFILE (use absolute path ,the Default is in argus-collector/logs/collector.log)
3. the collector run frequecy is based on the folder of /argus_collector/collectors/  in, the sleep folder in argus_collector/collectors have some prepared collector. you can use as your demand.
4. to start the collector use this command
   ``` ./tcollector start``` 

   