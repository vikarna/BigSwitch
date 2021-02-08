#BCF Prometheus interface counter  exporter# 
#Vikarna Tathe#
from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import urllib3

class JsonCollector(object):
  def __init__(self):
        pass
  def collect(self):
    
#Replace the username(admin) and password(admin) with your BCF controller login credentials 	
	
	data = { "user" : "admin", "password" : "admin" }
  
#Replace the ip address(1.1.1.1) with your BCF controller vip address

    r = requests.post('https://1.1.1.1:8443/api/v1/auth/login',data=json.dumps(data),verify=False)
    token = json.loads(r.text)['session_cookie']
    headers = { 'Cookie' : 'session_cookie= ' + token }
    response = json.loads(requests.get('https://1.1.1.1:8443/api/v1/data/controller/applications/bcf/info/statistic/interface-counter',verify=False,headers=headers).content.decode('UTF-8'))

#Parse the output and read through it 
    x = range(len(response))
    for i in x:
        
        z = range(len(response[i]['interface']))


        for k in z:

             metric = Metric('rxbyte'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], 'bytes received', 'counter')
             metric.add_sample('rxbyte'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], value=response[i]['interface'][k]['counter']['rx-byte'], labels={'switch': response[i]['switch-name'], 'interface': response[i]['interface'][k]['name']})
             yield metric

             metric = Metric('txbyte'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], 'bytes transmitted', 'counter')
             metric.add_sample('txbyte'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], value=response[i]['interface'][k]['counter']['tx-byte'], labels={'switch': response[i]['switch-name'], 'interface': response[i]['interface'][k]['name']})
             yield metric

             metric = Metric('linkup'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], 'link status', 'counter')
             metric.add_sample('linkup'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], value=response[i]['interface'][k]['counter']['link-up'], labels={'switch': response[i]['switch-name'], 'interface': response[i]['interface'][k]['name']})
             yield metric

             metric = Metric('rxdrop'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], 'drops observed on Received', 'counter')
             metric.add_sample('rxdrop'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], value=response[i]['interface'][k]['counter']['rx-drop'], labels={'switch': response[i]['switch-name'], 'interface': response[i]['interface'][k]['name']})
             yield metric


             metric = Metric('txdrop'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], 'drops observed on transmission', 'counter')
             metric.add_sample('txdrop'+'_'+response[i]['switch-name']+'_'+response[i]['interface'][k]['name'], value=response[i]['interface'][k]['counter']['tx-drop'], labels={'switch': response[i]['switch-name'], 'interface': response[i]['interface'][k]['name']})
             yield metric


if __name__ == '__main__':
  start_http_server(30081)
  REGISTRY.register(JsonCollector())

  while True:
      time.sleep(60)
