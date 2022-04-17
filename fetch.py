import requests
from oci.signer import Signer


def fetch_instance(auth: Signer, compartment_id: str, region: str):
    endpoint = f"https://iaas.{region}.oraclecloud.com/20160918/instances/"
    body = {
        "compartmentId": compartment_id
    }
    response = requests.get(endpoint, params=body, auth=auth)
    return response.text
