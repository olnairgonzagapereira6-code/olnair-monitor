# Olnair Monitor v1.0 🚀

Um monitor de sistema leve e eficiente desenvolvido para rodar no **Termux** (Android). Este projeto nasceu da necessidade de monitorar status vitais do dispositivo contornando limitações do sistema operacional.

## 📊 Funcionalidades
* Monitoramento de **Bateria** (Nível e Status).
* Monitoramento de **Temperatura** em tempo real.
* Verificação de conexão **Wi-Fi**.
* Interface Web moderna e responsiva.

## 🛠️ Como instalar e usar

Para clonar e rodar este projeto, você precisará do Termux instalado com o Python e as Termux-API.

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/olnairgonzagapereira6-code/olnair-monitor.git
   cd olnair-monitor
   ```

2. **Instale as dependências:**
   ```bash
   pkg install termux-api
   pip install flask
   ```

3. **Inicie o monitor:**
   ```bash
   python monitor.py
   ```

4. **Acesse no navegador:**
   Abra `http://127.0.0.1:5000` no seu celular.

---
Desenvolvido por **Olnair Gonzaga Pereira**.
