from flask import Flask, jsonify, request
from datetime import datetime
import json

preffix = '/api/v1'

app = Flask(__name__)

@app.route('/')
def hello():
    return "Server is working!"

@app.route(preffix + '/attack')
def aws():
    startTime = datetime.now()
    id = request.args.get('vm_id', default = '*', type = str)
    attacks = []
    
    for i in [0,1,2,3]:
        file = './data/input-%d.json' %(i) 
        flag = False
        
        with open(file, 'r') as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
            
        for vm in data['vms']:
            if(vm['vm_id'] == id): 
                attacks = getAttack(data, id)
                flag = True
                break
        
        if(flag):
            endTime = datetime.now()
            dt = endTime - startTime
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            if 'request_count' not in data:
                data.update({'request_count': 0})
                data.update({'average_request_time' : 0})
            
            avg = (data['request_count'] * data['average_request_time'] + ms) / (data['request_count'] + 1)
            data['request_count'] += 1
            data['average_request_time'] = avg

            with open(file, 'w') as newJsonFile:
                json.dump(data, newJsonFile)
                newJsonFile.close()
            
            break
    
    return jsonify(attacks)

def getAttack(data, id):
    tags = []
    sources = []
    canAttacks = []
    
    for vm in data['vms']:
        if(vm['vm_id'] == id): 
            tags = vm['tags']
       
    for rule in data['fw_rules']:
        if rule['dest_tag'] in tags:
            sources.append(rule['source_tag'])
           
    for vm in data['vms']:
        for source in sources:
            if source in vm['tags'] and vm['vm_id'] != id:
                canAttacks.append(vm['vm_id'])
                break
              
    return canAttacks
    
@app.route(preffix + '/stats')
def stats():
    result = []
    for i in [0,1,2,3]:
        file = './data/input-%d.json' %(i) 
        flag = False
        
        with open(file, 'r') as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
            
        if 'request_count' not in data:
            data.update({'request_count': 0})
            data.update({'average_request_time' : 0})
            
        result.append({ 
            'vm_count': len(data['vms']),
            'request_count': data['request_count'], 
            'average_request_time': data['average_request_time']
        })
    
    return jsonify(result)
