# flake8: noqa

import os

from opnsenseapi import opnsense

fw = opnsense.OpnSense(
    opnsense_address=os.getenv("OPNSENSE_ADDRESS"),
    opnsense_key=os.getenv("OPNSENSE_KEY"),
    opnsense_secret=os.getenv("OPNSENSE_SECRET"),
    verify_cert=False
)

unbound = fw.core().get_unbound().get_settings().get_host_override()
unbound.list()
# host = Host(id="eafe4ace-6b3d-4a4e-99f0-56c2b8176bf4",enabled=True, hostname="test01", server="10.10.10.10", domain="test.de",description="My Test Host", rr="A")
#
# unbound.create(host)
# unbound.get(host.id)
# host.hostname = "abc"
# unbound.update(host)
# unbound.read(host.id)
# unbound.delete_by_host(host)
unbound.delete_by_id("9c654e09-ca7d-402d-b2bb-38fb3c7983e9")
