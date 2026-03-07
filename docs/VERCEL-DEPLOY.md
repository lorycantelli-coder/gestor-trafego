# 🚀 Deploy no Vercel

Guia para deployar o Dashboard Meta Ads no Vercel com Next.js + API Backend.

## Arquitetura

```
Vercel (Frontend + API Routes)
    ↓
Railway/Render (Backend Python - Meta Ads API)
    ↓
Meta Ads API
```

## Opção A: Apenas Frontend no Vercel + Backend em outro serviço

### Passo 1: Preparar o Backend (Railway ou Render)

#### Railway (Recomendado)

1. Acesse [Railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "GitHub Repo"
4. Conecte seu repositório `gestor-trafego`
5. Configure variáveis de ambiente:
   ```
   META_ACCESS_TOKEN=seu-token
   META_AD_ACCOUNT_ID=seu-account-id
   META_APP_ID=seu-app-id
   PORT=5000
   ```
6. Railway faz deploy automático!
7. Copie a URL do seu backend: `https://seu-app.up.railway.app`

### Passo 2: Frontend no Vercel

1. Acesse [Vercel.com](https://vercel.com)
2. Clique em "New Project"
3. Importe seu repositório GitHub
4. Configure variáveis de ambiente:
   ```
   NEXT_PUBLIC_API_URL=https://seu-app.up.railway.app
   ```
5. Deploy automático! ✅

## Opção B: Next.js API Routes + Streamlit em Docker

### Passo 1: Converter para Next.js

```bash
# Criar projeto Next.js
npx create-next-app@latest gestor-trafego-web

# Instalar dependências
cd gestor-trafego-web
npm install axios chart.js react-chartjs-2
```

### Passo 2: Criar API Routes

Arquivo: `pages/api/campaigns.js`

```javascript
// API proxy para Meta Ads
export default async function handler(req, res) {
  const backendUrl = process.env.NEXT_PUBLIC_API_URL;

  try {
    const response = await fetch(`${backendUrl}/api/campaigns`, {
      headers: {
        'Authorization': `Bearer ${process.env.API_TOKEN}`
      }
    });

    const data = await response.json();
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```

### Passo 3: Deploy no Vercel

1. Acesse Vercel.com
2. Importe projeto Next.js
3. Configure variáveis:
   ```
   NEXT_PUBLIC_API_URL=seu-backend-url
   ```
4. Deploy automático! 🎉

## Opção C: Streamlit Cloud + Next.js no Vercel

### Melhor dos dois mundos!

**Frontend:**
- Vercel (Next.js)
- Performance excelente
- Sem tempo limite

**Backend:**
- Streamlit Cloud
- Deploy automático
- Sem custo extra

### Configuração

1. **Streamlit Cloud**
   - Deploy `dashboard.py`
   - Obtenha URL: `https://seu-app.streamlit.app`

2. **Vercel**
   - Deploy Next.js
   - Variável: `NEXT_PUBLIC_STREAMLIT_URL=https://seu-app.streamlit.app`

3. **Next.js Iframe**
   ```jsx
   export default function DashboardPage() {
     return (
       <iframe
         src={process.env.NEXT_PUBLIC_STREAMLIT_URL}
         style={{
           width: '100%',
           height: '100vh',
           border: 'none'
         }}
       />
     );
   }
   ```

## Variáveis de Ambiente

### .env.local (desenvolvimento)
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### Vercel (production)
```
NEXT_PUBLIC_API_URL=https://seu-backend.up.railway.app
```

## Servicos de Backend Recomendados

| Serviço | Preço | Uptime | Recomendado para |
|---------|-------|--------|-----------------|
| Railway | $5/mês | 99.9% | **Melhor custo-benefício** |
| Render | Grátis | 99.9% | Pequenos projetos |
| Heroku | $7/mês | 99.95% | Aplicações maiores |
| AWS | Variável | 99.99% | Escala grande |

## Comandos Úteis

### Testar API localmente
```bash
# Terminal 1: Backend
cd gestor-trafego
python -m flask run

# Terminal 2: Frontend
cd gestor-trafego-web
npm run dev
```

### Verificar deployment
```bash
# Streamlit Cloud
curl https://seu-app.streamlit.app

# Railway/Render
curl https://seu-backend.up.railway.app/health

# Vercel
curl https://seu-app.vercel.app
```

## Troubleshooting

### API não conecta?
- Verifique CORS no backend
- Confirme variáveis de ambiente
- Teste endpoint diretamente: `curl https://seu-backend.up.railway.app/api/campaigns`

### Vercel timeout?
- Reduza tamanho das requisições
- Implemente paginação
- Use caching de dados

### Dados não atualizam?
- Verifique token Meta Ads
- Aumente intervalo de atualização
- Verificar logs do backend

## Próximos Passos

1. **CI/CD Automático**
   - GitHub Actions
   - Testes automatizados
   - Deploy automático em push

2. **Monitoramento**
   - Sentry para erros
   - DataDog para performance
   - UptimeRobot para alertas

3. **Escalabilidade**
   - Redis para cache
   - Database para histórico
   - CDN para assets

---

**Precisa de ajuda?** Abra uma issue no GitHub!
