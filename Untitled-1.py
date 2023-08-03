ip_addresses = ["192.168.5.225", "10.0.0.1", "172.16.0.1"]
for ip_address in ip_addresses:
    parts = ip_address.split(".")
    print(parts)

ip_addresses = ["192.168.5.225", "10.0.0.1", "172.16.0.1"]
for ip_address in ip_addresses:
    parts = ip_address.split(".")
    last_part = parts[-1]
    print(last_part)

