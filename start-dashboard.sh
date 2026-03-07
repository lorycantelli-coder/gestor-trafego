#!/bin/bash
# Script para iniciar o Dashboard de Performance

cd ~/Projetos/gestor-trafego

# Parar instância anterior se houver
pkill -f "streamlit run dashboard.py" 2>/dev/null

echo "🚀 Iniciando Dashboard de Performance..."

# Iniciar dashboard
./venv/bin/streamlit run dashboard.py --server.port 8501 &

sleep 3

echo "✅ Dashboard iniciado!"
echo ""
echo "📊 Acesse: http://localhost:8501"
echo ""
echo "Para parar o dashboard, execute:"
echo "  pkill -f 'streamlit run dashboard.py'"
