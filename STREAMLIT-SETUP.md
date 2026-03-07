# 🚀 SETUP DO STREAMLIT CLOUD - PASSO A PASSO

## Opção 1: Automático (Copiar e Colar)

### Passo 1: Acesse https://streamlit.io/cloud

### Passo 2: Clique em "New app"

### Passo 3: Conecte seu repositório
- **GitHub repo**: `lorycantelli-coder/gestor-trafego`
- **Branch**: `main`
- **Main file path**: `dashboard.py`
- Clique em "Deploy"

### Passo 4: Aguarde 1-2 minutos
(Streamlit está fazendo download, instalando dependências e iniciando)

### Passo 5: Clique em ⚙️ Settings (canto superior direito)

### Passo 6: Selecione "Secrets" na esquerda

### Passo 7: Cole EXATAMENTE isto no editor:

```toml
META_ACCESS_TOKEN = "EAANNVTMzRiUBQsMPIb8K21NHWOJYv2UOaBIoGeNmCxKPdf8xQJClsMvhzv9jBDiSOt7W3peh7LbHhtianGaNEm2Fd2RIpnZCGJZCLwGYOHWL0uXPSsKoMhcZAIS0KmakXeQOZAbplDGzfUCe7bq3ec0HVsKZBxBPTKrQYihINvyp3wLIZCBL1unTMmbgynfSoJ0QZDZD"
META_AD_ACCOUNT_ID = "188938172932947"
META_APP_ID = "929453256689189"
```

### Passo 8: Clique em "Save"

### Passo 9: Aguarde 30 segundos

### Passo 10: Pronto! 🎉

A app vai recarregar com as credenciais. Se ainda der erro, vamos debugar.

---

## Opção 2: Se tiver dúvida, mande screenshot

Tire screenshot de:
1. Sua tela do Streamlit Cloud
2. O erro que aparece (se houver)
3. Onde você está preso

Aí eu ajudo direto!

---

## Troubleshooting Rápido

**Erro: "Sem dados disponíveis"**
- Normal no primeiro carregamento
- Aguarde mais 1 minuto
- Recarregue F5

**Erro: "Erro de Configuração"**
- Verifique se os Secrets foram salvos
- Confirme que não tem aspas faltando
- Recarregue a página

**Erro: "Erro na API"**
- Pode ser que o token expirou
- Ou a conta de anúncios não tem dados
- Me avise se persistir

---

## Acesso rápido após pronto

- **Local**: http://localhost:8501
- **Produção**: https://gestor-trafego.streamlit.app
- **GitHub**: https://github.com/lorycantelli-coder/gestor-trafego
