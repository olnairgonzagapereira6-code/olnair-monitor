#!/data/data/com.termux/files/usr/bin/bash

# Nível mínimo de bateria (em %)
MIN_BATTERY=20

# Loop infinito (verifica a cada 5 minutos)
while true; do
    # Pega a porcentagem de bateria
    BATTERY=$(termux-battery-status | grep -o '"percentage": [0-9]*' | grep -o '[0-9]*')
    
    echo "Bateria atual: $BATTERY%"

    # Se a bateria estiver abaixo do mínimo
    if [ "$BATTERY" -le "$MIN_BATTERY" ]; then
        termux-toast "⚠️ Bateria baixa: $BATTERY%"
        termux-vibrate -d 2000
    fi

    # Espera 5 minutos (300 segundos)
    sleep 300
done
