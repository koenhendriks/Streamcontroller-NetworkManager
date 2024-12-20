import logging
import subprocess
from typing import List, Optional


class NetworkConnection:
    def __init__(self, name: str, uuid: str, conn_type: str, device: Optional[str]):
        self.name = name
        self.uuid = uuid
        self.conn_type = conn_type
        self.device = device

    def __repr__(self):
        return (
            f"NetworkConnection(name='{self.name}', uuid='{self.uuid}', "
            f"type='{self.conn_type}', device='{self.device}')"
        )


class NetworkManager:
    @staticmethod
    def get_connections(conn_type: Optional[str] = None) -> List[NetworkConnection]:
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "NAME,UUID,TYPE,DEVICE", "con", "show"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            connections = []

            for line in result.stdout.strip().split("\n"):
                if line:  # Skip empty lines
                    parts = line.split(":")
                    if len(parts) == 4:
                        name, uuid, conn_type_parsed, device = parts
                        device = device if device else None  # Handle empty device field
                        connection = NetworkConnection(name, uuid, conn_type_parsed, device)
                        # Filter by type if specified
                        if conn_type is None or conn_type_parsed == conn_type:
                            connections.append(connection)
            return connections

        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing nmcli to retrieve connections: {e.stderr}")
            return []

    @staticmethod
    def activate_connection(uuid: str) -> bool:
        try:
            subprocess.run(
                ["nmcli", "con", "up", uuid],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing nmcli to activate connection: {e.stderr}")
            return False

    @staticmethod
    def deactivate_connection(uuid: str) -> bool:
        try:
            subprocess.run(
                ["nmcli", "con", "down", uuid],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return True

        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing nmcli to deactivate connection: {e.stderr}")
            return

    @staticmethod
    def is_connected(uuid: str) -> bool:
        try:
            result = subprocess.run(
                ["nmcli", "-t", "-f", "UUID,STATE", "con", "show", "--active"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            for line in result.stdout.strip().split("\n"):
                if line:  # Skip empty lines
                    active_uuid, state = line.split(":")
                    if active_uuid == uuid and state == "activated":
                        return True
            return False

        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing nmcli to check active connection: {e.stderr}")
            return False
