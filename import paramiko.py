import paramiko
import time
# Configuration details
router_ip = '192.168.1.1'
username = 'admin'
password = 'password'
x = input("entrer" )
pool_network = '10.110.10."x"'
pool_subnet = '255.255.255.0'
internal_network = '192.168.1."x"/24'
x = input('entre ' )
def configure_dynamic_nat():
    # Connect to the router
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(router_ip, username=username, password=password)
    ssh_shell = ssh_client.invoke_shell()
    # Enter configuration mode
    ssh_shell.send("configure terminal\n")
    time.sleep(1)
    # Configure dynamic NAT
    ssh_shell.send(f"ip nat pool mypool {pool_network} {pool_subnet}\n")
    time.sleep(1)
    ssh_shell.send(f"access-list 1 permit {internal_network}\n")
    time.sleep(1)
    ssh_shell.send("ip nat inside source list 1 pool mypool overload\n")
    time.sleep(1)
    # Exit configuration mode
    ssh_shell.send("end\n")
    time.sleep(1)
    # Save the configuration
    ssh_shell.send("copy running-config startup-config\n")
    time.sleep(2)
    # Close the SSH connection
    ssh_client.close()
# Execute the script
configure_dynamic_nat()
