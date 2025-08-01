"""
This type stub file was generated by pyright.
"""

from os import PathLike
from socket import socket
from types import TracebackType
from typing import Any, Optional, TYPE_CHECKING, TypedDict, Union
from docker.models.containers import Container, ExecResult
from typing_extensions import Self
from testcontainers.core.docker_client import DockerClient
from testcontainers.core.network import Network
from testcontainers.core.waiting_utils import wait_container_is_ready

if TYPE_CHECKING:
    ...
logger = ...
class Mount(TypedDict):
    bind: str
    mode: str
    ...


class DockerContainer:
    """
    Basic container object to spin up Docker instances.

    Args:
        image: The name of the image to start.
        docker_client_kw: Dictionary with arguments that will be passed to the
            docker.DockerClient init.
        command: Optional execution command for the container.
        name: Optional name for the container.
        ports: Ports to be exposed by the container. The port number will be
            automatically assigned on the host, use
            :code:`get_exposed_port(PORT)` method to get the port number on the host.
        volumes: Volumes to mount into the container. Each entry should be a tuple with
            three values: host path, container path and. mode (default 'ro').
        network: Optional network to connect the container to.
        network_aliases: Optional list of aliases for the container in the network.

    .. doctest::

        >>> from testcontainers.core.container import DockerContainer
        >>> from testcontainers.core.waiting_utils import wait_for_logs

        >>> with DockerContainer("hello-world") as container:
        ...    delay = wait_for_logs(container, "Hello from Docker!")
    """
    def __init__(self, image: str, docker_client_kw: Optional[dict[str, Any]] = ..., command: Optional[str] = ..., env: Optional[dict[str, str]] = ..., name: Optional[str] = ..., ports: Optional[list[int]] = ..., volumes: Optional[list[tuple[str, str, str]]] = ..., network: Optional[Network] = ..., network_aliases: Optional[list[str]] = ..., **kwargs: Any) -> None:
        ...
    
    def with_env(self, key: str, value: str) -> Self:
        ...
    
    def with_envs(self, **variables: str) -> Self:
        ...
    
    def with_env_file(self, env_file: Union[str, PathLike[str]]) -> Self:
        ...
    
    def with_bind_ports(self, container: Union[str, int], host: Optional[Union[str, int]] = ...) -> Self:
        """
        Bind container port to host port

        :param container: container port
        :param host: host port

        :doctest:

        >>> from testcontainers.core.container import DockerContainer
        >>> container = DockerContainer("nginx")
        >>> container = container.with_bind_ports("8080/tcp", 8080)
        >>> container = container.with_bind_ports("8081/tcp", 8081)

        """
        ...
    
    def with_exposed_ports(self, *ports: Union[str, int]) -> Self:
        """
        Expose ports from the container without binding them to the host.

        :param ports: ports to expose

        :doctest:

        >>> from testcontainers.core.container import DockerContainer
        >>> container = DockerContainer("nginx")
        >>> container = container.with_exposed_ports("8080/tcp", "8081/tcp")

        """
        ...
    
    def with_network(self, network: Network) -> Self:
        ...
    
    def with_network_aliases(self, *aliases: str) -> Self:
        ...
    
    def with_kwargs(self, **kwargs: Any) -> Self:
        ...
    
    def maybe_emulate_amd64(self) -> Self:
        ...
    
    def start(self) -> Self:
        ...
    
    def stop(self, force: bool = ..., delete_volume: bool = ...) -> None:
        ...
    
    def __enter__(self) -> Self:
        ...
    
    def __exit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        ...
    
    def get_container_host_ip(self) -> str:
        ...
    
    @wait_container_is_ready()
    def get_exposed_port(self, port: int) -> int:
        ...
    
    def with_command(self, command: Union[str, list[str]]) -> Self:
        ...
    
    def with_name(self, name: str) -> Self:
        ...
    
    def with_volume_mapping(self, host: Union[str, PathLike[str]], container: str, mode: str = ...) -> Self:
        ...
    
    def get_wrapped_container(self) -> Container:
        ...
    
    def get_docker_client(self) -> DockerClient:
        """
        :meta private:
        """
        ...
    
    def get_logs(self) -> tuple[bytes, bytes]:
        ...
    
    def exec(self, command: Union[str, list[str]]) -> ExecResult:
        ...
    


class Reaper:
    """
    :meta private:
    """
    _instance: Optional[Reaper] = ...
    _container: Optional[DockerContainer] = ...
    _socket: Optional[socket] = ...
    @classmethod
    def get_instance(cls) -> Reaper:
        ...
    
    @classmethod
    def delete_instance(cls) -> None:
        ...
    


