from netmiko import ConnectHandler
import paramiko
import time

num_routers = int(input("Enter the number of routers: "))

acl_number = int(input("Enter le numéro d'acl: "))
source_ip = '192.168.2.0'
wildcard_mask = '0.0.0.255'
for i in range(num_routers):
    router_ip = input(f"Enter the IP address for router {i+1}: ")
    username = input(f"Enter the username for router {i+1}: ")
    password = input(f"Enter the password for router {i+1}: ")
    
    # Create a dictionary with the device parameters
    device = {
        'device_type': 'hp_comware',
        'ip': router_ip,
        'username': username,
        'password': password,
    }
    # Establish an SSH connection to the device
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(router_ip, username=username, password=password)
    ssh_shell = ssh_client.invoke_shell()
    # Enter configuration mode
    ssh_shell.send("system-view\n")
    time.sleep(1)
    # Create ACL
    ssh_shell.send(f"Acl number acl_number\n")
    time.sleep(1)
    # Add permit statement to ACL source_ip
    ssh_shell.send(f"rule 10 permit \n")

    ssh_shell.send(f"permit ip {source_ip} any\n")

    ssh_shell.send(f"quit\n")
    ssh_shell.send(f"yes\n")
    ssh_shell.send(f"yes\n")

    time.sleep(1)
    # Apply ACL to an interface (modify as per your requirements)
    # ssh_shell.send("interface GigabitEthernet 1/0/1\n")
    # time.sleep(1)
    # ssh_shell.send(f"ip access-group ACL_{acl_number} in\n")
    # time.sleep(1)
    # Exit configuration mode
    # ssh_shell.send("end\n")
    # time.sleep(1)
    # print(f"ACL configuration completed for router {device['ip']}")

    # Disconnect from the router
    # ssh_shell.send("write memory\n")
    # time.sleep(2)
    # Add your code here to configure ACL on the router using the provided information
    
    # Disconnect from the device
    ssh_client.close()
