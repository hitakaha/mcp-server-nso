
#!/usr/bin/env python3
"""
MCP server for NSO by hitakaha@cisco.com
"""

from fastmcp import FastMCP
import requests
from requests.auth import HTTPBasicAuth
import json

NSO_ADDR = "198.18.133.101"
NSO_PORT = "8080"
USERNAME = "admin"
PASSWORD = "admin"

mcp = FastMCP(name="NsoServer")

@mcp.tool
def exec_cmd(device, command) -> str:
    """
    execute any commands via live-status/exec/any

    args:
    - device: target device
    - command: command to execute

    return:
    - outputs
    """
    nso_restconf = f"http://{NSO_ADDR}:{NSO_PORT}/restconf"
    headers = {
        'Content-Type':'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }
    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    url = f"{nso_restconf}/operations/tailf-ncs:devices/device={device}/live-status/exec/any"
    cmd = command

    payload = {
        "input":
        {
            'args': cmd
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload
    )


    # return the outputs, currently works for IOS or IOS-XR NEDs
    if "tailf-ned-cisco-ios-xr-stats:output" in response.json():
        ret = response.json()["tailf-ned-cisco-ios-xr-stats:output"]["result"] 
    elif "tailf-ned-cisco-ios-stats:output" in response.json():
        ret = response.json()["tailf-ned-cisco-ios-stats:output"]["result"] 
    else:
        ret = response.json() # return as it is for other NEDs

    return ret

@mcp.tool
def config_dryrun(device, config) -> str:
    """
    method to dry-run CLI through RESTCONF, equivalent to following

    $ curl -u admin:admin http://127.0.0.1:8080/restconf/\
        operations/tailf-ncs:devices/runcli:runcli-dryrun \  << runcli-dryrun
        -H 'Content-Type: application/yang-data+json' \
        -X POST -d '{"input": { "device": "R1", "command":"hostname test"}}'

    args:
    - device: target device
    - command: command to execute

    return:
    - outputs -> str
    """

    nso_restconf = f"http://{NSO_ADDR}:{NSO_PORT}/restconf"
    url = f"{nso_restconf}/operations/tailf-ncs:devices/runcli:runcli-dryrun"

    headers = {
        'Content-Type':'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }

    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    payload = {
        "input":
        {
            "device": device,
            "command": config
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload
    )

    return response.json()["runcli:output"]["output"]

@mcp.tool
def config_commit(device, config) -> str:
    """
    method to commit CLI through RESTCONF, equivalent to following

    $ curl -u admin:admin http://127.0.0.1:8080/restconf/\
        operations/tailf-ncs:devices/runcli:runcli-commit \  << runcli-commit
        -H 'Content-Type: application/yang-data+json' \
        -X POST -d '{"input": { "device": "R1", "command":"hostname test"}}'

    args:
    - device: target device
    - command: command to execute

    return:
    - outputs -> str
    """

    nso_restconf = f"http://{NSO_ADDR}:{NSO_PORT}/restconf"
    url = f"{nso_restconf}/operations/tailf-ncs:devices/runcli:runcli-commit"

    headers = {
        'Content-Type':'application/yang-data+json',
        'Accept': 'application/yang-data+json'
    }

    auth = HTTPBasicAuth(USERNAME, PASSWORD)

    payload = {
        "input":
        {
            "device": device,
            "command": config
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload
    )

    return response.json()["runcli:output"]["output"]


if __name__ == "__main__":
    mcp.run(transport='stdio')

