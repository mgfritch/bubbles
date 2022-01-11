# bubbles - a simplified management UI for Ceph
# Copyright (C) 2021 SUSE, LLC
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#

from mgr_module import MgrModule

from .fs import CephFS
from .nfs import NFS
from .orch import Orchestrator
from .osd import OSD


class CephController:
    fs: CephFS
    nfs: NFS
    orch: Orchestrator
    osd: OSD

    def __init__(self, mgr: MgrModule) -> None:
        self.fs = CephFS(mgr)
        self.nfs = NFS(mgr)
        self.orch = Orchestrator(mgr)
        self.osd = OSD(mgr)
