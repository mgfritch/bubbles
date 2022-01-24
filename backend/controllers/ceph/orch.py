# Copyright (C) 2021 SUSE, LLC
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
import json
import logging
from typing import List, NewType, Optional

import yaml
from mgr_module import MgrModule, MonCommandFailed
from pydantic.tools import parse_obj_as

from bubbles.backend.models.ceph.orch import (
    DaemonModel,
    ServiceModel,
    ServiceRequest,
)

logger = logging.getLogger(__name__)


class Error(Exception):
    pass


class Orchestrator:
    _mgr: MgrModule

    def __init__(self, mgr: MgrModule) -> None:
        self._mgr = mgr

    def ls(
        self,
        service_type: Optional[str] = None,
        service_name: Optional[str] = None,
        refresh: bool = False,
    ) -> List[ServiceModel]:
        cmd: dict = {
            "prefix": "orch ls",
            "format": "json",
        }
        if service_type:
            cmd["service_type"] = service_type
        if service_name:
            cmd["service_name"] = service_name
        if refresh:
            cmd["refresh"] = refresh

        try:
            _, out, _ = self._mgr.check_mon_command(cmd)
        except MonCommandFailed as e:
            raise Error(e)

        return parse_obj_as(List[ServiceModel], json.loads(out))

    def ps(
        self,
        hostname: Optional[str] = None,
        service_name: Optional[str] = None,
        daemon_type: Optional[str] = None,
        daemon_id: Optional[str] = None,
        refresh: bool = False,
    ) -> List[DaemonModel]:
        cmd: dict = {
            "prefix": "orch ps",
            "format": "json",
        }
        if hostname:
            cmd["hostname"] = hostname
        if service_name:
            cmd["service_name"] = service_name
        if daemon_type:
            cmd["daemon_type"] = daemon_type
        if daemon_id:
            cmd["daemon_id"] = daemon_id
        if refresh:
            cmd["refresh"] = refresh

        try:
            _, out, _ = self._mgr.check_mon_command(cmd)
        except MonCommandFailed as e:
            raise Error(e)

        return parse_obj_as(List[DaemonModel], json.loads(out))

    def apply(
        self,
        req: ServiceRequest,
        dry_run: bool = False,
        no_overwrite: bool = False,
    ) -> str:
        inbuf = yaml.dump(dict(req))

        cmd: dict = {
            "prefix": "orch apply",
            "inbuf": inbuf,
        }

        if dry_run:
            cmd["dry_run"] = dry_run
        if no_overwrite:
            cmd["no_overwrite"] = no_overwrite

        try:
            _, out, _ = self._mgr.check_mon_command(cmd)
        except MonCommandFailed as e:
            raise Error(e)

        return out
