from datetime import datetime, timezone
from pickletools import stringnl_noescape_pair
from sqlite3.dbapi2 import Timestamp
from sqlmodel import Field, SQLModel

class PingHistory( SQLModel, table = True):
    id: int | None = Field(default = None , primary_key = True)
    session_id:str | None = Field(default = None , index = True)

    device_id: int = Field( foreign_key = "device.id", index = True)
    ip_address: str
    result: str
    response_time_ms: float | None = None

    timestamp: datetime = Field(
        default_factory = lambda: datetime.now(timezone.utc),
        index= True
    )
