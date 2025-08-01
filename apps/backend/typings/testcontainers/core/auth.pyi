"""
This type stub file was generated by pyright.
"""

from typing import Any, Optional

DockerAuthInfo = ...
_AUTH_WARNINGS = ...
def process_docker_auth_config_encoded(auth_config_dict: dict[str, dict[str, dict[str, Any]]]) -> list[DockerAuthInfo]:
    """
    Process the auths config.

    Example:
    {
        "auths": {
            "https://index.docker.io/v1/": {
                "auth": "dXNlcm5hbWU6cGFzc3dvcmQ="
            }
        }
    }

    Returns a list of DockerAuthInfo objects.
    """
    ...

def process_docker_auth_config_cred_helpers(auth_config_dict: dict[str, Any]) -> None:
    """
    Process the credHelpers config.

    Example:
    {
        "credHelpers": {
            "<aws_account_id>.dkr.ecr.<region>.amazonaws.com": "ecr-login"
        }
    }

    This is not supported yet.
    """
    ...

def process_docker_auth_config_store(auth_config_dict: dict[str, Any]) -> None:
    """
    Process the credsStore config.

    Example:
    {
        "credsStore": "ecr-login"
    }

    This is not supported yet.
    """
    ...

def parse_docker_auth_config(auth_config: str) -> Optional[list[DockerAuthInfo]]:
    """Parse the docker auth config from a string and handle the different formats."""
    ...

