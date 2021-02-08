# BigSwitch
Prometheus exporter for Big cloud fabric(BCF)

1. Install required packages
   
   pip install prometheus_client requests

2. Replace the username/password and IP of BCF controller in the exporter.py

3. Running the program
    python exporter.py
    
    OR
    
    Create a linux service 
    
 
 4. It will open the port 30081 on the server and export the metrics. Metrics can be seen on url, for example:
        http://localhost:30081/metrics
      
 5. Prometheus scrape config. For example, add the following lines to prometheus.yml file and restart it. 
 
        - job_name: 'BigSwitch'
          scrape_interval: 30s
          static_configs:
            - targets: ['localhost:30081']

