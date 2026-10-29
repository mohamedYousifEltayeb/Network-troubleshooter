import platform
import subprocess
import re

def ping_device(ip_address: str) -> tuple[bool, float | None]:
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
        is_reachable = result.returncode == 0
        response_time_ms = None
        if is_reachable:
            match = re.search(
                            r"time[=<]\s*(\d+(?:\.\d+)?)\s*ms",
                            result.stdout,
                            re.IGNORECASE
                        )
            if match:
                response_time_ms = float(match.group(1))
        return is_reachable, response_time_ms
    except(subprocess.TimeoutExpired, FileNotFoundError):
        return False, None
