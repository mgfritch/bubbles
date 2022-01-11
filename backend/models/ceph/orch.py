# Copyright (C) 2022 SUSE, LLC
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
from typing import List, Optional

from pydantic import BaseModel


class ServiceStatus(BaseModel):
    created: str
    last_refresh: str
    running: int
    size: int
    ports: Optional[List[int]]


class ServiceModel(BaseModel):
    service_type: str
    service_id: Optional[str]  # TODO: missing for crash service
    service_name: str
    placement: dict
    status: ServiceStatus
