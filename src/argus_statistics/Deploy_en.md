# Dashboard Service deployment 

This Services needed to deployed with argus-web project, sharing the the same mongodb host,and cluster opentsdb is needed for it 

python runtime for the project is python3 needed (version>=3.6.0)

## Deployment
1. pip install -r requirement
2. configurate the settings.py 
3. start the program ,there are two way to start the program
   1. use the command 
    ···
    nohup python start_dashboard.py --start &
    ···
   2. start with supervisor
     the detail need to be find in the official website of supervisor 
     
   
