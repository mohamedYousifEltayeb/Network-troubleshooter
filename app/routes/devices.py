import uuid
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select

from app.core.templates import templates
from app.database import get_session
from app.models.device import Device
from app.models.ping_history import PingHistory
from app.services.device_service import (create_device,
    get_all_devices,
    delete_device,
    update_device,
    get_device_by_ip)
from app.services.connectivity_service import (ping_device,run_ping_session)
from pydantic import ValidationError
from app.schemas.device import DeviceCreate
from sqlalchemy.exc import IntegrityError

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
    hostname: str = Form(default =""),
    vendor: str = Form(default =""),
    device_type: str = Form(default =""),
    management_ip: str = Form(default =""),
    location: str = Form(default =""),
    model: str = Form(default =""),
):
    try:
        device_data = DeviceCreate(
        hostname=hostname,
        management_ip=management_ip,
        vendor=vendor,
        model=model,
        device_type=device_type,
        location=location
        )
    except ValidationError as e:
        errors = e.errors()
        error_messages = []

        for error in errors:
            if error["loc"] ==("management_ip",):
                   error_messages.append("Please enter a valid management IP address..")
            elif error["loc"] == ("hostname",):
                   error_messages.append("Hostname is required.")
            elif error["loc"] == ("vendor",):
                   error_messages.append("Vendor is required. ")

            elif error["loc"] == ("model",):
                   error_messages.append("Model is required. ")
            elif error["loc"] ==("device_type",):
                   error_messages.append("Device type is required.")

            elif error["loc"] ==("location",):
                   error_messages.append("Location is required. ")

        return templates.TemplateResponse(
            request = request,
            name ="add_device.html",
            context ={
                "errors": error_messages,
                "hostname":hostname,
                "management_ip": management_ip,
                "model": model,
                "vendor": vendor,
                "device_type": device_type,
                "location": location
            }
        )

    existing_device = get_device_by_ip(
        session,
        str(device_data.management_ip)
    )
    if existing_device:
        return templates.TemplateResponse(
            request = request,
            name = "add_device.html",
            context = {
                "errors": ["This management IP address is already assigned to another device."],
                "hostname": hostname,
                "management_ip": management_ip,
                "model" : model,
                "vendor": vendor,
                "device_type": device_type,
                "location": location,
            },
            status_code = 400,
        )
    try:
            create_device(session, device_data)
    except IntegrityError:
        session.rollback()
        return templates.TemplateResponse(
                request=request,
                name="add_device.html",
                context={
                    "errors": [
                        "This management IP address is already assigned to another device."
                    ],
                    "hostname": hostname,
                    "management_ip": management_ip,
                    "model": model,
                    "vendor": vendor,
                    "device_type": device_type,
                    "location": location,
                },
                status_code=400,
            )

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
    request: Request,
    hostname: str = Form(),
    management_ip: str = Form(),
    vendor: str = Form(),
    model: str = Form(),
    device_type: str = Form(),
    location: str = Form(),
    session: Session = Depends(get_session)
):
    try:
        device_data = DeviceCreate(
            hostname=hostname,
            management_ip=management_ip,
            vendor=vendor,
            model=model,
            device_type=device_type,
            location=location,
        )
    except ValidationError:
        statement = select(Device).where(Device.id == device_id)
        device = session.exec(statement).first()

        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        # Preserve the submitted values so the user can correct them.
        device.hostname = hostname
        device.management_ip = management_ip
        device.vendor = vendor
        device.model = model
        device.device_type = device_type
        device.location = location

        return templates.TemplateResponse(
            request=request,
            name="edit_device.html",
            context={
                "device": device,
                "errors": [
                    "Please enter a valid IP address and complete all required fields."
                ],
            },
            status_code=400,
        )

    try:
        device = update_device(
            session,
            device_id,
            hostname,
            str(device_data.management_ip),
            vendor,
            model,
            device_type,
            location,
        )
    except ValueError as e:
        statement = select(Device).where(Device.id == device_id)
        device = session.exec(statement).first()

        if device is None:
            raise HTTPException(status_code=404, detail="Device not found")

        return templates.TemplateResponse(
            request=request,
            name="edit_device.html",
            context={
                "device": device,
                "errors": [str(e)],
                "submitted_management_ip": management_ip,
            },
            status_code=400,
        )

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return RedirectResponse(url="/devices", status_code=303)

