from flask import Flask, render_template, request, flash
from netmiko import ConnectHandler
import paramiko

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def run_script(num_ips, ip_addresses, your_username, your_password, nom_de_fichier):
    # The rest of the code remains the same as before
    # ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_ips = int(request.form['num_ips'])
        ip_addresses = request.form['ip_addresses'].split(',')
        your_username = request.form['username']
        your_password = request.form['password']
        nom_de_fichier = request.form['filename']

        try:
            output = run_script(num_ips, ip_addresses, your_username, your_password, nom_de_fichier)
            flash(output)
        except Exception as ex:
            flash(f"An error occurred: {ex}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
