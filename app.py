from flask import Flask, Blueprint, jsonify
from datetime import datetime
import json

# bp = Blueprint('burritos', __name__, template_folder='templates')
preffix = '/api'

app = Flask(__name__)
# app.register_blueprint(bp, url_prefix='/api')

@app.route('/')
def hello():
    return "Server is working!"

from flask import request
@app.route(preffix + '/v1/attack')
def getAttack():
    startTime = datetime.now()
    id = request.args.get('vm_id', default = '*', type = str)
    
    with open('./data/input-0.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
        
    tags = []
    sources = []
    canAttacks = []
    
    for vm in data['vms']:
        if(vm['vm_id'] == id): 
            tags = vm['tags']
            
    for rule in data['fw_rules']:
        for tag in tags:
            if(tag == rule['dest_tag']):
                sources.append(rule['source_tag'])
           
    for vm in data['vms']:
        for source in sources:
            for tag in vm['tags']:
                if(source == tag and vm['vm_id'] != id):
                    canAttacks.append(vm['vm_id'])
                    break
                    
    endTime = datetime.now()
    dt = endTime - startTime
    ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
    
    if 'request_count' not in data:
        data.update({'request_count': 0})
        data.update({'average_request_time' : 0})
    
    avg = (data['request_count'] * data['average_request_time'] + ms) / (data['request_count'] + 1)
    data['request_count'] += 1
    data['average_request_time'] = avg
    
    print(ms)
    print(data)
    
    with open('./data/input-0.json', 'w') as newJsonFile:
        json.dump(data, newJsonFile)
        newJsonFile.close()
      
    print(canAttacks)  
    # return '
    return jsonify(canAttacks)
    
@app.route(preffix + '/v1/stats')
def stats():
    with open('./data/input-0.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
    
    if 'request_count' not in data:
        data.update({'request_count': 0})
        data.update({'average_request_time' : 0})
        
    result = { 
        'vm_count': len(data['vms']),
        'request_count': data['request_count'], 
        'average_request_time': data['average_request_time']
    }
    
    return result
