"""
Dashboard de Performance - Sistema de Visualização em Tempo Real
Desenvolvido para F5 Estratégia
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any

from youtube_api_manager import initialize_youtube_system, YouTubeAnalyticsCollector
from content_optimizer import ContentOptimizer
from competitor_analyzer import CompetitorAnalyzer
from config import F5Config, AppConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class F5YouTubeDashboard:
    """Dashboard principal da F5 Estratégia para YouTube"""
    
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.setup_layout()
        self.setup_callbacks()
        
        # Inicializar sistemas
        try:
            self.youtube_system = initialize_youtube_system()
            self.analytics_collector = self.youtube_system['analytics_collector']
            self.data_collector = self.youtube_system['data_collector']
            self.content_optimizer = ContentOptimizer()
            self.competitor_analyzer = CompetitorAnalyzer(self.youtube_system['api_manager'])
            logger.info("Dashboard inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar sistemas do dashboard: {e}")
            self.youtube_system = None
    
    def setup_layout(self):
        """Configura o layout do dashboard"""
        
        # Estilo CSS customizado
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("F5 Estratégia - YouTube Analytics Dashboard", 
                       className="dashboard-title"),
                html.P("Sistema de Otimização e Análise de Performance", 
                       className="dashboard-subtitle"),
                html.Div([
                    html.Span("🔴 Ao Vivo", className="live-indicator"),
                    html.Span(id="last-update", className="last-update")
                ], className="status-bar")
            ], className="header"),
            
            # Navigation
            html.Div([
                dcc.Tabs(id="main-tabs", value="overview", children=[
                    dcc.Tab(label="📊 Visão Geral", value="overview"),
                    dcc.Tab(label="🎯 Análise de Conteúdo", value="content"),
                    dcc.Tab(label="🏆 Concorrentes", value="competitors"),
                    dcc.Tab(label="📈 Tendências", value="trends"),
                    dcc.Tab(label="⚙️ Otimização", value="optimization")
                ])
            ], className="navigation"),
            
            # Main Content
            html.Div(id="main-content", className="main-content"),
            
            # Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=300*1000,  # 5 minutos
                n_intervals=0
            )
            
        ], className="dashboard-container")
    
    def setup_callbacks(self):
        """Configura os callbacks do dashboard"""
        
        @self.app.callback(
            Output('main-content', 'children'),
            Input('main-tabs', 'value')
        )
        def render_tab_content(active_tab):
            if active_tab == "overview":
                return self.render_overview_tab()
            elif active_tab == "content":
                return self.render_content_tab()
            elif active_tab == "competitors":
                return self.render_competitors_tab()
            elif active_tab == "trends":
                return self.render_trends_tab()
            elif active_tab == "optimization":
                return self.render_optimization_tab()
            return html.Div("Selecionando aba...")
        
        @self.app.callback(
            Output('last-update', 'children'),
            Input('interval-component', 'n_intervals')
        )
        def update_timestamp(n):
            return f"Última atualização: {datetime.now().strftime('%H:%M:%S')}"
    
    def render_overview_tab(self) -> html.Div:
        """Renderiza a aba de visão geral"""
        return html.Div([
            # KPIs principais
            html.Div([
                html.H2("📊 KPIs Principais", className="section-title"),
                html.Div(id="kpi-cards", children=self.create_kpi_cards())
            ], className="section"),
            
            # Gráficos de performance
            html.Div([
                html.H2("📈 Performance do Canal", className="section-title"),
                html.Div([
                    html.Div([
                        dcc.Graph(id="views-chart")
                    ], className="chart-container"),
                    html.Div([
                        dcc.Graph(id="engagement-chart")
                    ], className="chart-container")
                ], className="charts-row")
            ], className="section"),
            
            # Fontes de tráfego
            html.Div([
                html.H2("🚀 Fontes de Tráfego", className="section-title"),
                dcc.Graph(id="traffic-sources-chart")
            ], className="section")
        ])
    
    def render_content_tab(self) -> html.Div:
        """Renderiza a aba de análise de conteúdo"""
        return html.Div([
            # Selector de vídeo
            html.Div([
                html.H2("🎯 Análise de Conteúdo", className="section-title"),
                html.Div([
                    dcc.Dropdown(
                        id="video-selector",
                        placeholder="Selecione um vídeo para análise",
                        style={'margin-bottom': '20px'}
                    ),
                    html.Button("Analisar Vídeo", id="analyze-btn", 
                               className="btn-primary")
                ])
            ], className="section"),
            
            # Resultados da análise
            html.Div(id="content-analysis-results", className="section")
        ])
    
    def render_competitors_tab(self) -> html.Div:
        """Renderiza a aba de análise de concorrentes"""
        return html.Div([
            html.H2("🏆 Análise de Concorrentes", className="section-title"),
            
            # Controles
            html.Div([
                html.Div([
                    html.Label("Palavras-chave para análise:"),
                    dcc.Dropdown(
                        id="keywords-selector",
                        options=[{'label': kw, 'value': kw} for kw in F5Config.CORE_KEYWORDS],
                        value=F5Config.CORE_KEYWORDS[:3],
                        multi=True
                    )
                ], className="control-group"),
                html.Button("Executar Análise", id="competitor-analyze-btn", 
                           className="btn-primary")
            ], className="controls-section"),
            
            # Resultados
            html.Div(id="competitor-analysis-results", className="section")
        ])
    
    def render_trends_tab(self) -> html.Div:
        """Renderiza a aba de tendências"""
        return html.Div([
            html.H2("📈 Análise de Tendências", className="section-title"),
            
            # Trending topics
            html.Div([
                html.H3("🔥 Tópicos em Alta"),
                html.Div(id="trending-topics")
            ], className="section"),
            
            # Oportunidades de conteúdo
            html.Div([
                html.H3("💡 Oportunidades de Conteúdo"),
                html.Div(id="content-opportunities")
            ], className="section")
        ])
    
    def render_optimization_tab(self) -> html.Div:
        """Renderiza a aba de otimização"""
        return html.Div([
            html.H2("⚙️ Otimização de Conteúdo", className="section-title"),
            
            # Input de análise
            html.Div([
                html.Div([
                    html.Label("Título do Vídeo:"),
                    dcc.Input(
                        id="title-input",
                        type="text",
                        placeholder="Digite o título do vídeo...",
                        style={'width': '100%', 'margin-bottom': '10px'}
                    )
                ]),
                html.Div([
                    html.Label("Descrição:"),
                    dcc.Textarea(
                        id="description-input",
                        placeholder="Digite a descrição do vídeo...",
                        style={'width': '100%', 'height': 100, 'margin-bottom': '10px'}
                    )
                ]),
                html.Div([
                    html.Label("Tags (separadas por vírgula):"),
                    dcc.Input(
                        id="tags-input",
                        type="text",
                        placeholder="tag1, tag2, tag3...",
                        style={'width': '100%', 'margin-bottom': '10px'}
                    )
                ]),
                html.Button("Otimizar Conteúdo", id="optimize-btn", 
                           className="btn-primary")
            ], className="optimization-inputs"),
            
            # Resultados da otimização
            html.Div(id="optimization-results", className="section")
        ])
    
    def create_kpi_cards(self) -> List[html.Div]:
        """Cria cards de KPIs"""
        # Dados simulados - em produção viriam das APIs
        kpis = [
            {"title": "Total de Visualizações", "value": "125.4K", "change": "+12.3%", "trend": "up"},
            {"title": "Inscritos", "value": "8.9K", "change": "+5.7%", "trend": "up"},
            {"title": "Taxa de Engajamento", "value": "4.2%", "change": "+0.8%", "trend": "up"},
            {"title": "Score SEO Médio", "value": "7.8/10", "change": "+1.2", "trend": "up"}
        ]
        
        cards = []
        for kpi in kpis:
            trend_icon = "📈" if kpi["trend"] == "up" else "📉"
            change_class = "positive" if kpi["trend"] == "up" else "negative"
            
            card = html.Div([
                html.Div([
                    html.H3(kpi["title"], className="kpi-title"),
                    html.H2(kpi["value"], className="kpi-value"),
                    html.P([
                        html.Span(trend_icon),
                        html.Span(kpi["change"], className=f"kpi-change {change_class}")
                    ])
                ])
            ], className="kpi-card")
            cards.append(card)
        
        return cards
    
    def get_sample_charts_data(self):
        """Gera dados de exemplo para os gráficos"""
        # Dados de visualizações (últimos 30 dias)
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                             end=datetime.now(), freq='D')
        
        views_data = {
            'date': dates,
            'views': [1200 + i*50 + (i%7)*200 for i in range(len(dates))],
            'impressions': [8000 + i*300 + (i%7)*1000 for i in range(len(dates))]
        }
        
        # Dados de engajamento
        engagement_data = {
            'metric': ['Curtidas', 'Comentários', 'Compartilhamentos', 'Saves'],
            'count': [1250, 89, 156, 234],
            'percentage': [85, 6, 11, 16]
        }
        
        # Fontes de tráfego
        traffic_data = {
            'source': ['YouTube Search', 'Browse Features', 'External', 'Direct', 'Suggested'],
            'percentage': [45, 25, 15, 10, 5],
            'views': [5625, 3125, 1875, 1250, 625]
        }
        
        return views_data, engagement_data, traffic_data
    
    def run_server(self, debug=True, port=8050):
        """Inicia o servidor do dashboard"""
        self.app.run_server(debug=debug, port=port)

# Funções auxiliares para callbacks mais complexos
def create_views_chart(views_data):
    """Cria gráfico de visualizações"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=views_data['date'],
        y=views_data['views'],
        mode='lines+markers',
        name='Visualizações',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=views_data['date'],
        y=views_data['impressions'],
        mode='lines',
        name='Impressões',
        line=dict(color='#004E89', width=2, dash='dash'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Visualizações vs Impressões (30 dias)",
        xaxis_title="Data",
        yaxis_title="Visualizações",
        yaxis2=dict(title="Impressões", overlaying='y', side='right'),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_engagement_chart(engagement_data):
    """Cria gráfico de engajamento"""
    fig = px.bar(
        x=engagement_data['metric'],
        y=engagement_data['count'],
        title="Métricas de Engajamento",
        color=engagement_data['count'],
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    
    return fig

def create_traffic_sources_chart(traffic_data):
    """Cria gráfico de fontes de tráfego"""
    fig = px.pie(
        values=traffic_data['percentage'],
        names=traffic_data['source'],
        title="Fontes de Tráfego",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

# CSS Styles
dashboard_styles = """
.dashboard-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f5f6fa;
    min-height: 100vh;
}

.header {
    background: linear-gradient(135deg, #FF6B35 0%, #004E89 100%);
    color: white;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.dashboard-title {
    margin: 0;
    font-size: 2.5em;
    font-weight: bold;
}

.dashboard-subtitle {
    margin: 5px 0 0 0;
    font-size: 1.2em;
    opacity: 0.9;
}

.status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 15px;
}

.live-indicator {
    background-color: #e74c3c;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 0.9em;
    font-weight: bold;
}

.last-update {
    font-size: 0.9em;
    opacity: 0.8;
}

.navigation {
    background-color: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.main-content {
    padding: 20px;
    max-width: 1400px;
    margin: 0 auto;
}

.section {
    background-color: white;
    border-radius: 10px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.section-title {
    color: #2c3e50;
    border-bottom: 3px solid #FF6B35;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.kpi-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    padding: 20px;
    margin: 10px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.kpi-card:hover {
    transform: translateY(-5px);
}

.kpi-title {
    font-size: 0.9em;
    margin: 0 0 10px 0;
    opacity: 0.9;
}

.kpi-value {
    font-size: 2.2em;
    font-weight: bold;
    margin: 0 0 10px 0;
}

.kpi-change.positive {
    color: #2ecc71;
}

.kpi-change.negative {
    color: #e74c3c;
}

.charts-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.chart-container {
    background-color: white;
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.btn-primary {
    background-color: #FF6B35;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}

.btn-primary:hover {
    background-color: #e55a2b;
}

.controls-section {
    background-color: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.control-group {
    margin-bottom: 15px;
}

.optimization-inputs {
    background-color: #f8f9fa;
    padding: 25px;
    border-radius: 8px;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .charts-row {
        grid-template-columns: 1fr;
    }
    
    .dashboard-title {
        font-size: 1.8em;
    }
}
"""

def create_f5_dashboard():
    """Factory function para criar o dashboard"""
    dashboard = F5YouTubeDashboard()
    
    # Adicionar estilos CSS
    dashboard.app.index_string = f'''
    <!DOCTYPE html>
    <html>
        <head>
            {{%metas%}}
            <title>F5 Estratégia - YouTube Dashboard</title>
            {{%favicon%}}
            {{%css%}}
            <style>
                {dashboard_styles}
            </style>
        </head>
        <body>
            {{%app_entry%}}
            <footer>
                {{%config%}}
                {{%scripts%}}
                {{%renderer%}}
            </footer>
        </body>
    </html>
    '''
    
    return dashboard

if __name__ == "__main__":
    # Inicializar e executar dashboard
    dashboard = create_f5_dashboard()
    
    print("🚀 Iniciando F5 YouTube Analytics Dashboard...")
    print("📊 Dashboard disponível em: http://localhost:8050")
    print("🔗 Ctrl+C para parar o servidor")
    
    dashboard.run_server(debug=True, port=8050) 