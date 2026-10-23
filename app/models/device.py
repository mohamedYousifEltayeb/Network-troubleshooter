from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hostname: str
    management_ip: str = Field(unique = True, index = True)
    vendor: str
    model: str
    device_type: str
    location: str
    status: str = Field( default ="Unknown", index = True)
