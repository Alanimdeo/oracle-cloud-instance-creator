import requests
from oci.signer import Signer


def create_instance(auth: Signer, region: str, create_instance_option: dict):
    endpoint = f"https://iaas.{region}.oraclecloud.com/20160918/instances/"
    response = requests.post(endpoint, json=create_instance_option, auth=auth)
    return response.text
