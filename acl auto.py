from netmiko import ConnectHandler
import paramiko
import time
from netmiko import ConnectHandler
# Create an empty list
ip_addresses = []
# Get the number of IP addresses to add
num_ips = int(input("Enter the number of IP addresses: "))
# Add IP addresses to the list using a for loop
for i in range(num_ips):
    ip = input("Enter IP address: ")
    ip_addresses.append(ip)

# Display the list of IP addresses
print(ip_addresses)

your_username = input("Enter username: ")
your_password = input("Enter password: ")

routers = []
for ip in ip_addresses:
    router = {
        'device_type': 'hp_comware',
        'ip': ip,
        'username': your_username,
        'password': your_password,
        'read_timeout': 30,  # Set a larger read timeout value

    }
    routers.append(router)

# Display the list of routers
for router in routers:
    print(router)

# Iterate through the routers and configure ACLs

    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**router)

        # Enter configuration mode
        net_connect.config_mode()

        # Create ACL
        command = f'display cu'

        output = net_connect.send_command(command, expect_string=r'#')

        print(f"ACL configuration completed for router {router['ip']}")

        # Disconnect from the router
        net_connect.disconnect()

    except Exception as e:
        print(f"Failed to configure ACL on router {router['ip']}: {str(e)}")

