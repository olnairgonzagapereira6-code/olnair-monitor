import subprocess
import json
import time
import re

def limpar_texto(texto):
    return re.sub(r'[^\w\s,?.!]', '', str(texto))

print("🛡️ Robô Leitor Ativado!")
print("Dica: Se ele disser 'Nova mensagem', verifique se a prévia está ativa no WhatsApp.")

def carregar_mensagens_atuais():
    try:
        res = subprocess.check_output(["termux-notification-list"], stderr=subprocess.DEVNULL)
        notifs = json.loads(res)
        return {f"{n.get('title')}_{n.get('content')}" for n in notifs if n.get('packageName') in ['com.whatsapp', 'com.whatsapp.w4b']}
    except:
        return set()

mensagens_lidas = carregar_mensagens_atuais()

while True:
    try:
        resultado = subprocess.check_output(["termux-notification-list"], stderr=subprocess.DEVNULL)
        if not resultado:
            continue
            
        notificacoes = json.loads(resultado)

        for n in notificacoes:
            pacote = n.get('packageName', '')
            if pacote in ['com.whatsapp', 'com.whatsapp.w4b']:
                quem = n.get('title', 'Alguém')
                # Tenta pegar o conteúdo de várias formas possíveis
                o_que = n.get('content') or n.get('text') or ""
                
                msg_id = f"{quem}_{o_que}"
                
                if msg_id not in mensagens_lidas:
                    quem_limpo = limpar_texto(quem)
                    o_que_limpo = limpar_texto(o_que)
                    
                    # Se o conteúdo for apenas "WhatsApp" ou "Nova mensagem", ele tenta ignorar ou avisar
                    if "mensagem" in o_que_limpo.lower() and len(o_que_limpo) < 20:
                         frase = f"Olnair, nova mensagem de {quem_limpo}."
                    else:
                         frase = f"Olnair, {quem_limpo} enviou: {o_que_limpo}"
                    
                    print(f"✅ Lendo de {quem_limpo}: {o_que_limpo}")
                    subprocess.run(["termux-tts-speak", frase])
                    
                    mensagens_lidas.add(msg_id)
        
        time.sleep(2)
        
    except Exception:
        time.sleep(4)
