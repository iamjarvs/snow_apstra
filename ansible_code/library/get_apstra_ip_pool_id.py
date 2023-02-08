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
from ansible.module_utils.apstra_utils import get_aos_blueprints
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


def get_ip_pools(aos, ip_pool_name):
    try:
        ip_pool = aos.resources.ipv4_pools.find_by_name(ip_pool_name).pop()
        return ip_pool.id
    except Exception as e:
        logger.error(f'An error occurred while getting the API token: {e}')
        raise e


def main():
    module = AnsibleModule(
        argument_spec={
            "ip_pool_name": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "ip": {"type": "str", "required": True},
            "port": {"type": "int", "required": True},
        }
    )

    # Assign module parameters to variables
    ip_pool_name = module.params["ip_pool_name"]
    username = module.params["username"]
    password = module.params["password"]
    ip = module.params["ip"]
    port = module.params["port"]

    # Call get_aos_api_token() function with username, password, ip and port as arguments to get AosClient object 
    aos_obj = get_aos_api_token(username, password, ip, port)

    # Call get_ip_pools() function with AosClient object and ip pool name as arguments to get ip pool id
    ip_pool_id = get_ip_pools(aos=aos_obj, ip_pool_name=ip_pool_name)

    # Exit the module with blueprint information
    module.exit_json(ip_pool_id=ip_pool_id)

if __name__ == '__main__':
    main()
