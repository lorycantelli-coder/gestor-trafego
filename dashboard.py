"""
Dashboard Meta Ads - Professional
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from meta_ads_api import MetaAdsAPI

# ======================== CONFIG ========================
st.set_page_config(
    page_title="Meta Ads Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== ESTILO ========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif !important; }

    .stApp { background-color: #ffffff; }

    .metric-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    .metric-label {
        color: #64748b;
        font-size: 0.813rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #1e293b;
        font-size: 1.875rem;
        font-weight: 700;
        line-height: 1.2;
    }

    h1 {
        color: #0f172a !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        color: #1e293b !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid #e2e8f0 !important;
        padding-bottom: 0.75rem !important;
    }

    .subtitle {
        color: #64748b !important;
        font-size: 0.95rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================== HEADER ========================
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Dashboard Meta Ads")
    st.markdown('<p class="subtitle">Campanhas [VENDA] • Performance em Tempo Real</p>', unsafe_allow_html=True)

# ======================== SIDEBAR ========================
with st.sidebar:
    st.markdown("### ⚙️ Filtros")

    period_label = st.selectbox(
        "Período:",
        ["7 dias", "15 dias", "30 dias", "60 dias", "90 dias"],
        index=2
    )

    period_map = {
        "7 dias": 7,
        "15 dias": 15,
        "30 dias": 30,
        "60 dias": 60,
        "90 dias": 90
    }
    days = period_map[period_label]

    if st.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("### 📈 Status")
    st.write(f"**Última atualização:**")
    st.write(f"`{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}`")

# ======================== CARREGAR DADOS ========================
@st.cache_data(ttl=300)
def load_data(days):
    try:
        api = MetaAdsAPI()
        campaigns_raw = api.get_campaigns(name_filter="[VENDA]")

        if not campaigns_raw:
            return None, None, None

        campaigns = [dict(c) for c in campaigns_raw]
        insights_raw = api.get_sales_campaign_insights(days=days)
        insights = [dict(i) for i in insights_raw]
        summary = api.get_sales_summary(days=days)

        return summary, insights, campaigns
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        return None, None, None

with st.spinner("⏳ Carregando dados..."):
    summary, insights, campaigns = load_data(days)

if summary is None:
    st.warning("⚠️ Sem dados disponíveis")
    st.stop()

# ======================== MÉTRICAS PRINCIPAIS ========================
st.markdown("## 📊 Resumo de Performance")

metrics_data = [
    ("💰 Gasto Total", f"R$ {summary.get('spend', 0):,.2f}", "#3b82f6"),
    ("👁️ Impressões", f"{summary.get('impressions', 0):,}", "#06b6d4"),
    ("🖱️ Cliques", f"{summary.get('clicks', 0):,}", "#8b5cf6"),
    ("📊 CTR", f"{summary.get('ctr', 0)*100:.2f}%", "#ec4899"),
    ("💵 CPC", f"R$ {summary.get('cpc', 0):.2f}", "#f59e0b"),
    ("✅ Conversões", f"{summary.get('conversions', 0):,}", "#10b981"),
    ("🎯 CPL", f"R$ {summary.get('cpl', 0):.2f}", "#06b6d4"),
    ("📈 ROAS", f"{summary.get('roas', 0):.2f}x", "#8b5cf6"),
]

cols = st.columns(4)
for idx, (label, value, color) in enumerate(metrics_data):
    with cols[idx % 4]:
        st.markdown(f"""
        <div class="metric-box" style="border-left-color: {color};">
            <div class="metric-label">{label.split(' ', 1)[1]}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ======================== GRÁFICOS ========================
st.markdown("## 📈 Análise Temporal")

if insights:
    df_insights = pd.DataFrame(insights)

    col1, col2 = st.columns(2)

    # Gráfico Gasto
    with col1:
        if 'date' in df_insights.columns and 'spend' in df_insights.columns:
            fig_spend = go.Figure()
            fig_spend.add_trace(go.Bar(
                x=df_insights['date'],
                y=df_insights['spend'],
                marker=dict(color='#3b82f6', line=dict(width=0)),
                hovertemplate='<b>%{x}</b><br>Gasto: R$ %{y:.2f}<extra></extra>'
            ))
            fig_spend.update_layout(
                title='<b>Gasto Diário</b>',
                xaxis_title='',
                yaxis_title='R$',
                height=400,
                template='plotly_white',
                showlegend=False,
                margin=dict(l=0, r=0, t=40, b=0),
                hovermode='x unified'
            )
            st.plotly_chart(fig_spend, use_container_width=True)

    # Gráfico Conversões
    with col2:
        if 'date' in df_insights.columns and 'conversions' in df_insights.columns:
            fig_conv = go.Figure()
            fig_conv.add_trace(go.Bar(
                x=df_insights['date'],
                y=df_insights['conversions'],
                marker=dict(color='#10b981', line=dict(width=0)),
                hovertemplate='<b>%{x}</b><br>Conversões: %{y}<extra></extra>'
            ))
            fig_conv.update_layout(
                title='<b>Conversões Diárias</b>',
                xaxis_title='',
                yaxis_title='Qtd',
                height=400,
                template='plotly_white',
                showlegend=False,
                margin=dict(l=0, r=0, t=40, b=0),
                hovermode='x unified'
            )
            st.plotly_chart(fig_conv, use_container_width=True)

# ======================== TABELA CAMPANHAS ========================
st.markdown("## 🎯 Campanhas Ativas")

if campaigns:
    df_campaigns = pd.DataFrame(campaigns)

    display_cols = ['name', 'spend', 'impressions', 'clicks']
    if all(col in df_campaigns.columns for col in display_cols):
        df_display = df_campaigns[display_cols].copy()
        df_display.columns = ['Campanha', 'Gasto', 'Impressões', 'Cliques']
        df_display['Gasto'] = df_display['Gasto'].apply(lambda x: f"R$ {float(x):,.2f}")
        df_display['Impressões'] = df_display['Impressões'].apply(lambda x: f"{int(float(x)):,}")
        df_display['Cliques'] = df_display['Cliques'].apply(lambda x: f"{int(float(x)):,}")

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            height=400
        )

# ======================== FOOTER ========================
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #94a3b8; font-size: 0.85rem;'>"
    f"Dashboard Meta Ads • Período: {period_label} • "
    f"Atualizado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}"
    f"</p>",
    unsafe_allow_html=True
)
