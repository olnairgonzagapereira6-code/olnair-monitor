from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
import subprocess
import os
from datetime import datetime

app = Flask(__name__)
# Usando o caminho que o Termux mapeia internamente para garantir
DOWNLOAD_PATH = os.path.expanduser("~/storage/downloads")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gravador Master</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; background: #0f0f0f; color: #e0e0e0; text-align: center; padding: 20px; }
        .card { background: #1a1a1a; border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 450px; margin: auto; }
        h1 { color: #ff4b4b; }
        .btn-record { background: linear-gradient(45deg, #ff4b4b, #ff8080); color: white; width: 95%; padding: 15px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; margin: 10px 0; }
        .btn-stop { background: #444; color: white; width: 95%; padding: 15px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; }
        input { width: 90%; padding: 12px; margin: 8px 0; border-radius: 8px; border: 1px solid #333; background: #252525; color: white; }
        .file-list { margin-top: 20px; text-align: left; background: #1a1a1a; padding: 15px; border-radius: 15px; border-left: 5px solid #ff4b4b; max-width: 450px; margin: auto; }
        .file-item { border-bottom: 1px solid #333; padding: 15px 0; }
        audio { width: 100%; height: 35px; margin-top: 10px; filter: invert(100%) hue-rotate(180deg); }
        .error-msg { color: #ffeb3b; background: #443a00; padding: 10px; border-radius: 5px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🎙️ Gravador do Olnair</h1>
        <form action="/record" method="post">
            <input type="text" name="filename" value="web_{{ time }}">
            <input type="number" name="duration" value="10">
            <button type="submit" class="btn-record">🔴 INICIAR GRAVAÇÃO</button>
        </form>
        <form action="/stop" method="post">
            <button type="submit" class="btn-stop">⏹️ PARAR TUDO</button>
        </form>
    </div>

    <div class="file-list">
        <h3 style="margin-top:0">📂 Suas Gravações:</h3>
        {% if error %}
            <p class="error-msg">⚠️ {{ error }}</p>
        {% endif %}
        {% for file in files %}
            <div class="file-item">
                <strong>🎵 {{ file }}</strong><br>
                <audio controls>
                    <source src="/download/{{ file }}" type="audio/mpeg">
                </audio>
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    files = []
    error = None
    try:
        if os.path.exists(DOWNLOAD_PATH):
            all_files = [f for f in os.listdir(DOWNLOAD_PATH) if f.endswith('.mp3')]
            files = sorted(all_files, key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_PATH, x)), reverse=True)[:5]
        else:
            error = "Pasta não encontrada. Rode 'termux-setup-storage'."
    except PermissionError:
        error = "Permissão negada. Verifique as configurações do Android para o Termux."
    except Exception as e:
        error = f"Erro inesperado: {str(e)}"
        
    return render_template_string(HTML, files=files, time=datetime.now().strftime('%d%m_%H%M'), error=error)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_PATH, filename)

@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('filename', 'audio')
    dur = request.form.get('duration', '10')
    path = os.path.join(DOWNLOAD_PATH, f"{name}.mp3")
    subprocess.Popen(["termux-microphone-record", "-f", path, "-l", str(dur)])
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    subprocess.run(["termux-microphone-record", "-q"])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
