import ipaddress

def validate_ip(ip):
    try:
        ipaddress.IPv4Address(ip)
        return "IPv4"
    except ipaddress.AddressValueError:
        try:
            ipaddress.IPv6Address(ip)
            return "IPv6"
        except ipaddress.AddressValueError:
            return None

def es_red_ipv4_valida(ip_cidr):
    try:
        red = ipaddress.IPv4Network(ip_cidr, strict=False)
        return red
    except Exception:
        return None



