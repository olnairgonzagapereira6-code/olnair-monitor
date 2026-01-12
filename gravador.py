import os
import certifi
import subprocess
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from pymongo import MongoClient

# CAMINHO ABSOLUTO PARA O PLAYER NÃO FALHAR
DOWNLOAD_PATH = "/storage/emulated/0/Download"

app = Flask(__name__)

uri = "mongodb://olnairgonzagapereira6_db_user:NXPX4dKglEq0MBqA@cluster0-shard-00-00.d6lswau.mongodb.net:27017,cluster0-shard-00-01.d6lswau.mongodb.net:27017,cluster0-shard-00-02.d6lswau.mongodb.net:27017/?ssl=true&replicaSet=atlas-d6lswau-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=2000)
    db = client.olnair_monitor
    logs_gravacao = db.historico_audios
    client.admin.command('ping')
    status_db = "✅ Online"
except:
    logs_gravacao = None
    status_db = "⚠️ Offline"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Gravador Olnair</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: white; padding: 20px; }
        .btn-record { width: 100%; padding: 20px; font-size: 18px; border-radius: 15px; border: none; background: #ff4b4b; color: white; font-weight: bold; cursor: pointer; }
        .audio-card { background: #222; padding: 15px; border-radius: 15px; margin-top: 20px; border: 1px solid #333; }
        audio { width: 100%; margin-top: 10px; border-radius: 5px; }
        .file-link { display: block; padding: 10px; color: #4caf50; text-decoration: none; border-bottom: 1px solid #333; }
    </style>
</head>
<body>
    <h1>🎙️ Gravador Pro</h1>
    <p>{{ status }}</p>
    
    <form action="/record" method="post">
        <input type="text" name="filename" value="rec_{{ time }}" style="width: 80%; padding: 10px; margin-bottom: 15px;">
        <button type="submit" class="btn-record">🔴 GRAVAR AGORA</button>
    </form>

    <div class="audio-card">
        <h3>🎧 Ouvir Última Gravação</h3>
        {% if last_audio %}
            <p>{{ last_audio }}</p>
            <audio controls preload="none">
                <source src="{{ url_for('ouvir', filename=last_audio) }}" type="audio/mpeg">
                Seu navegador não suporta áudio.
            </audio>
            <br><br>
            <a href="{{ url_for('ouvir', filename=last_audio) }}" download style="color: #aaa; font-size: 12px;">Baixar arquivo</a>
        {% else %}
            <p>Nenhum áudio encontrado.</p>
        {% endif %}
    </div>

    <div style="margin-top: 20px; text-align: left;">
        <h4>📂 Lista de Arquivos:</h4>
        {% for file in files %}
            <a href="{{ url_for('ouvir', filename=file) }}" class="file-link">🎵 {{ file }}</a>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        files = [f for f in os.listdir(DOWNLOAD_PATH) if f.endswith('.mp3')]
        files.sort(reverse=True)
        last_audio = files[0] if files else None
    except:
        files, last_audio = [], None
    return render_template_string(HTML, time=datetime.now().strftime("%H%M%S"), status=status_db, files=files[:5], last_audio=last_audio)

# ROTA ESSENCIAL PARA O PLAYER FUNCIONAR
@app.route('/ouvir/<filename>')
def ouvir(filename):
    return send_from_directory(DOWNLOAD_PATH, filename, as_attachment=False)

@app.route('/record', methods=['POST'])
def record():
    name = request.form.get('filename', 'audio') + ".mp3"
    path = os.path.join(DOWNLOAD_PATH, name)
    subprocess.Popen(["termux-microphone-record", "-f", path, "-l", "10"])
    if logs_gravacao:
        try: logs_gravacao.insert_one({"nome": name, "data": datetime.now()})
        except: pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
