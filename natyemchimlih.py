from netmiko import ConnectHandler
import paramiko
import time
class ConfigurationError(Exception):
    pass

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


routers = []
for ip in ip_addresses:
    router = {
        'device_type': 'hp_comware',
        'ip': ip,
        'username': "admin",
        'password': "ckoi7galer",
        'read_timeout': 5,  # Set a larger read timeout value
    }
    routers.append(router)

# Display the list of routers
for router in routers:
    

    try: 

# Iterate through the routers and configure ACLs

    # Establish an SSH connection to the device
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username="admin", password="ckoi7galer")
        ssh_shell = ssh_client.invoke_shell()
    # Enter configuration mode
        ssh_shell.send("system-view\n")
        time.sleep(1)
    # Add permit statement to ACL source_ip
        ssh_shell.send("acl number 3256 name VoIP_interne_autres_VLAN\n")
        time.sleep(1)
        ssh_shell.send(f"rule 15 permit ip destination 10.107.144.160 0.0.0.7 \n")
        time.sleep(1)
        ssh_shell.send(f" rule 16 permit ip destination 10.107.144.168 0 \n")
        time.sleep(1)
        ssh_shell.send(f"rule 17 permit ip destination 10.107.144.169 0 \n")
        time.sleep(1)
        ssh_shell.send(f"rule 18 permit ip destination 10.107.144.170 0 \n")
        time.sleep(1)
        ssh_shell.send(f"rrrrule 19 permit ip destination 10.8.83.192 0.0.0.63 \n")
        time.sleep(1)
        ssh_shell.send(f"interface GigabitEthernet1/2/0/5 \n")
        time.sleep(1)
        ssh_shell.send(f"port link-mode bridge \n")
        time.sleep(1)
        ssh_shell.send(f" packet-filter 3256 inbound \n")
        time.sleep(1)
   
        ssh_shell.send(f"quit\n")
        time.sleep(2)
        ssh_shell.send(f"save\n")
        time.sleep(2)
        ssh_shell.send(f"yes\n")
        time.sleep(3)
        ssh_shell.send(f"\n")
        time.sleep(3)
        ssh_shell.send(f"yes\n")
        time.sleep(12)          
        # Capture the output of the commands

    except ConfigurationError as conf_err:
        print(conf_err)
        break  # Stop execution for this device

    except Exception as ex:
        print(f"An error occurred for {ip}: {ex}")
        break 
   
