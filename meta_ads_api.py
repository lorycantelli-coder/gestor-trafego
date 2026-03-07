"""
Meta Ads API Integration
Busca métricas de campanhas para o dashboard
Foco em campanhas de VENDA com métricas de e-commerce
"""
import os
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from dotenv import load_dotenv
import streamlit as st

# Carregar credenciais em ordem de precedência:
# 1. Streamlit Secrets (Streamlit Cloud)
# 2. .env.meta-ads (Desenvolvimento local)
# 3. Variáveis de ambiente

def get_credential(key):
    """Obtém credencial de múltiplas fontes"""
    # Tentar Streamlit secrets primeiro (Streamlit Cloud)
    if hasattr(st, 'secrets') and key in st.secrets:
        return st.secrets[key]

    # Tentar variáveis de ambiente
    if key in os.environ:
        return os.environ[key]

    # Tentar arquivo .env.meta-ads (desenvolvimento)
    load_dotenv(os.path.expanduser('~/.env.meta-ads'))
    return os.getenv(key)

class MetaAdsAPI:
    def __init__(self):
        self.access_token = get_credential('META_ACCESS_TOKEN')
        self.ad_account_id = f"act_{get_credential('META_AD_ACCOUNT_ID')}"
        self.app_id = get_credential('META_APP_ID')

        # Validar credenciais
        if not self.access_token:
            raise ValueError(
                "❌ META_ACCESS_TOKEN não configurado!\n"
                "Configure nos Secrets do Streamlit Cloud ou em ~/.env.meta-ads"
            )
        if not self.ad_account_id or self.ad_account_id == "act_None":
            raise ValueError(
                "❌ META_AD_ACCOUNT_ID não configurado!\n"
                "Configure nos Secrets do Streamlit Cloud ou em ~/.env.meta-ads"
            )
        if not self.app_id:
            raise ValueError(
                "❌ META_APP_ID não configurado!\n"
                "Configure nos Secrets do Streamlit Cloud ou em ~/.env.meta-ads"
            )

        # Inicializar API
        FacebookAdsApi.init(
            app_id=self.app_id,
            access_token=self.access_token
        )

        self.account = AdAccount(self.ad_account_id)

    def get_campaigns(self, name_filter=None, status_filter=None):
        """
        Busca campanhas da conta com filtros opcionais

        Args:
            name_filter: Filtrar por texto no nome (ex: "[VENDA]")
            status_filter: Lista de status (ex: ['ACTIVE', 'PAUSED'])

        Returns:
            Lista de campanhas
        """
        params = {
            'fields': [
                'id',
                'name',
                'status',
                'objective',
                'daily_budget',
                'lifetime_budget',
                'created_time',
                'updated_time'
            ]
        }

        filtering = []

        if status_filter:
            filtering.append({
                'field': 'campaign.status',
                'operator': 'IN',
                'value': status_filter
            })

        if name_filter:
            filtering.append({
                'field': 'campaign.name',
                'operator': 'CONTAIN',
                'value': name_filter
            })

        if filtering:
            params['filtering'] = filtering

        campaigns = self.account.get_campaigns(params=params)
        return list(campaigns)

    def get_sales_campaign_insights(self, campaign_id=None, days=30):
        """
        Busca insights específicos para campanhas de VENDA

        Métricas incluídas:
        - Alcance (reach)
        - Impressões (impressions)
        - Frequência (frequency)
        - CTR
        - CPC
        - Custo por visualização da página de destino (cost_per_action_type: landing_page_view)
        - Initiate Checkout - custo por IC (cost_per_action_type: initiate_checkout)
        - Compras (actions: purchase)
        - Custo por compra (cost_per_action_type: purchase)
        - ROAS (purchase_roas)

        Args:
            campaign_id: ID da campanha específica (None = todas [VENDA])
            days: Número de dias para análise

        Returns:
            Lista de insights
        """
        # Definir período
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        params = {
            'time_range': {
                'since': start_date.strftime('%Y-%m-%d'),
                'until': end_date.strftime('%Y-%m-%d')
            },
            'fields': [
                'campaign_id',
                'campaign_name',
                'reach',                    # Alcance
                'impressions',              # Impressões
                'frequency',                # Frequência
                'ctr',                      # CTR
                'cpc',                      # CPC
                'spend',                    # Gasto
                'actions',                  # Todas as ações (purchase, initiate_checkout, etc)
                'action_values',            # Valores das ações (receita)
                'cost_per_action_type',     # Custo por tipo de ação
                'purchase_roas',            # ROAS
                'date_start',
                'date_stop'
            ],
            'level': 'campaign',
            'time_increment': 1,  # Dados diários
            'action_attribution_windows': ['7d_click', '1d_view']
        }

        if campaign_id:
            # Insights de campanha específica
            campaign = Campaign(campaign_id)
            insights = campaign.get_insights(params=params)
        else:
            # Insights de todas as campanhas [VENDA]
            insights = self.account.get_insights(params=params)

        return list(insights)

    def get_sales_summary(self, days=30):
        """
        Resumo geral das campanhas de VENDA

        Returns:
            Dict com métricas totais
        """
        insights = self.get_sales_campaign_insights(days=days)

        if not insights:
            return {
                'total_spend': 0,
                'total_reach': 0,
                'total_impressions': 0,
                'avg_frequency': 0,
                'avg_ctr': 0,
                'avg_cpc': 0,
                'total_landing_page_views': 0,
                'cost_per_landing_page_view': 0,
                'total_initiate_checkout': 0,
                'cost_per_initiate_checkout': 0,
                'total_purchases': 0,
                'cost_per_purchase': 0,
                'total_revenue': 0,
                'roas': 0
            }

        # Agregar métricas
        total_spend = sum(float(i.get('spend', 0)) for i in insights)
        total_reach = sum(int(i.get('reach', 0)) for i in insights)
        total_impressions = sum(int(i.get('impressions', 0)) for i in insights)

        # Frequência média
        avg_frequency = (total_impressions / total_reach) if total_reach > 0 else 0

        # CTR e CPC médios
        total_clicks = sum(
            sum(int(action.get('value', 0))
                for action in i.get('actions', [])
                if action.get('action_type') == 'link_click')
            for i in insights
        )
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0

        # Landing Page Views
        total_landing_page_views = sum(
            sum(int(action.get('value', 0))
                for action in i.get('actions', [])
                if action.get('action_type') == 'landing_page_view')
            for i in insights
        )

        cost_per_landing_page_view = 0
        for insight in insights:
            for cost in insight.get('cost_per_action_type', []):
                if cost.get('action_type') == 'landing_page_view':
                    cost_per_landing_page_view += float(cost.get('value', 0))
        cost_per_landing_page_view = cost_per_landing_page_view / len(insights) if insights else 0

        # Initiate Checkout
        total_initiate_checkout = sum(
            sum(int(action.get('value', 0))
                for action in i.get('actions', [])
                if action.get('action_type') == 'initiate_checkout')
            for i in insights
        )

        cost_per_initiate_checkout = 0
        for insight in insights:
            for cost in insight.get('cost_per_action_type', []):
                if cost.get('action_type') == 'initiate_checkout':
                    cost_per_initiate_checkout += float(cost.get('value', 0))
        cost_per_initiate_checkout = cost_per_initiate_checkout / len(insights) if insights else 0

        # Purchases (Compras)
        total_purchases = sum(
            sum(int(action.get('value', 0))
                for action in i.get('actions', [])
                if action.get('action_type') == 'purchase')
            for i in insights
        )

        cost_per_purchase = 0
        for insight in insights:
            for cost in insight.get('cost_per_action_type', []):
                if cost.get('action_type') == 'purchase':
                    cost_per_purchase += float(cost.get('value', 0))
        cost_per_purchase = cost_per_purchase / len(insights) if insights else 0

        # Revenue e ROAS
        total_revenue = sum(
            sum(float(value.get('value', 0))
                for value in i.get('action_values', [])
                if value.get('action_type') == 'purchase')
            for i in insights
        )

        roas = (total_revenue / total_spend) if total_spend > 0 else 0

        return {
            'total_spend': total_spend,
            'total_reach': total_reach,
            'total_impressions': total_impressions,
            'avg_frequency': avg_frequency,
            'avg_ctr': avg_ctr,
            'avg_cpc': avg_cpc,
            'total_landing_page_views': total_landing_page_views,
            'cost_per_landing_page_view': cost_per_landing_page_view,
            'total_initiate_checkout': total_initiate_checkout,
            'cost_per_initiate_checkout': cost_per_initiate_checkout,
            'total_purchases': total_purchases,
            'cost_per_purchase': cost_per_purchase,
            'total_revenue': total_revenue,
            'roas': roas
        }
