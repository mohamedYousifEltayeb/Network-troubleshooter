from app.services.connectivity_service import ping_device

ip_address = "127.0.0.1"

result = ping_device(ip_address)

if result:
    print(f"{ip_address} is reachable.")
else:
    print(f"{ip_address} did not respond to ping.")
