from sqlmodel import Session, select
from app.models.device import Device
from app.schemas.device import DeviceCreate

device_data = DeviceCreate(
    hostname=hostname,
    management_ip=management_ip,
    vendor=vendor,
    model=model,
    device_type=device_type,
    location=location
)

create_device(session, device_data)

def create_device(session: Session, data:DeviceCreate):
    device = Device(
    hotname = data.hostname,
    management_ip = data.management_ip,
    vendor = data.vendor,
    model = data.model,
    device_type = data.device_type,
    location = data.location
    )
    session.add(device)
    session.commit()
    session.refresh(device)
    return device
    
def get_all_devices(session: Session):
    statement = select(Device)
    results = session.exec(statement)
    devices = results.all()
    return devices
    
def delete_device(session: Session, device_id: int):
    statement = select(Device).where(Device.id == device_id)
    device = session.exec(statement).first()

    if device is None:
        return None

    session.delete(device)
    session.commit()
    return device

def update_device(
session: Session,
device_id: int, 
hostname: str,
management_ip: str,
vendor: str,
model: str, 
device_type: str,
location:str
):
    statement = select(Device).where(Device.id == device_id)
    device = session.exec(statement).first()
    if device is None:
        return None
    device.hostname = hostname
    device.management_ip = management_ip
    device.vendor = vendor
    device.model = model
    device.device_type = device_type
    device.location = location
    session.commit()
    session.refresh(device)
    return device
