"""
This code is a Python script that uses the AnsibleModule to get blueprint information from an AOS server. 
It imports the urllib3, logging, and AnsibleModule modules from the aos.client package. It then disables any warnings from urllib3 and sets up logging. 
The get_aos_api_token() function takes in a username, password, ip address, and port as parameters and returns an AosClient object. 
The get_aos_blueprints() function takes in an AosClient object and a blueprint name as parameters and returns the blueprint information. 
The main() function sets up the AnsibleModule with arguments for blueprint name, username, password, ip address, and port. It then calls the get_aos_api_token() and get_aos_blueprints() functions to retrieve the blueprint information before exiting with a JSON containing the blueprint information. 
"""

import urllib3
import logging
from typing import Dict
from ansible.module_utils.basic import AnsibleModule
from aos.client import AosClient
# Disable urllib3 warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get AosClient object using username, password, ip and port
def get_aos_api_token(username:str, password:str, ip:str, port:str)->AosClient:
    try:
        aos = AosClient(protocol="https", host=ip, port=port)
        aos.auth.login(username, password)
        return aos
    except Exception as e:
        logger.error(f'An error occurred while getting the API token: {e}')
        raise e

def create_virtual_network(aos, blueprint_id, virtual_network_name, routing_zone_name, ipv4_subnet, ipv4_gateway):

    bound_to = list()
    tor_nodes = aos.blueprint.get_all_tor_nodes(blueprint_id)

    for node in tor_nodes:
        bound_to.append({"system_id": node["id"]})

    return aos.blueprint.create_virtual_network(
        bp_id=blueprint_id,
        name=virtual_network_name,
        bound_to=bound_to,
        sz_name=routing_zone_name,
        ipv4_subnet=ipv4_subnet,
        ipv4_gateway=ipv4_gateway,
        tagged_ct=True,
    )

    

def main():
    module = AnsibleModule(
        argument_spec={
            "blueprint_id": {"type": "str", "required": True},
            "virtual_network_name": {"type": "str", "required": True},
            "ipv4_subnet": {"type": "str", "required": False},
            "ipv4_gateway": {"type": "str", "required": False},
            "routing_zone_name": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "ip": {"type": "str", "required": True},
            "port": {"type": "int", "required": True},
        }
    )

    # Assign module parameters to variables
    blueprint_id = module.params["blueprint_id"]
    virtual_network_name = module.params["virtual_network_name"]
    ipv4_subnet = module.params["ipv4_subnet"]
    ipv4_gateway = module.params["ipv4_gateway"]
    routing_zone_name = module.params["routing_zone_name"]
    username = module.params["username"]
    password = module.params["password"]
    ip = module.params["ip"]
    port = module.params["port"]

    # Call get_aos_api_token() function with username, password, ip and port as arguments to get AosClient object 
    aos_obj = get_aos_api_token(username, password, ip, port)

    # Call get_aos_blueprints() function with AosClient object and blueprint name as arguments to get blueprint information 
    virtual_network_information= create_virtual_network(aos=aos_obj, blueprint_id=blueprint_id, virtual_network_name=virtual_network_name, routing_zone_name=routing_zone_name, ipv4_subnet=ipv4_subnet, ipv4_gateway=ipv4_gateway)

    # Exit the module with new routing zone
    module.exit_json(virtual_network_information=virtual_network_information.__dict__)

if __name__ == '__main__':
    main()
