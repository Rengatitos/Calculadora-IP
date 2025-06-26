import ipaddress

def ipv4_to_hex(ipv4):
    try:
        octetos = ipv4.split('.')
        hex_parts = [format(int(o), '02X') for o in octetos]
        part1 = hex_parts[0] + hex_parts[1]
        part2 = hex_parts[2] + hex_parts[3]
        part1 = part1.lstrip('0') or '0'
        part2 = part2.lstrip('0') or '0'
        return f"{part1}:{part2}"
    except (ValueError, IndexError, AttributeError):
        return None

def ipv4_to_ipv6(ipv4):
    try:
        ipaddress.IPv4Address(ipv4)
        hex_ip = ipv4_to_hex(ipv4)
        if hex_ip:
            return f"::FFFF:{hex_ip}"
        return None
    except ipaddress.AddressValueError:
        return None

def ipv6_to_ipv4(ipv6):
    try:
        ipv6_obj = ipaddress.IPv6Address(ipv6)
        if ipv6_obj.ipv4_mapped:
            return str(ipv6_obj.ipv4_mapped)
        elif '::ffff:' in ipv6.lower():
            parts = ipv6.split(':')[-2:]
            if len(parts) == 2:
                hex_str = parts[0] + parts[1]
                if len(hex_str) == 8:
                    octetos = [
                        str(int(hex_str[i:i+2], 16)) 
                        for i in range(0, 8, 2)
                    ]
                    return '.'.join(octetos)
        return None
    except ipaddress.AddressValueError:
        return None

import ipaddress

import ipaddress

def calcular_subredes(ip_cidr, lista_hosts_por_subred, cantidad_a_mostrar):
    red_base = ipaddress.IPv4Network(ip_cidr, strict=False)
    subredes_resultado = []

    red_actual = red_base.network_address

    for cantidad_hosts in lista_hosts_por_subred:
        cantidad_total = cantidad_hosts + 2  # Red + Broadcast
        bits_necesarios = (cantidad_total - 1).bit_length()
        prefijo = 32 - bits_necesarios

        try:
            nueva_red = ipaddress.IPv4Network((red_actual, prefijo), strict=False)
        except ValueError:
            break 
        
        #---------------------------------------
        nueva_red = ipaddress.IPv4Network(f"{nueva_red.network_address}/{prefijo}")
        

        if not nueva_red.subnet_of(red_base):
            break 

        # Obtener hosts disponibles
        hosts = list(nueva_red.hosts())
        router = hosts[0] if hosts else None
        hosts_mostrados = hosts[1:1 + cantidad_a_mostrar] if len(hosts) > 1 else []
        ultimo = hosts[-1] if hosts else None


        datos = {
            "subred": str(nueva_red),
            "mascara": str(nueva_red.netmask),
            "prefijo": nueva_red.prefixlen,                 
            "cantidad_hosts": nueva_red.num_addresses - 2, 
            "inicio": str(nueva_red.network_address),
            "fin": str(nueva_red.broadcast_address),
            "router": str(router) if router else None,
            "broadcast": str(nueva_red.broadcast_address),
            "ultimo_host": str(ultimo) if ultimo else None
        }


        for i, h in enumerate(hosts_mostrados):
            datos[f"host_{i + 1}"] = str(h)

        subredes_resultado.append(datos)


        red_actual = nueva_red.broadcast_address + 1

    return subredes_resultado

def calcular_subredes_fijo(ip_cidr, cantidad_subredes, cantidad_a_mostrar):
    red_base = ipaddress.IPv4Network(ip_cidr, strict=False)
    subredes_resultado = []


    bits_extra = (cantidad_subredes - 1).bit_length()
    nuevo_prefijo = red_base.prefixlen + bits_extra

    if nuevo_prefijo > 32:
        raise ValueError("No es posible subdividir la red base en la cantidad de subredes solicitadas.")

    subredes_generadas = list(red_base.subnets(new_prefix=nuevo_prefijo))

    if len(subredes_generadas) < cantidad_subredes:
        raise ValueError("No hay suficientes subredes disponibles.")

    for i in range(cantidad_subredes):
        subred = subredes_generadas[i]
        hosts = list(subred.hosts())
        router = hosts[0] if hosts else None
        hosts_mostrados = hosts[1:1 + cantidad_a_mostrar] if len(hosts) > 1 else []
        ultimo = hosts[-1] if hosts else None

        datos = {
            "subred": str(subred),
            "mascara": str(subred.netmask),
            "prefijo": subred.prefixlen,
            "cantidad_hosts": subred.num_addresses - 2,
            "inicio": str(subred.network_address),
            "fin": str(subred.broadcast_address),
            "router": str(router) if router else None,
            "broadcast": str(subred.broadcast_address),
            "ultimo_host": str(ultimo) if ultimo else None
        }

        for j, h in enumerate(hosts_mostrados):
            datos[f"host_{j + 1}"] = str(h)

        subredes_resultado.append(datos)

    return subredes_resultado


