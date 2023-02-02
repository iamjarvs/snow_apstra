import urllib3
from ansible.module_utils.basic import AnsibleModule
from aos.client import AosClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_aos_api_token(username:str, password:str, ip:str, port:str)->str:
    try:
        aos = AosClient(protocol="https", host=ip, port=port)
        aos_token = aos.auth.login(username, password)
        return aos_token.token
    except Exception as e:
        print(f'An error occurred while getting the API token: {e}')
        raise e


def main():
    module = AnsibleModule(
        argument_spec={
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "ip": {"type": "str", "required": True},
            "port": {"type": "int", "required": True},
        }
    )

    username = module.params["username"]
    password = module.params["password"]
    ip = module.params["ip"]
    port = module.params["port"]

    token = get_aos_api_token(username, password, ip, port)
    module.exit_json(token=token)

if __name__ == '__main__':
    main()
