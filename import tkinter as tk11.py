import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from netmiko import ConnectHandler
import paramiko

def run_script():
    # Same code as before
    num_ips = int(num_ips_entry.get())
    ip_addresses = ip_addresses_entry.get().split(',')
    your_username = username_entry.get()
    your_password = password_entry.get()
    nom_de_fichier = filename_entry.get()

    routers = []
    with open(nom_de_fichier, 'r') as config_file:
        config_commands = config_file.read().strip()

    for ip in ip_addresses:
        router = {
            'device_type': 'hp_comware',
            'ip': ip.strip(),
            'username': your_username,
            'password': your_password,
        }
        routers.append(router)

    for router in routers:
        try:
            ssh_client = ConnectHandler(**router)
            output = ssh_client.send_config_set(config_commands, cmd_verify=True)

            if "Unrecognized command found at '^' position." in output:
                error_message = output.split("Unrecognized command found at '^' position.")[0]
                error_line = output.split("Unrecognized command found at '^' position.")[1].splitlines()[0]

                messagebox.showerror("Error", f"Error alert! On {router['ip']}: {error_message.strip()} \n{error_line}")
                with open(f'error_{router["ip"]}.txt', 'w') as error_file:
                    error_file.write(f"Device IP: {router['ip']} - {error_message.strip()} \n{error_line}\n")
            else:
                messagebox.showinfo("Success", "La configuration a été appliquée avec succès")

            ssh_client.save_config()
            ssh_client.disconnect()

        except paramiko.ssh_exception.SSHException as ssh_ex:
            messagebox.showerror("SSH Error", f"Uh-oh! SSH Error on {router['ip']}: {ssh_ex}")
        except Exception as ex:
            messagebox.showerror("Error", f"Oopsie-daisy! An error on {router['ip']}: {ex}")

# Create the main application window
root = tk.Tk()
root.title("ACL Automation")

# Apply a themed look
style = ttk.Style()
style.theme_use("vista")  # You can change the theme here, e.g., 'clam', 'alt', 'default', etc.

# Customize the font and background color
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12), fieldbackground="#f0f0f0")
style.configure("TButton", font=("Helvetica", 14), background="#0066cc", foreground="white")

# Rest of the code remains the same
# ...

# Labels and Entry fields
ttk.Label(root, text="Entrez le nombre d'adresses IP:").grid(row=0, column=0, padx=5, pady=5)
num_ips_entry = ttk.Entry(root)
num_ips_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Entrez l'adresse IP (séparer par des virgules):").grid(row=1, column=0, padx=5, pady=5)
ip_addresses_entry = ttk.Entry(root)
ip_addresses_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Entrez username:").grid(row=2, column=0, padx=5, pady=5)
username_entry = ttk.Entry(root)
username_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(root, text="Entrez password :").grid(row=3, column=0, padx=5, pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(root, text="Enter the name of the file:").grid(row=4, column=0, padx=5, pady=5)
filename_entry = ttk.Entry(root)
filename_entry.grid(row=4, column=1, padx=5, pady=5)

# Button
run_button = ttk.Button(root, text="Run Script", command=run_script)
run_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Start the main event loop
root.mainloop()

