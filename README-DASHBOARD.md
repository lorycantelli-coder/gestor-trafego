# 📊 Dashboard de Performance - Meta Ads

Dashboard interativo em tempo real para monitorar campanhas do Meta Ads.

## 🚀 Como Acessar

**URL Local:** http://localhost:8501

O dashboard já está rodando em background!

## 📈 O que o Dashboard Mostra

### 1. Métricas Principais (Cards)
- 💰 Gasto Total
- 👁️ Impressões
- 🖱️ Cliques
- 📊 CTR (Taxa de Cliques)
- 💵 CPC (Custo por Clique)
- ✅ Conversões
- 🎯 CPL (Custo por Lead)
- 📈 ROAS Estimado

### 2. Evolução Temporal
- Gráfico de gasto diário
- Gráfico de impressões diárias
- Gráfico de cliques diários

### 3. Comparação entre Campanhas
- Top 5 campanhas por gasto
- Tabela completa com todas as campanhas e métricas

## ⚙️ Filtros Disponíveis

- **Período:** Últimos 7, 15, 30 ou 90 dias
- **Atualização:** Automática a cada 5 minutos
- **Botão de atualização manual**

## 🔧 Comandos Úteis

### Ver se o dashboard está rodando:
```bash
ps aux | grep streamlit | grep dashboard.py
```

### Parar o dashboard:
```bash
pkill -f "streamlit run dashboard.py"
```

### Iniciar o dashboard:
```bash
cd ~/Projetos/gestor-trafego
./venv/bin/streamlit run dashboard.py --server.port 8501
```

### Ver logs em tempo real:
```bash
tail -f /private/tmp/claude-501/-Users-lorycantelli/tasks/b68b0c6.output
```

## 🔐 Credenciais

As credenciais do Meta Ads estão configuradas em:
- `~/.env.meta-ads`

O dashboard carrega automaticamente essas credenciais.

## 📁 Arquivos do Projeto

| Arquivo | Função |
|---------|--------|
| `dashboard.py` | Interface principal do dashboard (Streamlit) |
| `meta_ads_api.py` | Integração com Meta Ads API |
| `requirements.txt` | Dependências Python |
| `.streamlit/config.toml` | Configurações do Streamlit |

## 🎨 Tecnologias

- **Streamlit** - Framework de dashboard
- **Plotly** - Gráficos interativos
- **Pandas** - Processamento de dados
- **Facebook Business SDK** - Integração com Meta Ads API

## 📊 Exemplo de Uso

1. Abra http://localhost:8501 no navegador
2. Selecione o período desejado no sidebar
3. Visualize as métricas em tempo real
4. Use o botão "Atualizar Dados" para forçar atualização
5. Analise os gráficos de evolução temporal
6. Compare performance entre campanhas

## ⚠️ Solução de Problemas

### Dashboard não carrega?
```bash
# Verificar se está rodando
ps aux | grep streamlit

# Reiniciar
pkill -f "streamlit run dashboard.py"
cd ~/Projetos/gestor-trafego
./venv/bin/streamlit run dashboard.py --server.port 8501
```

### Erro de autenticação Meta Ads?
- Verifique se as credenciais em `~/.env.meta-ads` estão corretas
- Confirme que o token não expirou

### Sem dados aparecendo?
- Verifique se há campanhas ativas na conta
- Confirme o período selecionado (pode não haver dados em períodos muito antigos)
- Verifique se o Ad Account ID está correto

## 🔄 Próximas Melhorias

- [ ] Exportar relatório em PDF
- [ ] Alertas de orçamento via WhatsApp
- [ ] Comparação entre períodos
- [ ] Filtro por status de campanha
- [ ] Métricas por conjunto de anúncios
- [ ] Dashboard de criativos (análise de imagens/vídeos)

---

**Dashboard criado em:** 2026-03-06
**Tecnologia:** Streamlit 1.55.0 + Meta Ads API
