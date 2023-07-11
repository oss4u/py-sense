import json

from opnsenseapi.ifaces.opnsense import _OpnSense


class Host:
    id: str
    enabled: bool
    hostname: str
    domain: str
    rr: str
    mxprio: int
    mx: str
    server: str
    description: str

    def __init__(self,
                 enabled: bool,
                 hostname: str,
                 domain: str,
                 rr: str,
                 server: str,
                 description: str,
                 mxprio: int = None,
                 mx: str = None,
                 id: str = None):
        self.enabled = enabled
        self.hostname = hostname
        self.domain = domain
        self.rr = rr
        self.server = server
        self.description = description
        self.mx = mx
        self.mxprio = mxprio
        self.id = id


class HostOverride(object):
    ctrl: _OpnSense
    module = "unbound"
    controller = "settings"

    def __init__(self, ctrl: _OpnSense):
        self.ctrl = ctrl

    def create(self, host: Host):
        data = self.create_json_from_host(host)
        result = self.ctrl.modifying_request(self.module, self.controller, 'addHostOverride', data=data)
        if result['result'] == "saved":
            host.id = result['uuid']
            return host
        else:
            print(f"ERROR: {result}")
            return host

    def read(self, id: str):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'getHostOverride', params=[id])
        print(result)

    def update(self, host: Host):
        data = self.create_json_from_host(host)
        result = self.ctrl.modifying_request(self.module, self.controller, 'setHostOverride', data=data, params=[host.id])
        print(f"RES: {result}")
        if result['result'] == "saved":
            return host
        else:
            print(f"ERROR: {result}")
            return host

    def delete(self, host: Host):
        result = self.ctrl.modifying_request(self.module, self.controller, 'delHostOverride', params=[host.id])
        print(result)

    def get(self, id):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'getHostOverride', params=[id])
        print(result)

    def list(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def search(self):
        result = self.ctrl.non_modifying_request(self.module, self.controller, 'searchHostOverride')
        print(result)

    def create_host_from_json(self, result_json):
        host_json = json.loads(result_json)['host']
        if host_json['enabled'] == 1:
            enabled = 1
        else:
            enabled = 0
        h = Host(
            enabled=enabled,
            hostname=host_json['hostname'],
            domain=host_json['domain'],
            server=host_json['server'],
            description=host_json['description'],
            mxprio=host_json['mxprio'],
            mx=host_json['mx'],
            rr=host_json['rr']
        )
        return h

    def create_json_from_host(self, host: Host):
        enabled = 0
        if host.enabled:
            enabled = 1
        if not host.mx:
            mx = ""
        else:
            mx = host.mx
        if not host.mxprio:
            mxprio = ""
        else:
            mxprio = str(host.mxprio)

        h = {
            'host': {
                'enabled': str(enabled),
                'hostname': host.hostname,
                'domain': host.domain,
                'rr': host.rr,
                'mxprio': mxprio,
                'mx': mx,
                'server': host.server,
                'description': host.description
            }
        }
        return json.dumps(h, indent=2)
