# bubbles - a simplified management UI for Ceph
# Copyright (C) 2021 SUSE, LLC
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
from typing import Callable, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status

from bubbles.backend.api import jwt_auth_scheme
from bubbles.backend.controllers.ceph.orch import Error
from bubbles.backend.models.ceph.orch import DaemonModel, ServiceModel
from bubbles.bubbles import Bubbles

router = APIRouter(prefix="/ceph/orch", tags=["ceph"])


@router.get(
    "/service",
    name="List Orchestrator services",
    response_model=List[ServiceModel],
)
async def ls(
    request: Request,
    _: Callable = Depends(jwt_auth_scheme),
    service_type: Optional[str] = None,
    service_name: Optional[str] = None,
    refresh: bool = False,
) -> List[ServiceModel]:
    bubbles: Bubbles = request.app.state.bubbles
    try:
        return bubbles.ctrls.ceph.orch.ls(
            service_type=service_type,
            service_name=service_name,
            refresh=refresh,
        )
    except Error as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/daemon",
    name="List Orchestrator daemons",
    response_model=List[DaemonModel],
)
async def ps(
    request: Request,
    _: Callable = Depends(jwt_auth_scheme),
    hostname: Optional[str] = None,
    service_name: Optional[str] = None,
    daemon_type: Optional[str] = None,
    daemon_id: Optional[str] = None,
    refresh: bool = False,
) -> List[DaemonModel]:
    bubbles: Bubbles = request.app.state.bubbles
    try:
        return bubbles.ctrls.ceph.orch.ps(
            hostname=hostname,
            service_name=service_name,
            daemon_type=daemon_type,
            daemon_id=daemon_id,
            refresh=refresh,
        )
    except Error as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
