from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.core.templates import templates
from app.database import get_session
from app.models.device import Device
from app.services.device_service import create_device, get_all_devices, delete_device, update_device

router = APIRouter()


@router.get("/devices/add")
def add_device(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="add_device.html"
    )


@router.post("/devices")
def adding_device(
    request: Request,
    session: Session = Depends(get_session),
    hostname: str = Form(),
    vendor: str = Form(),
    device_type: str = Form(),
    management_ip: str = Form(),
    location: str = Form(),
    model: str = Form(),
):
    device = Device(
        hostname=hostname,
        management_ip=management_ip,
        vendor=vendor,
        model=model,
        device_type=device_type,
        location=location,
    )

    create_device(session, device)

    return RedirectResponse(url="/devices", status_code=303)

@router.get("/devices")
def get_devices(request: Request, session: Session = Depends(get_session)):
    devices = get_all_devices(session)
    context = {"devices": devices}
    return templates.TemplateResponse(
        request=request, 
        name="devices.html", 
        context=context
    )
@router.post("/devices/{device_id}/delete")
def delete_device_route(device_id:int , session: Session = Depends(get_session)):
    device  = delete_device(session, device_id)
    if device is None:
        raise HTTPException(
        status_code= 404, detail = "Device not found"
        )
    return RedirectResponse(url="/devices", status_code= 303)
        
   
@router.get("/devices/{device_id}/edit")
def edit_device_form(
    device_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    statement = select(Device).where(Device.id == device_id)

    device = session.exec(statement).first()

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="edit_device.html",
        context={"device": device}
    )
@router.post("/devices/{device_id}/edit")
def edit_device(
    device_id: int,
    hostname: str = Form(),
    management_ip: str = Form(),
    vendor: str = Form(),
    model: str = Form(),
    device_type: str = Form(),
    location: str = Form(),
    session: Session = Depends(get_session)
):
    device = update_device(
    session, device_id, hostname, management_ip, vendor, model, device_type, location)
    if device is None:
        raise HTTPException(status_code= 404, detail = "Device not found")
        
    return RedirectResponse(url = "/devices", status_code = 303)
        
    