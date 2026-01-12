from flask import Flask, render_template_string, request, redirect, url_for
import os
from datetime import datetime
import subprocess

# Pasta onde os áudios serão salvos
AUDIO_DIR = "/storage/emulated/0/recordings/audios_termux"

# Cria a pasta se não existir
os.makedirs(AUDIO_DIR, exist_ok=True)

app = Flask(__name__)

# HTML da interface
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Controle de Áudio Termux</title>
</head>
<body>
    <h1>Gravar Áudio</h1>
    <form method="POST">
        Duração (segundos): <input type="number" name="duration" value="10" min="1" max="600">
        <button type="submit">Gravar</button>
    </form>
    <h2>Áudios Gravados</h2>
    <ul>
    {% for audio in audios %}
        <li>
            {{ audio }}
            <audio controls>
                <source src="{{ url_for('serve_audio', filename=audio) }}" type="audio/3gp">
                Seu navegador não suporta áudio.
            </audio>
        </li>
    {% else %}
        <li>Nenhum áudio gravado ainda.</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        duration = int(request.form.get("duration", 10))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{timestamp}.3gp"
        filepath = os.path.join(AUDIO_DIR, filename)

        # Comando para gravar áudio via Termux
        subprocess.Popen([
            "termux-microphone-record",
            "-f", filepath,
            "-l", str(duration)
        ])

        return redirect(url_for("index"))

    # Lista todos os arquivos gravados
    audios = sorted(os.listdir(AUDIO_DIR), reverse=True)
    return render_template_string(HTML, audios=audios)

@app.route("/audios/<filename>")
def serve_audio(filename):
    return redirect(f"/storage/emulated/0/recordings/audios_termux/{filename}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
