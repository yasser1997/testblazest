import paramiko
import time

# Configuration details
router_ip = '192.168.1.1'
username = 'admin'
password = 'password'
nat_mappings = {}

def add_nat_mapping():
    private_ip = input("Enter the private IP address: ")
    public_ip = input("Enter the public IP address: ")
    nat_mappings[private_ip] = public_ip

def configure_static_nat(nat_mappings):
    # Connect to the router
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(router_ip, username=username, password=password)
    ssh_shell = ssh_client.invoke_shell()
    
    # Enter configuration mode
    ssh_shell.send("configure terminal\n")
    time.sleep(1)

    # Configure Static NAT mappings
    for private_ip, public_ip in nat_mappings.items():
        config_command = f"ip nat inside source static {private_ip} {public_ip}\n"
        ssh_shell.send(config_command)
        time.sleep(1)

    # Exit configuration mode
    ssh_shell.send("end\n")
    time.sleep(1)

    # Save the configuration
    ssh_shell.send("copy running-config startup-config\n")
    time.sleep(2)

    # Close the SSH connection
    ssh_client.close()

# Interactive NAT mapping input
add_more = True
while add_more:
    add_nat_mapping()
    answer = input("Add another NAT mapping? (y/n): ")
    if answer.lower() != 'y':
        add_more = False

# Execute the script
configure_static_nat(nat_mappings)
