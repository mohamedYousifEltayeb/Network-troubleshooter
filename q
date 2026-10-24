warning: in the working copy of 'app/static/style.css', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/app/routes/devices.py b/app/routes/devices.py[m
[1mindex 69fe86f..696fcd6 100644[m
[1m--- a/app/routes/devices.py[m
[1m+++ b/app/routes/devices.py[m
[36m@@ -10,6 +10,7 @@[m [mfrom app.services.device_service import (create_device,[m
     delete_device,[m
     update_device,[m
     get_device_by_ip)[m
[32m+[m[32mfrom app.services.connectivity_service import ping_device[m
 from pydantic import ValidationError[m
 from app.schemas.device import DeviceCreate[m
 from sqlalchemy.exc import IntegrityError[m
[36m@@ -249,6 +250,7 @@[m [mdef edit_device([m
 def devices_details([m
     device_id:int,[m
     request: Request,[m
[32m+[m[32m    ping: str | None = None,[m
     session: Session = Depends(get_session)[m
 ):[m
     statement = select(Device).where(Device.id == device_id)[m
[36m@@ -259,5 +261,29 @@[m [mdef devices_details([m
     return templates.TemplateResponse([m
         request = request,[m
         name="device_details.html",[m
[31m-        context={"device":device}[m
[32m+[m[32m        context={"device":device,[m
[32m+[m[32m            "ping": ping[m
[32m+[m[32m        }[m
[32m+[m[32m    )[m
[32m+[m[32m@router.post("/devices/{device_id}/ping")[m
[32m+[m[32mdef ping_device_route([m
[32m+[m[32m    device_id : int,[m
[32m+[m[32m    session: Session = Depends(get_session)[m
[32m+[m[32m):[m
[32m+[m[32m    statement = select(Device).where(Device.id == device_id)[m
[32m+[m[32m    device = session.exec(statement).first()[m
[32m+[m
[32m+[m[32m    if device is None:[m
[32m+[m[32m        raise HTTPException(status_code=404, detail= "Device not found")[m
[32m+[m[32m    is_reachable = ping_device(device.management_ip)[m
[32m+[m
[32m+[m[32m    device.status = "Reachable" if is_reachable else "Unreachable"[m
[32m+[m
[32m+[m[32m    session.add(device)[m
[32m+[m[32m    session.commit()[m
[32m+[m[32m    session.refresh(device)[m
[32m+[m
[32m+[m[32m    return RedirectResponse([m
[32m+[m[32m        url=f"/devices/{device_id}?ping={'success' if is_reachable else 'failed'}",[m
[32m+[m[32m        status_code=303[m
     )[m
[1mdiff --git a/app/services/connectivity_service.py b/app/services/connectivity_service.py[m
[1mindex 6ab678e..b778aee 100644[m
[1m--- a/app/services/connectivity_service.py[m
[1m+++ b/app/services/connectivity_service.py[m
[36m@@ -18,6 +18,10 @@[m [mdef ping_device(ip_address: str) -> bool:[m
             text = True,[m
             timeout=4[m
         )[m
[32m+[m[32m        print("Ping command:", command)[m
[32m+[m[32m        print("Return code:", result.returncode)[m
[32m+[m[32m        print("Ping output:", result.stdout)[m
[32m+[m[32m        print("Ping errors:", result.stderr)[m
         return result.returncode == 0[m
     except(subprocess.TimeoutExpired, FileNotFoundError):[m
         return False[m
[1mdiff --git a/app/static/style.css b/app/static/style.css[m
[1mindex 5337d63..c365d5f 100644[m
[1m--- a/app/static/style.css[m
[1m+++ b/app/static/style.css[m
[36m@@ -12,3 +12,16 @@[m [mh1 {[m
 p {[m
     color: #444;[m
 }[m
[32m+[m
[32m+[m[32m.ping-success {[m
[32m+[m[32m    color: green;[m
[32m+[m[32m    background-color: #e8f5e9;[m
[32m+[m[32m    padding: 10px;[m
[32m+[m[32m    border-radius: 5px;[m
[32m+[m[32m}[m
[32m+[m[32m.ping-failed {[m
[32m+[m[32m    color: #b71c1c;[m
[32m+[m[32m    background-color: #ffebee;[m
[32m+[m[32m    padding: 10px;[m
[32m+[m[32m    border-radius: 5px;[m
[32m+[m[32m}[m
[1mdiff --git a/app/templates/device_details.html b/app/templates/device_details.html[m
[1mindex 4416c0c..cd88032 100644[m
[1m--- a/app/templates/device_details.html[m
[1m+++ b/app/templates/device_details.html[m
[36m@@ -2,12 +2,22 @@[m
 <html>[m
     <head>[m
         <title> Device Details</title>[m
[31m-        < link rel ="stylesheet" href="/static/style.css">[m
[32m+[m[32m        <link rel ="stylesheet" href="/static/style.css">[m
     </head>[m
     <body>[m
[31m-        <div class="head">[m
[32m+[m[32m        <div>[m
[32m+[m[32m            <div class="head">[m
             <h1>Device details</h1>[m
         </div>[m
[32m+[m[32m        {% if ping == "success" %}[m
[32m+[m[32m            <p class="ping-success">[m
[32m+[m[32m                Ping Successful! The device responded to ICMP.[m
[32m+[m[32m            </p>[m
[32m+[m[32m        {% elif ping == "failed" %}[m
[32m+[m[32m              <p class="ping-failed">[m
[32m+[m[32m                  Ping failed. The device did not respond to ICMP.[m
[32m+[m[32m              </p>[m
[32m+[m[32m        {% endif %}[m
         <div class="table">[m
             <table>[m
                 <tr>[m
[36m@@ -46,5 +56,8 @@[m
         </div>[m
         <p> <a href="/devices"> Back to Device Inventory </a></p>[m
         <p><a href="/devices/{{ device.id }}/edit"> Edit Device </a></p>[m
[32m+[m[32m        <form action ="/devices/{{device.id}}/ping" method ="post">[m
[32m+[m[32m            <button type="submit">Ping Device</button>[m
[32m+[m[32m        </form>[m
     </body>[m
 </html>[m
