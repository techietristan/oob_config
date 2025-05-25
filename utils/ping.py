import os, subprocess

def host_pings(ip_address: str, attempts_remaining: int = 10, retry: bool = False) -> bool:
    if attempts_remaining == 0:
        return False

    is_windows: bool = os.sys.platform.lower() ==  'win32' #type: ignore[attr-defined]
    count_param: str = '-n' if is_windows else '-c'
    host_is_pinging: bool = subprocess.run(
        ['ping', count_param, '1', ip_address],
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL         
    ).returncode == 0

    if host_is_pinging:
        return True

    return host_pings(ip_address, attempts_remaining -1, True)

def wait_for_ping(ip_address: dict) -> bool:
    if host_pings(ip_address, 10):
        return True
    return False