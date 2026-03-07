"""
Dashboard de Performance - Meta Ads
Design: Dark Mode Premium Refinado
Fundo Preto + Letras Brancas + Anúncios Visíveis
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from meta_ads_api import MetaAdsAPI

# ============================================
# CONFIGURAÇÃO
# ============================================
st.set_page_config(
    page_title="Dashboard Meta Ads | Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS DARK MODE PREMIUM REFINADO
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Fundo preto premium */
    .stApp {
        background-color: #0a0e27;
    }

    .main .block-container {
        padding: 2.5rem 3rem;
        max-width: 1600px;
        background-color: #0a0e27;
    }

    /* Títulos elegantes */
    h1 {
        color: #ffffff;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.8px;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        color: #ffffff;
        font-size: 1.35rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #60a5fa;
    }

    h3 {
        color: #e5e7eb;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    p, span, div, label {
        color: #d1d5db !important;
    }

    /* Cards de métricas limpos */
    [data-testid="stMetric"] {
        background: transparent;
        padding: 1.25rem;
        border-radius: 0;
        border: none;
        box-shadow: none;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        line-height: 1.2;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #a0aec0 !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 0.5rem !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }

    /* Abas minimalistas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border: none;
        padding: 0;
        border-bottom: none;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0;
        font-size: 0.9rem;
        font-weight: 500;
        color: #9ca3af;
        background-color: transparent;
        border: none;
        transition: all 0.2s;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #60a5fa;
        border: none;
    }

    .stTabs [data-baseweb="tab-panel"] {
        background-color: transparent;
        padding: 1.5rem 0;
        border: none;
        box-shadow: none;
    }

    /* Sidebar dark premium */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: #d1d5db !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        width: 100%;
        border-radius: 8px;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
        border-radius: 8px;
    }

    /* Divisores */
    hr {
        border: none;
        height: 1px;
        background-color: #334155;
        margin: 2rem 0;
    }

    /* Tabelas premium */
    [data-testid="stDataFrame"] {
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
        background-color: #0f172a;
    }

    [data-testid="stDataFrame"] tbody {
        background-color: #0f172a;
    }

    [data-testid="stDataFrame"] tr {
        border-bottom: 1px solid #1e293b;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #60a5fa;
        background-color: #0f172a;
        color: #d1d5db;
    }

    /* Subtitle */
    .subtitle {
        color: #9ca3af;
        font-size: 1rem;
        font-weight: 400;
    }

    /* Card container */
    .card-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER MINIMALISTA
# ============================================
st.markdown("<h1 style='margin-bottom: 0.2rem;'>📊 Meta Ads Performance</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle' style='margin-bottom: 2rem;'>Campanhas [VENDA]</p>", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
st.sidebar.markdown("### ⚙️ Configurações")
st.sidebar.markdown("")

period = st.sidebar.selectbox(
    "Período",
    ["Últimos 7 dias", "Últimos 15 dias", "Últimos 30 dias", "Últimos 60 dias", "Últimos 90 dias"],
    index=2
)

period_map = {
    "Últimos 7 dias": 7,
    "Últimos 15 dias": 15,
    "Últimos 30 dias": 30,
    "Últimos 60 dias": 60,
    "Últimos 90 dias": 90
}
days = period_map[period]

st.sidebar.markdown("")

if st.sidebar.button("🔄 Atualizar"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Período**\n{period}")
st.sidebar.markdown(f"**Última Atualização**\n{datetime.now().strftime('%H:%M:%S')}")

# ============================================
# CARREGAR DADOS
# ============================================
@st.cache_data(ttl=300)
def load_sales_data(days):
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

with st.spinner("⏳ Carregando..."):
    summary, insights, campaigns = load_sales_data(days)

if summary is None:
    st.warning("⚠️ Sem dados disponíveis")
    st.stop()

# ============================================
# ABAS
# ============================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎯 Conversão",
    "📊 Distribuição",
    "🔥 Aquecimento",
    "📢 Anúncios",
    "🎓 Aulas"
])

# ============================================
# ABA 1: CONVERSÃO
# ============================================
with tab1:
    st.markdown("## Conversões & ROI")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Investimento", f"R$ {summary['total_spend']:,.2f}")

    with col2:
        st.metric("Receita", f"R$ {summary['total_revenue']:,.2f}")

    with col3:
        lucro = summary['total_revenue'] - summary['total_spend']
        st.metric("Lucro", f"R$ {lucro:,.2f}")

    with col4:
        st.metric("ROAS", f"{summary['roas']:.2f}x", delta="✓ Positivo" if summary['roas'] > 1 else "⚠ Atenção")

    st.markdown("---")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric("Visualizações", f"{summary['total_landing_page_views']:,}".replace(',', '.'))
    with col2:
        st.metric("Custo/Viz", f"R$ {summary['cost_per_landing_page_view']:.2f}")
    with col3:
        st.metric("Checkout", f"{summary['total_initiate_checkout']:,}".replace(',', '.'))
    with col4:
        st.metric("Custo/Checkout", f"R$ {summary['cost_per_initiate_checkout']:.2f}")
    with col5:
        st.metric("Compras", f"{summary['total_purchases']:,}".replace(',', '.'))
    with col6:
        st.metric("Custo/Compra", f"R$ {summary['cost_per_purchase']:.2f}")

    st.markdown("---")

    if insights:
        df_insights = pd.DataFrame([
            {'data': i.get('date_start'), 'gasto': float(i.get('spend', 0))}
            for i in insights
        ])

        df_daily = df_insights.groupby('data').agg({'gasto': 'sum'}).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_daily['data'],
            y=df_daily['gasto'],
            marker_color='#60a5fa'
        ))

        fig.update_layout(
            title='Investimento Diário',
            xaxis_title='Data',
            yaxis_title='R$',
            height=400,
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#d1d5db')
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================
# ABA 2: DISTRIBUIÇÃO
# ============================================
with tab2:
    st.markdown("## Distribuição por Campanha")

    if insights:
        df_insights = pd.DataFrame([
            {'campanha': i.get('campaign_name', 'N/A'), 'gasto': float(i.get('spend', 0))}
            for i in insights
        ])

        df_camps = df_insights.groupby('campanha').agg({'gasto': 'sum'}).reset_index().sort_values('gasto', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_camps['campanha'],
            x=df_camps['gasto'],
            orientation='h',
            marker_color='#60a5fa',
            text=df_camps['gasto'].apply(lambda x: f'R$ {x:,.0f}'),
            textposition='outside'
        ))

        fig.update_layout(
            title='Gasto por Campanha',
            xaxis_title='Investimento (R$)',
            height=max(400, len(df_camps) * 40),
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter', color='#d1d5db')
        )

        st.plotly_chart(fig, use_container_width=True)

# ============================================
# ABA 3: AQUECIMENTO
# ============================================
with tab3:
    st.markdown("## Topo de Funil")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Alcance", f"{summary['total_reach']:,}".replace(',', '.'))
    with col2:
        st.metric("Impressões", f"{summary['total_impressions']:,}".replace(',', '.'))
    with col3:
        st.metric("Frequência", f"{summary['avg_frequency']:.2f}")
    with col4:
        st.metric("CTR", f"{summary['avg_ctr']:.2f}%")

    st.markdown("")

    col5, col6 = st.columns(2)
    with col5:
        st.metric("CPC", f"R$ {summary['avg_cpc']:.2f}")
    with col6:
        cpm = (summary['total_spend'] / summary['total_impressions'] * 1000) if summary['total_impressions'] > 0 else 0
        st.metric("CPM", f"R$ {cpm:.2f}")

    st.markdown("---")

    if insights:
        df_insights = pd.DataFrame([
            {
                'data': i.get('date_start'),
                'alcance': int(i.get('reach', 0)),
                'impressoes': int(i.get('impressions', 0)),
            }
            for i in insights
        ])

        df_daily = df_insights.groupby('data').agg({'alcance': 'sum', 'impressoes': 'sum'}).reset_index()

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(
                x=df_daily['data'],
                y=df_daily['alcance'],
                fill='tozeroy',
                line=dict(color='#60a5fa', width=2),
                marker=dict(size=6)
            ))

            fig1.update_layout(
                title='Alcance Diário',
                height=350,
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#d1d5db')
            )

            st.plotly_chart(fig1, use_container_width=True)

        with col_g2:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df_daily['data'],
                y=df_daily['impressoes'],
                fill='tozeroy',
                line=dict(color='#10b981', width=2),
                marker=dict(size=6)
            ))

            fig2.update_layout(
                title='Impressões Diárias',
                height=350,
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#d1d5db')
            )

            st.plotly_chart(fig2, use_container_width=True)

# ============================================
# ABA 4: ANÚNCIOS (NOVO!)
# ============================================
with tab4:
    st.markdown("## Anúncios Ativos")

    if insights:
        # Preparar dados de anúncios
        ads_data = []
        for insight in insights:
            ads_data.append({
                'Campanha': insight.get('campaign_name', 'N/A'),
                'Data': insight.get('date_start', ''),
                'Impressões': int(insight.get('impressions', 0)),
                'Cliques': int(insight.get('clicks', 0)) if 'clicks' in insight else 0,
                'CTR': f"{float(insight.get('ctr', 0)):.2f}%",
                'CPC': f"R$ {float(insight.get('cpc', 0)):.2f}",
                'Gasto': f"R$ {float(insight.get('spend', 0)):,.2f}"
            })

        df_ads = pd.DataFrame(ads_data)

        # Agrupar por campanha (mostrar últimas ocorrências)
        if not df_ads.empty:
            df_ads_latest = df_ads.sort_values('Data', ascending=False).drop_duplicates('Campanha')

            st.markdown("### Performance de Anúncios por Campanha")
            st.dataframe(df_ads_latest, use_container_width=True, hide_index=True)

            st.markdown("---")

            # Gráfico de Top Campanhas
            df_camp_perf = df_ads.groupby('Campanha').agg({
                'Impressões': 'sum',
                'CTR': lambda x: float(x.iloc[0].strip('%'))
            }).reset_index().sort_values('Impressões', ascending=False).head(5)

            fig_ads = px.bar(
                df_camp_perf,
                x='Campanha',
                y='Impressões',
                title='Top 5 Campanhas por Impressões',
                color='Impressões',
                color_continuous_scale=['#60a5fa', '#3b82f6']
            )

            fig_ads.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family='Inter', color='#d1d5db'),
                height=400
            )

            st.plotly_chart(fig_ads, use_container_width=True)
        else:
            st.info("ℹ️ Nenhum dado de anúncios disponível")
    else:
        st.info("ℹ️ Carregando dados de anúncios...")

# ============================================
# ABA 5: AULAS AO VIVO
# ============================================
with tab5:
    st.markdown("## Campanhas de Aulas ao Vivo")

    aulas = [c for c in campaigns if 'AULA' in c.get('name', '').upper() or 'LIVE' in c.get('name', '').upper()]

    if aulas:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Ativas", len([c for c in aulas if c.get('status') == 'ACTIVE']))
        with col2:
            st.metric("Pausadas", len([c for c in aulas if c.get('status') == 'PAUSED']))
        with col3:
            budget = sum(float(c.get('daily_budget', 0))/100 for c in aulas if c.get('daily_budget'))
            st.metric("Orçamento/Dia", f"R$ {budget:.2f}")

        st.markdown("---")

        df_aulas = pd.DataFrame([
            {
                'Campanha': c.get('name'),
                'Status': '🟢 Ativa' if c.get('status') == 'ACTIVE' else '⏸️ Pausada',
                'Objetivo': c.get('objective', 'N/A')
            }
            for c in aulas
        ])

        st.dataframe(df_aulas, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Sem campanhas de aulas ao vivo")

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: #6b7280; font-size: 0.85rem;'>Última atualização: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')} • Dark Mode Premium v2.0</p>", unsafe_allow_html=True)
