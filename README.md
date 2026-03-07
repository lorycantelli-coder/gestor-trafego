# 📊 Gestor de Tráfego - Dashboard Meta Ads

Dashboard interativo em tempo real para monitorar e otimizar campanhas do Meta Ads (Facebook/Instagram).

## ✨ Recursos

- 📊 **Métricas em Tempo Real**: Gasto, impressões, cliques, CTR, CPC, conversões, CPL e ROAS
- 📈 **Gráficos Interativos**: Evolução temporal com Plotly
- 🎯 **Comparação de Campanhas**: Análise comparativa e ranking
- 🔄 **Atualização Automática**: Sincroniza a cada 5 minutos
- 🎨 **Dark Mode Premium**: Interface moderna e elegante
- 📱 **Responsivo**: Funciona em desktop, tablet e mobile

## 🚀 Deploy Rápido

### Opção 1: Streamlit Cloud (Recomendado)

1. **Fork ou clone este repositório**
   ```bash
   git clone https://github.com/seu-usuario/gestor-trafego.git
   cd gestor-trafego
   git push origin main
   ```

2. **Acesse [Streamlit Cloud](https://streamlit.io/cloud)**
   - Clique em "New app"
   - Conecte seu repositório GitHub
   - Selecione `dashboard.py` como main file

3. **Configure os Secrets**
   - Na página de deploy, vá para "Advanced settings"
   - Adicione suas credenciais Meta Ads:
     ```
     META_ACCESS_TOKEN = "seu-token"
     META_AD_ACCOUNT_ID = "seu-account-id"
     META_APP_ID = "seu-app-id"
     ```

4. **Deploy automático!** 🎉
   - URL: `https://seu-usuario-gestor-trafego.streamlit.app`

### Opção 2: Vercel (Com API Backend)

Veja `docs/VERCEL-DEPLOY.md` para instruções detalhadas.

## 💻 Desenvolver Localmente

### Requisitos
- Python 3.8+
- pip ou poetry

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/gestor-trafego.git
cd gestor-trafego

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Instale dependências
pip install -r requirements.txt

# Configure credenciais
cp .streamlit/secrets-example.toml .streamlit/secrets.toml
# Edite .streamlit/secrets.toml com suas credenciais
```

### Rodando o Dashboard

```bash
streamlit run dashboard.py
```

Acesse em: http://localhost:8501

## 🔐 Credenciais Meta Ads

### Obtenha suas credenciais:

1. **Access Token**
   - Vá para [Facebook Developers](https://developers.facebook.com)
   - Crie uma app ou use uma existente
   - Graph API Explorer → Generate Token

2. **Ad Account ID**
   - Meta Ads Manager → Settings
   - Copie o ID da conta de anúncios (formato: 123456789)

3. **App ID**
   - Facebook Developers → Suas Apps → Settings → Basic
   - Copie o App ID

### Salvar credenciais locais (desenvolvimento)

```bash
# Crie ~/.env.meta-ads
echo "META_ACCESS_TOKEN=seu-token" >> ~/.env.meta-ads
echo "META_AD_ACCOUNT_ID=seu-account-id" >> ~/.env.meta-ads
echo "META_APP_ID=seu-app-id" >> ~/.env.meta-ads
```

## 📁 Estrutura do Projeto

```
gestor-trafego/
├── dashboard.py                 # Aplicação principal Streamlit
├── meta_ads_api.py             # Integração com Meta Ads API
├── requirements.txt             # Dependências Python
├── .streamlit/
│   ├── config.toml             # Configurações Streamlit
│   └── secrets-example.toml     # Exemplo de secrets
├── README.md                    # Este arquivo
└── docs/
    └── VERCEL-DEPLOY.md        # Instruções Vercel
```

## 📊 Funcionalidades Detalhadas

### Métricas Principais
- **Gasto Total**: Investimento em campanhas
- **Impressões**: Quantas vezes os anúncios foram vistos
- **Cliques**: Interações com os anúncios
- **CTR**: Taxa de cliques (Cliques / Impressões)
- **CPC**: Custo por clique
- **Conversões**: Ações completadas (compras, leads)
- **CPL**: Custo por lead
- **ROAS**: Retorno sobre investimento em anúncios

### Filtros
- Período: 7, 15, 30 ou 90 dias
- Atualização manual a qualquer momento
- Sincronização automática a cada 5 minutos

### Gráficos
- Evolução de gasto diário
- Evolução de impressões diárias
- Evolução de cliques diários
- Ranking das campanhas por performance

## 🛠️ Tecnologias

- **[Streamlit](https://streamlit.io/)** - Framework web para Python
- **[Plotly](https://plotly.com/)** - Gráficos interativos
- **[Pandas](https://pandas.pydata.org/)** - Processamento de dados
- **[Facebook Business SDK](https://github.com/facebook/facebook-python-business-sdk)** - API Meta Ads

## 📝 Variáveis de Ambiente

### Desenvolvimento (.env.meta-ads ou .streamlit/secrets.toml)
```
META_ACCESS_TOKEN=seu_token_de_acesso
META_AD_ACCOUNT_ID=seu_account_id
META_APP_ID=seu_app_id
```

### Streamlit Cloud
Use a interface de Secrets do Streamlit Cloud

## 🐛 Troubleshooting

### Dashboard não carrega dados?
- Verifique se o token é válido: `curl https://graph.instagram.com/debug_token?input_token=SEU_TOKEN&access_token=SEU_TOKEN`
- Confirme que o account ID está correto
- Verifique se há campanhas ativas na conta

### Erro de autenticação?
- Token expirou: gere um novo em Facebook Developers
- Permissões insuficientes: configure as permissões na app

### Performance lenta?
- Reduza o período de consulta
- Verifique a conexão de internet
- Limite o número de campanhas consultadas

## 📚 Documentação

- [Streamlit Docs](https://docs.streamlit.io/)
- [Meta Ads API Docs](https://developers.facebook.com/docs/marketing-api)
- [Plotly Docs](https://plotly.com/python/)

## 🎯 Roadmap

- [ ] Exportar relatório em PDF
- [ ] Alertas de orçamento via WhatsApp
- [ ] Comparação entre períodos
- [ ] Filtro por status de campanha
- [ ] Métricas por conjunto de anúncios
- [ ] Dashboard de criativos (análise de imagens/vídeos)
- [ ] Previsões com Machine Learning
- [ ] Relatórios agendados por email

## 👨‍💻 Desenvolvimento

### Rodando testes
```bash
# Em desenvolvimento futura
pytest tests/
```

### Linting
```bash
# Em desenvolvimento futura
flake8 .
```

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Add MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📞 Suporte

Encontrou um bug ou tem uma sugestão? Abra uma [issue](https://github.com/seu-usuario/gestor-trafego/issues).

---

**Criado com ❤️ para otimizar campanhas de Meta Ads**

*Última atualização: 2026-03-07*
