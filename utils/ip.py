from ipaddress import IPv4Address as ipv4
from ipaddress import ip_address as get_ip
from ipaddress import ip_network, AddressValueError

def is_valid_ip(ip_address: str) -> bool:
    try:
        ipv4(ip_address)
    except AddressValueError:
        return False
    
    return True

def is_valid_subnet_mask(subnet_mask: str) -> bool:
    stripped_subnet_mask: str = subnet_mask.strip().strip('/')
    is_valid_cidr: bool = stripped_subnet_mask.isdigit() and 0 < int(stripped_subnet_mask) < 33
    if is_valid_ip(stripped_subnet_mask) or is_valid_cidr:
        try:
            return bool(ip_network(f'0.0.0.0/{stripped_subnet_mask}', strict = True))
        except ValueError:
            return False
    else:
        return False

def get_next_ip(ip_address: str) -> str:
    if not is_valid_ip(ip_address):
        return False
    next_ip: ipv4 = get_ip(ip_address) + 1
    next_ip_address: str = str(next_ip)

    return next_ip_address

def get_subnet_mask(subnet_mask: str) -> str:
    stripped_subnet_mask: str = subnet_mask.strip().strip('/')
    if is_valid_subnet_mask(stripped_subnet_mask):
        return str(ip_network(f'0.0.0.0/{stripped_subnet_mask}', strict = True).netmask)
    else:
        return False