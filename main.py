# Import StreamController modules
from data.plugins.NetworkManager.actions.ToggleVpn.ToggleVpn import ToggleVpn
from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()

        ## Register actions
        self.toggle_vpn_holder = ActionHolder(
            plugin_base = self,
            action_base = ToggleVpn,
            action_id = "com_koenhendriks_NetworkManager::ToggleVpn",
            action_name = "Toggle VPN",
        )
        self.add_action_holder(self.toggle_vpn_holder)

        # Register plugin
        self.register(
            plugin_name = "NetworkManager",
            github_repo = "https://github.com/koenhendriks/Streamcontroller-NetworkManager/",
            plugin_version = "0.1.0",
            app_version = "1.1.1-alpha"
        )