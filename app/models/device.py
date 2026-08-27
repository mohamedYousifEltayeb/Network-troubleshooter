from typing import Optional

from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hostname: str
    management_ip: str
    vendor: str
    model: str
    device_type: str
    location: str