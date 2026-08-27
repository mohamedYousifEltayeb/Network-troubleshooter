from pydantic import BaseModel, IPvAnyAddress, Field, ValidationError


class DeviceCreate(BaseModel):
    hostname: str = Field(min_length = 1)
    management_ip: IPvAnyAddress
    vendor: str = Field(min_length = 1)
    model: str = Field(min_length= 1)
    device_type: str = Field(min_length = 1)
    location: str = Field(min_length = 1)