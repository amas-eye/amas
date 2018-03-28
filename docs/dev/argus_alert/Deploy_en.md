# Deployment documentation for argus-alert

## python requirement
version >= 3.6.0

## database_dependencies
0. mongodb version >= 3.4.0
1. redis version >= 3.10.0
2. opentsdb version >= 2.3.0

## python runtime
###### we suggest that it is better to run in virtual enviorment that the system python
package taht we suggest to install virtual environment in python  is virtualenvwrapper
find the doc in here https://virtualenvwrapper.readthedocs.io/en/latest/

## deployment 
0. set up argus-alert path to the virtualenv or system  PYTHONPATH

    ```
    ## like this in /etc/profile or ~/.bashrc
    exprot ARGUS_ALERT=<path/to/argus-alert>
    export PYTHONPATH=$PYTHONPATH:$ARGUS_ALERT
    ```
1. install the python package dependencies
    ```
    pip install -r requirements.txt
    ```
2. start the argus-alert program
   in here  we have two way to start 
   1. start individually
   2. start by superviosr

   #### start individually
   Once you set up the PYTHONPATH,you can run this three command in order
   assume you are in argus-alert/argus_alert
   0. nohup python core/inspect/driver.py &
   1. nohup python core/inspect/exector.py &
   0. nohup python core/notice/handler.py &

   #### start by supervisor(which we highly recommended in this way)
   0. install supervisor in python2(nomatter is virtual environment or system environment ,both is ok)
   ```
    pip install supervisor
   ```
   1. change the configuartion in argus-alert/supervisor.conf
    few parts needs to be changed 
    0. change the part [program:*] below diretory into your real argus-alert path(if you use virtual environment to start,
       you also need to change the command part, replace python into the virtualenvpath/bin/python
    )
    1. change the [supervisord] configuration
    this part can see details in http://www.supervisord.org/

   2. start the whole program
      supervisord -c supervisor.conf




