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

    def get_selected_vpn_uuid(self) -> str:
        settings = self.get_settings()
        vpn = settings.get('vpn_uuid', 'no-selection')
        return vpn

    def get_selected_vpn_name(self) -> str:
        settings = self.get_settings()
        vpn = settings.get('vpn_name', 'no-selection')
        return vpn

    def on_ready(self) -> None:
        self.update()

    def on_tick(self) -> None:
        self.update()

    def on_key_down(self) -> None:
        print("Key down")
    
    def on_key_up(self) -> None:
        print("Key up")

    def get_config_rows(self) -> "list[Adw.PreferencesRow]":
        vpn_connections = NetworkManager.get_connections('vpn')
        log.debug(f"Found VPN connections: {vpn_connections}")
        rows = [ItemListComboRowListItem("no-selection", "Choose VPN")]

        for vpn in vpn_connections:
            rows.append(ItemListComboRowListItem(vpn.uuid, vpn.name))

        connection_row = ItemListComboRow(items=rows)
        connection_row.set_title("Select Connection")
        connection_row.set_selected_item_by_key(self.get_selected_vpn_uuid())

        connection_row.connect("notify::selected", self.on_connection_changed)

        return [connection_row]

    def on_connection_changed(self, widget, *args):
        log.debug(f"Selected VPN connection: {widget.get_selected_item().name} ({widget.get_selected_item().key})")

        settings = self.get_settings()
        settings["vpn_uuid"] = widget.get_selected_item().key
        settings["vpn_name"] = widget.get_selected_item().name
        self.set_settings(settings)

    def update(self) -> None:
        vpn_name = self.get_selected_vpn_name()
        vpn_uuid = self.get_selected_vpn_uuid()

        if vpn_uuid == 'no-selection':
            return self.handle_no_selection()

        if not NetworkManager.is_connected(vpn_uuid):
            return self.handle_not_connected(vpn_name)

        return self.handle_connected(vpn_name)

    def handle_no_selection(self):
        self.set_top_label(text="Select VPN", font_size=13)
        self.set_center_label("in the")
        self.set_bottom_label("config")

    def handle_not_connected(self, name:str = ""):
        self.set_top_label(name)
        self.set_center_label("")
        self.set_label("VPN OFF")
        pass

    def handle_connected(self, name:str = ""):
        self.set_top_label(name)
        self.set_center_label("")
        self.set_label("VPN ON")
        pass




