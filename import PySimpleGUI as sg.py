import PySimpleGUI as sg()
from netmiko import ConnectHandler

# Create the window
layout = [[sg.Text("Enter IP address:")],
          [sg.Input(key="-IP-")],
          [sg.Button("Connect"), sg.Button("Exit")],
          [sg.Output(size=(60, 10))]]

window = sg.Window("Netmiko Script", layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    # Connect to the device
    device = {
        "device_type": "cisco_ios",
        "ip": values["-IP-"],
        "username": "admin",
        "password": "password",
    }

    with ConnectHandler(**device) as conn:
        output = conn.send_command("show ip interface brief")
        print(output)

window.close()
