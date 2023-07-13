from opnsenseapi.core.unbound.settings.host_override import HostOverride, _HostOverride
from opnsenseapi.ifaces.opnsense import _OpnSense


class _Settings:
    def host_override(self) -> _HostOverride:
        pass


class Settings(_Settings):
    ctrl: _OpnSense

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def host_override(self) -> _HostOverride:
        return HostOverride(self.ctrl)
