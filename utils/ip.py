from ipaddress import IPv4Address as ipv4
from ipaddress import ip_address as get_ip
from ipaddress import AddressValueError, NetmaskValueError, ip_address

def is_valid_ip(ip_address: str) -> bool:
    try:
        ipv4(ip_address)
    except AddressValueError:
        return False
    
    return True

def get_next_ip(ip_address: str) -> str:
    if not is_valid_ip(ip_address):
        return False
    next_ip: ipv4 = get_ip(ip_address) + 1
    next_ip_address: str = str(next_ip)

    return next_ip_address