@router.get("/devices/{device_id}")
def devices_details(
    device_id:int,
    request: Request,
    ping: str | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Device).where(Device.id == device_id)
    device = session.exec(statement).first()

    if device is None:
        raise HTTPException(status_code = 404, detail = "Device not found")
    history_statement = (
        select(PingHistory)
        .where(PingHistory.device_id == device_id)
        .order_by(PingHistory.timestamp.desc())
    )
    ping_history = session.exec(history_statement).all()

    latest_session = next(
        (record for record in ping_history if record.session_id is not None), None
    )
    session_history = [
        record for record in ping_history
        if latest_session is not None
        and record.session_id == latest_session.session_id
    ]
    chart_labels = [record.timestamp.strftime("%m-%d %H:%M")
        for record in reversed(ping_history)]

    chart_data = [record.response_time_ms
        for record in reversed(ping_history)]

    response_times = [
        record.response_time_ms
        for record in session_history
        if record.response_time_ms is not None
    ]

    total_pings = len(session_history)

    successful_pings = sum(
        1 for record in session_history
        if record.result == "Success"
    )

    failed_pings = sum(
        1 for record in session_history
        if record.result == "Failed"
    )

    packet_loss = (
        (failed_pings / total_pings) * 100
        if total_pings > 0 else 0
    )

    average_time = (
        sum(response_times) / len(response_times)
        if response_times else None
    )

    minimum_time = min(response_times) if response_times else None
    maximum_time = max(response_times) if response_times else None
    return templates.TemplateResponse(
        request = request,
        name="device_details.html",
        context={"device":device,
            "ping": ping,
            "ping_history": ping_history,
            "total_pings": total_pings,
            "successful_pings": successful_pings,
            "failed_pings": failed_pings,
            "packet_loss": packet_loss,
            "average_time": average_time,
            "minimum_time": minimum_time,
            "maximum_time": maximum_time,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
            "session_history": session_history,

        }
    )
@router.post("/devices/{device_id}/ping")
def ping_device_route(
    device_id : int,
    session: Session = Depends(get_session)
):
    statement = select(Device).where(Device.id == device_id)
    device = session.exec(statement).first()

    if device is None:
        raise HTTPException(status_code=404, detail= "Device not found")
    is_reachable,response_time_ms  = ping_device(device.management_ip)
    record = PingHistory(
        device_id = device.id,
        ip_address = device.management_ip,
        result = "Success" if is_reachable else "Failed",
        response_time_ms= response_time_ms
    )
    session.add(record)

    device.status = "Reachable" if is_reachable else "Unreachable"

    session.add(device)
    session.commit()
    session.refresh(device)

    return RedirectResponse(
        url=f"/devices/{device_id}?ping={'success' if is_reachable else 'failed'}",
        status_code=303
    )
@router.post("/devices/{device_id}/ping-session")
def ping_session_route(
device_id: int,
session: Session = Depends(get_session)
):
    statement = select(Device).where(Device.id == device_id)
    device = session.exec(statement).first()

    if device is None:
        raise HTTPException(status_code =404, detail= "Device is not found")


    results = run_ping_session(device.management_ip, count= 10)
    session_id = str(uuid.uuid4())
    for result in results:
        record = PingHistory(
            device_id = device.id,
            ip_address = device.management_ip,
            result = result["result"],
            response_time_ms = result["response_time_ms"],
            session_id = session_id
        )
        session.add(record)

    successful_pings = sum(
        1 for result in results
        if result["result"] == "Success"
    )
    device.status = (
        "Reachable" if successful_pings > 0 else "Unreachable"
    )

    session.add(device)
    session.commit()

    return RedirectResponse(
            url=f"/devices/{device_id}",
            status_code=303
        )
