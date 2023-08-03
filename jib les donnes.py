# ... (previous code)

for router in routers:
    print(router)

    try:
        # Establish an SSH connection to the device
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(ip, username=your_username, password=your_password)
        ssh_shell = ssh_client.invoke_shell()

        # Enter configuration mode
        ssh_shell.send("system-view\n")
        time.sleep(1)

        # Add permit statements to ACL source_ip
        ssh_shell.send("acl number 3256 name VoIP_interne_autres_VLAN\n")
        time.sleep(1)

        # ... (previous code)

        ssh_shell.send(f"rrrrule 19 permit ip destination 10.8.83.192 0.0.0.63 \n")
        time.sleep(1)

        # ... (previous code)

        # Wait for the command execution to finish (adjust the time.sleep() value if needed)
        time.sleep(2)

        # Capture the output of the commands
        output = ""
        while ssh_shell.recv_ready():
            output += ssh_shell.recv(4096).decode("utf-8")

        # Print the output
        print(output)

        # Disconnect from the device after configuring ACL, even if an error occurred
        ssh_client.close()

    except paramiko.ssh_exception.SSHException as ssh_ex:
        print(f"SSH Error occurred for {ip}: {ssh_ex}")
        break  # Stop execution for this device

    except Exception as ex:
        print(f"An error occurred for {ip}: {ex}")
        break  # Stop execution for this device
