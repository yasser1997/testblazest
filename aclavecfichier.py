from netmiko import ConnectHandler
import paramiko
import time

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
with open('config2.txt', 'r') as config_file:
    config_commands = config_file.read().strip()

for ip in ip_addresses:
    router = {
        'device_type': 'hp_comware',
        'ip': ip,
        'username': your_username,
        'password': your_password,
        #'read_timeout': 5,  # Set a larger read timeout value
    }
    routers.append(router)

# Display the list of routers
for router in routers:    
    try:
        ssh_client = ConnectHandler(**router)
    # Transfer the configuration from the specified file
        output = ssh_client.send_config_set(config_commands, cmd_verify=True)
        print("Configuration applied successfully:")
       
        ssh_client.save_config()
        # Save the configuration to a file with the IP address as the filename
        with open(f'{ip}.txt', 'w') as config_file:
            config_file.write(output)


    except paramiko.ssh_exception.SSHException as ssh_ex:
        print(f"Uh-oh! SSH Error on {ip}: {ssh_ex}")
        continue  # Keep on truckin' to the next device

        
    except ValueError as value_err:
        # Extract the command causing the error from the ValueError message
        error_command = str(value_err).split(":")[0]
        print(f"Error alert! On {ip}: Unrecognized command: {error_command}")
        error_message = f"Unrecognized command: {error_command}"
        if "Unrecognized command found at '^' position." in output:
            # Extract the error message and the line with the unrecognized command
            error_message = output.split("Unrecognized command found at '^' position.")[0]
            error_line = output.split("Unrecognized command found at '^' position.")[1].splitlines()[0]
            print(f"Error alert! On {router['ip']}: {error_message.strip()} \n{error_line}")
            # Save the error message and line to "erreur.txt" file along with the device IP
            with open('erreur.txt', 'a') as error_file:
                error_file.write(f"Device IP: {router['ip']} - {error_message.strip()} \n{error_line}\n")

        else:
            print(f"Oopsie-daisy! An error on {router['ip']}: {ex}")

        print(f"Error alert! On {router['ip']}: {error_message}")
        # Save the error message to "erreur.txt" file along with the device IP
        with open('erreur.txt', 'a') as error_file:
            error_file.write(f"Device IP: {router['ip']} - {error_message}\n")
        
        continue  # Onward to the next device


   
