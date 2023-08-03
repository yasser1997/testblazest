from netmiko import ConnectHandler
import paramiko
import time

# Create an empty list
ip_addresses = []

# Get the number of IP addresses to add
num_ips = int(input("Entrez le nombre d'adresses IP : "))

# Add IP addresses to the list using a for loop
for i in range(num_ips):
    ip = input("Entrez l'adresse IP: ")
    ip_addresses.append(ip)

# Display the list of IP addresses
print(ip_addresses)
your_username = input("Entrez username: ")
your_password = input("Entrez password: ")
routers = []
nom_de_fichier = input("Enter nom de fichier: ")
with open(nom_de_fichier, 'r') as config_file:
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
       
        # Check if the output contains an unrecognized command error message
        if "Unrecognized command found at '^' position." in output:
            # Extract the error message and the line with the unrecognized command
         with open(f'error{router[ip]}.txt', 'a') as error_file:

            error_message = output.split("Unrecognized command found at '^' position.")[0]

            error_line = output.split("Unrecognized command found at '^' position.")[1].splitlines()[0]

            print(f"Erreur alert! On {router['ip']}: vous trouvez les erreurs dans le fichier {router['ip']}.txt")

            # Save the error message and line to "erreur.txt" file along with the device IP
           # with open(f'error{router["ip"]}.txt', 'a') as error_file:

            error_file.write(f"Device IP: {router['ip']} - {error_message.strip()} \n{error_line}\n")

            with open(f'{router["ip"]}.txt', 'w') as config_file:

                config_file.write(output)
        else:
                  
            print("La configuration a été appliquée avec succès")
        ssh_client.save_config()

        # Save the configuration to a file with the IP address as the filename
        ssh_client.disconnect()


    except paramiko.ssh_exception.SSHException as ssh_ex:
        print(f"Uh-oh! SSH Error on {router['ip']}: {ssh_ex}")
        continue  # Keep on truckin' to the next device


   
   
