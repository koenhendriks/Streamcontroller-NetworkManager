# Import StreamController modules
from GtkHelper.ItemListComboRow import ItemListComboRowListItem, ItemListComboRow
from data.plugins.NetworkManager.services.NetworkManager import NetworkManager
from src.backend.PluginManager.ActionBase import ActionBase
from loguru import logger as log


# Import python modules
import os

# Import gtk modules - used for the config rows
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

class ToggleVpn(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_ready(self) -> None:
        icon_path = os.path.join(self.plugin_base.PATH, "assets", "info.png")
        self.set_media(media_path=icon_path, size=0.75)
        self.set_label("yes")

    def on_key_down(self) -> None:
        print("Key down")
    
    def on_key_up(self) -> None:
        print("Key up")

    def get_config_rows(self):
        vpn_connections = NetworkManager.get_connections('vpn')
        log.debug(f"Found VPN connections: {vpn_connections}")
        rows = [ItemListComboRowListItem("no-selection", "Choose VPN")]
        for vpn in vpn_connections:
            rows.append(
                ItemListComboRowListItem(vpn.uuid, vpn.name)
            )

        connection_row = ItemListComboRow(items=rows)
        connection_row.set_title("Select Connection")
        connection_row.connect("notify::selected", self.on_connection_changed)

        return [connection_row]

    def on_connection_changed(self, widget, *args):
        settings = self.get_settings()
        log.debug(f"Selected VPN connection: {widget.get_selected_item().name}")
        settings["vpn"] = widget.get_selected_item().key
        self.set_settings(settings)