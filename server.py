
#!/usr/bin/env python3
"""
MCP server for NSO by hitakaha@cisco.com
"""

from fastmcp import FastMCP
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import logging

NSO_ADDR = os.getenv("NSO_ADDR", "198.18.133.101")
NSO_PORT = os.getenv("NSO_PORT", "8080")
USERNAME = os.getenv("NSO_USERNAME", "admin")
PASSWORD = os.getenv("NSO_PASSWORD", "admin")
LOG_FILE = os.getenv("NSO_LOG_FILE", "/tmp/nsomcp.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info(f"Executing command '{command}' on device '{device}'")
    
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

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=payload
        )
        response.raise_for_status()
        logger.info(f"Command executed successfully on device '{device}'")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to execute command on device '{device}': {e}")
        raise

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
    logger.info(f"Running config dry-run on device '{device}': {config}")

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

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=payload
        )
        response.raise_for_status()
        logger.info(f"Dry-run completed successfully on device '{device}'")
        return response.json()["runcli:output"]["output"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to run dry-run on device '{device}': {e}")
        raise
    except KeyError as e:
        logger.error(f"Unexpected response format from dry-run on device '{device}': {e}")
        raise

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
    logger.info(f"Running config commit on device '{device}': {config}")

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

    try:
        response = requests.post(
            url,
            headers=headers,
            auth=auth,
            json=payload
        )
        response.raise_for_status()
        logger.info(f"Config commit completed successfully on device '{device}'")
        return response.json()["runcli:output"]["output"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to commit config on device '{device}': {e}")
        raise
    except KeyError as e:
        logger.error(f"Unexpected response format from commit on device '{device}': {e}")
        raise


if __name__ == "__main__":
    mcp.run(transport='stdio')

