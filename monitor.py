from flask import Flask, render_template_string
import subprocess
import json
import datetime

app = Flask(__name__)

# Design da página (HTML)
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Olnair Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; }
        .card { background: #1e1e1e; padding: 20px; margin: 20px; border-radius: 15px; border: 1px solid #333; }
        .status-ok { color: #4CAF50; font-weight: bold; }
        .status-alert { color: #f44336; font-weight: bold; }
        h1 { color: #007bff; }
    </style>
</head>
<body>
    <h1>Olnair Monitor v1.0</h1>
    <p>Última atualização: {{ hora }}</p>
    
    <div class="card">
        <h2>🔋 Bateria</h2>
        <p style="font-size: 2em;">{{ bateria }}%</p>
        <p>Status: {{ status_bateria }}</p>
    </div>

    <div class="card">
        <h2>🌡️ Temperatura</h2>
        <p style="font-size: 2em;">{{ temperatura }}°C</p>
    </div>

    <div class="card">
        <h2>🌐 Conexão Wi-Fi</h2>
        <p class="status-ok">{{ wifi }}</p>
    </div>
</body>
</html>
"""

def get_termux_data():
    try:
        # Pega dados da bateria via Termux:API
        res_bat = subprocess.check_output(["termux-battery-status"])
        data = json.loads(res_bat)
        
        # Pega nome do Wi-Fi
        try:
            res_wifi = subprocess.check_output(["termux-wifi-connectioninfo"])
            wifi_data = json.loads(res_wifi)
            wifi_name = wifi_data.get('ssid', 'Desconectado')
        except:
            wifi_name = "Erro ao ler Wi-Fi"
            
        return data, wifi_name
    except:
        return None, "Erro"

@app.route('/')
def home():
    data, wifi = get_termux_data()
    if data:
        return render_template_string(HTML_PAGE, 
            bateria=data['percentage'],
            status_bateria=data['status'],
            temperatura=data['temperature'],
            wifi=wifi,
            hora=datetime.datetime.now().strftime("%H:%M:%S")
        )
    return "Erro ao coletar dados do sistema."

if __name__ == '__main__':
    print("🚀 Monitor Iniciado em http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
