import os
import ovh
import time
import signal
from pprint import pprint
from googleapiclient import discovery


run = True
try:
    import json
    from pygments import highlight
    from pygments.lexers import JsonLexer
    from pygments.formatters import TerminalFormatter
    def pprint_dict(_dict):
        json_str = json.dumps(i, indent=4)
        print(highlight(json_str, JsonLexer(), TerminalFormatter()))
except:
    pass

def signal_handler(signal, frame):
    global run
    print("exiting")
    run = False

def pause():
    for _ in range(0,50):
        # set run as global var
        if not run:
            exit(0)
        time.sleep(0.1)

def list_zones(compute, project):
    zones = compute.zones().list(project=project).execute()
    return zones['items'] if 'items' in zones else None

def list_instances(compute, project):
    _filter = "status eq 'RUNNING'"
    result = compute.instances().aggregatedList(project=project, filter=_filter).execute()
    return result['items'] if 'items' in result else None

signal.signal(signal.SIGTERM, signal_handler)
client = ovh.Client()
zoneName = os.environ['OVH_ZONENAME']
root_url = f'/domain/zone/{zoneName}/dynHost'
# Use an env variable or commandline argument
project = 'refined-bolt-255914'
compute = discovery.build('compute', 'v1')

while run:
    i_result = list_instances(compute, project)
    instances = {}

    # Flatten instances
    for name, inst in i_result.items():
        if 'instances' in inst:
            instances[name] = inst['instances']
    
    for region, inst in instances.items():
        for i in inst:
            ovh_subd = f"{i['name']}.{region.replace('zones/', '')}"
            ovh_ipv4 = i['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            record_id = client.get(f'{root_url}/record',
                subDomain=ovh_subd
            )
            if not record_id:
                result = client.post(f'{root_url}/record',
                    ip=ovh_ipv4,
                    subDomain=ovh_subd
                )
                print(f'Creating record {ovh_subd}.{zoneName} with IPv4 {ovh_ipv4}')
            else:
                result = client.get(f'{root_url}/record/{record_id[0]}')
                if ovh_ipv4 == result['ip']:
                    continue
                result = client.put(f'{root_url}/record/{record_id[0]}',
                    ip=ovh_ipv4,
                    subDomain=ovh_subd
                )
                print(f'Updating record {ovh_subd}.{zoneName} with IPv4 {ovh_ipv4}')
            result = client.post(f'/domain/zone/{zoneName}/refresh')
    pause()
