import platform
import subprocess

def ping_device(ip_address: str) -> bool:
    """ Return True if the device responds to ping"""
    operating_system = platform.system().lower()

    if operating_system == "windows":
        command = ["ping", "-n", "1","-w", "2000", ip_address]

    else:
        command = ["ping", "-c", "1","-W", "2", ip_address ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text = True,
            timeout=4
        )
        print("Ping command:", command)
        print("Return code:", result.returncode)
        print("Ping output:", result.stdout)
        print("Ping errors:", result.stderr)
        return result.returncode == 0
    except(subprocess.TimeoutExpired, FileNotFoundError):
        return False
