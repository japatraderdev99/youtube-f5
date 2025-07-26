"""
Módulo de Analytics Avançado - Dashboard Moderno F5
Análises sofisticadas e visualizações interativas para otimização de conteúdo

Desenvolvido para F5 Estratégia
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

class AdvancedContentAnalytics:
    """Analytics avançado para análise de conteúdo"""
    
    def __init__(self):
        self.performance_data = self._generate_sample_data()
    
    def _generate_sample_data(self) -> pd.DataFrame:
        """Gera dados de exemplo para demonstração"""
        dates = pd.date_range(start=datetime.now() - timedelta(days=90), 
                             end=datetime.now(), freq='D')
        
        np.random.seed(42)  # Para resultados consistentes
        
        data = []
        for date in dates:
            # Simular dados realistas de performance
            base_views = 1000 + np.random.normal(0, 200)
            day_of_week = date.weekday()
            
            # Ajustar por dia da semana (mais visualizações nos fins de semana)
            weekend_boost = 1.3 if day_of_week >= 5 else 1.0
            
            views = max(0, int(base_views * weekend_boost))
            likes = max(0, int(views * np.random.uniform(0.02, 0.08)))
            comments = max(0, int(views * np.random.uniform(0.001, 0.005)))
            shares = max(0, int(views * np.random.uniform(0.002, 0.01)))
            
            data.append({
                'date': date,
                'views': views,
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'watch_time': views * np.random.uniform(2.5, 8.5),  # minutos
                'ctr': np.random.uniform(0.02, 0.12),
                'retention_rate': np.random.uniform(0.25, 0.75)
            })
        
        return pd.DataFrame(data)
    
    def create_performance_overview_chart(self) -> go.Figure:
        """Cria gráfico de visão geral de performance"""
        df = self.performance_data.tail(30)  # Últimos 30 dias
        
        fig = go.Figure()
        
        # Views
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['views'],
            mode='lines+markers',
            name='Visualizações',
            line=dict(color='#FF6B35', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{y:,}</b> views<br>%{x}<extra></extra>'
        ))
        
        # Adicionar média móvel
        df['views_ma'] = df['views'].rolling(window=7).mean()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['views_ma'],
            mode='lines',
            name='Média Móvel (7 dias)',
            line=dict(color='#004E89', width=2, dash='dash'),
            hovertemplate='<b>%{y:,.0f}</b> views (média)<br>%{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Performance de Visualizações (30 dias)",
            xaxis_title="Data",
            yaxis_title="Visualizações",
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Arial", size=12),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Adicionar anotações para picos de performance
        max_views_idx = df['views'].idxmax()
        max_views_date = df.loc[max_views_idx, 'date']
        max_views_value = df.loc[max_views_idx, 'views']
        
        fig.add_annotation(
            x=max_views_date,
            y=max_views_value,
            text=f"Pico: {max_views_value:,}",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#FF6B35",
            bgcolor="rgba(255,107,53,0.8)",
            bordercolor="#FF6B35",
            font=dict(color="white")
        )
        
        return fig
    
    def create_engagement_funnel_chart(self) -> go.Figure:
        """Cria gráfico de funil de engajamento"""
        df = self.performance_data.tail(30)
        
        # Calcular métricas do funil
        total_views = df['views'].sum()
        total_likes = df['likes'].sum()
        total_comments = df['comments'].sum()
        total_shares = df['shares'].sum()
        
        # Simular conversões
        subscribers = int(total_shares * 0.3)  # 30% dos shares viram inscritos
        leads = int(subscribers * 0.1)  # 10% dos inscritos viram leads
        
        stages = ['Views', 'Likes', 'Comments', 'Shares', 'Subscribers', 'Leads']
        values = [total_views, total_likes, total_comments, total_shares, subscribers, leads]
        
        # Calcular percentuais de conversão
        percentages = [100]
        for i in range(1, len(values)):
            percentage = (values[i] / values[0]) * 100
            percentages.append(percentage)
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            texttemplate="<b>%{value:,}</b><br>(%{percentInitial:.1%})",
            marker=dict(
                color=['#FF6B35', '#E55A2B', '#CC4E24', '#B3421D', '#993717', '#7F2B10'],
                line=dict(width=2, color="white")
            ),
            connector=dict(line=dict(color="rgba(0,0,0,0.2)", dash="dot", width=3))
        ))
        
        fig.update_layout(
            title="Funil de Engajamento (30 dias)",
            font=dict(family="Arial", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_content_performance_heatmap(self) -> go.Figure:
        """Cria heatmap de performance por dia da semana e hora"""
        # Simular dados de performance por hora e dia da semana
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        hours = list(range(24))
        
        np.random.seed(42)
        
        # Criar matriz de performance
        performance_matrix = []
        for day in range(7):
            day_performance = []
            for hour in hours:
                # Simular padrões realistas (mais atividade à noite e fins de semana)
                base_performance = 50
                
                # Boost para horários de pico (18h-22h)
                if 18 <= hour <= 22:
                    base_performance *= 1.8
                
                # Boost para fins de semana
                if day >= 5:  # Sábado e Domingo
                    base_performance *= 1.4
                
                # Adicionar variação aleatória
                performance = base_performance * np.random.uniform(0.7, 1.3)
                day_performance.append(performance)
            
            performance_matrix.append(day_performance)
        
        fig = go.Figure(data=go.Heatmap(
            z=performance_matrix,
            x=[f"{h:02d}:00" for h in hours],
            y=days,
            colorscale='RdYlBu_r',
            showscale=True,
            hoverongaps=False,
            hovertemplate='<b>%{y}</b><br>%{x}<br>Score: %{z:.1f}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Heatmap de Performance: Dia da Semana vs Horário",
            xaxis_title="Horário",
            yaxis_title="Dia da Semana",
            font=dict(family="Arial", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_seo_radar_chart(self, video_data: Dict[str, Any]) -> go.Figure:
        """Cria gráfico radar para análise SEO"""
        # Simular scores SEO baseados no conteúdo
        categories = [
            'Título SEO',
            'Descrição',
            'Tags',
            'Thumbnail',
            'Engagement',
            'Duração',
            'Call-to-Action',
            'Persona Fit'
        ]
        
        # Gerar scores baseados no conteúdo (simulado)
        scores = [
            np.random.uniform(6, 10),  # Título SEO
            np.random.uniform(7, 9),   # Descrição
            np.random.uniform(5, 8),   # Tags
            np.random.uniform(6, 9),   # Thumbnail
            np.random.uniform(4, 8),   # Engagement
            np.random.uniform(7, 10),  # Duração
            np.random.uniform(3, 7),   # Call-to-Action
            np.random.uniform(8, 10)   # Persona Fit
        ]
        
        fig = go.Figure()
        
        # Score atual
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Score Atual',
            line_color='#FF6B35',
            fillcolor='rgba(255,107,53,0.3)'
        ))
        
        # Score ideal (benchmark)
        ideal_scores = [9, 9, 8, 9, 8, 9, 8, 9]
        fig.add_trace(go.Scatterpolar(
            r=ideal_scores,
            theta=categories,
            fill='toself',
            name='Score Ideal',
            line_color='#004E89',
            fillcolor='rgba(0,78,137,0.1)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=10),
                    gridcolor="rgba(0,0,0,0.1)"
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                )
            ),
            showlegend=True,
            title="Análise SEO Multidimensional",
            font=dict(family="Arial", size=12),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Retorna métricas principais de performance"""
        df = self.performance_data.tail(30)
        df_prev = self.performance_data.tail(60).head(30)
        
        current_metrics = {
            'total_views': df['views'].sum(),
            'avg_daily_views': df['views'].mean(),
            'total_engagement': df['likes'].sum() + df['comments'].sum() + df['shares'].sum(),
            'avg_retention': df['retention_rate'].mean(),
            'avg_ctr': df['ctr'].mean()
        }
        
        prev_metrics = {
            'total_views': df_prev['views'].sum(),
            'avg_daily_views': df_prev['views'].mean(),
            'total_engagement': df_prev['likes'].sum() + df_prev['comments'].sum() + df_prev['shares'].sum(),
            'avg_retention': df_prev['retention_rate'].mean(),
            'avg_ctr': df_prev['ctr'].mean()
        }
        
        # Calcular variações
        metrics_with_changes = {}
        for key in current_metrics:
            current = current_metrics[key]
            previous = prev_metrics[key]
            change = ((current - previous) / previous) * 100 if previous > 0 else 0
            
            metrics_with_changes[key] = {
                'value': current,
                'change': change,
                'trend': 'up' if change > 0 else 'down' if change < 0 else 'stable'
            }
        
        return metrics_with_changes
    
    def analyze_content_gaps(self) -> List[Dict[str, Any]]:
        """Analisa lacunas de conteúdo e oportunidades"""
        gaps = [
            {
                'category': 'Funil de Vendas',
                'opportunity': 'Conteúdo sobre qualificação de leads',
                'potential_reach': '+35% audience',
                'competition_level': 'Médio',
                'priority': 'Alta'
            },
            {
                'category': 'Attribution Models',
                'opportunity': 'Vídeos sobre multi-touch attribution',
                'potential_reach': '+28% audience',
                'competition_level': 'Baixo',
                'priority': 'Alta'
            },
            {
                'category': 'Marketing Automation',
                'opportunity': 'Tutoriais de configuração de workflows',
                'potential_reach': '+22% audience',
                'competition_level': 'Alto',
                'priority': 'Média'
            },
            {
                'category': 'Customer Journey',
                'opportunity': 'Mapping de jornada do cliente B2B',
                'potential_reach': '+31% audience',
                'competition_level': 'Médio',
                'priority': 'Alta'
            }
        ]
        
        return gaps
    
    def predict_performance(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prediz performance baseado em dados históricos"""
        # Simulação de modelo de ML simples
        base_score = 100
        
        # Fatores que influenciam performance
        title_length = len(video_data.get('title', ''))
        if 40 <= title_length <= 70:  # Tamanho ideal
            base_score *= 1.2
        
        # Presença de números no título
        if any(char.isdigit() for char in video_data.get('title', '')):
            base_score *= 1.15
        
        # Persona target
        persona_multipliers = {
            'estrategico': 1.1,
            'crescimento': 1.25,
            'smart': 1.0
        }
        persona = video_data.get('target_persona', 'crescimento')
        base_score *= persona_multipliers.get(persona, 1.0)
        
        # Variação aleatória para simular incerteza
        np.random.seed(hash(video_data.get('title', '')) % 2**32)
        variation = np.random.uniform(0.8, 1.3)
        predicted_views = int(base_score * 15 * variation)  # ~1500 views base
        
        return {
            'predicted_views': predicted_views,
            'confidence_interval': [
                int(predicted_views * 0.7),
                int(predicted_views * 1.4)
            ],
            'predicted_engagement_rate': np.random.uniform(3.5, 7.2),
            'estimated_reach': f"{predicted_views * np.random.uniform(0.15, 0.35):,.0f}",
            'performance_category': self._categorize_performance(predicted_views)
        }
    
    def _categorize_performance(self, views: int) -> str:
        """Categoriza performance baseada em views"""
        if views >= 5000:
            return "Excelente"
        elif views >= 2500:
            return "Boa"
        elif views >= 1000:
            return "Média"
        else:
            return "Baixa"

class TrendAnalyzer:
    """Analisador de tendências de mercado"""
    
    def __init__(self):
        self.trending_data = self._generate_trending_data()
    
    def _generate_trending_data(self) -> List[Dict[str, Any]]:
        """Gera dados de tendências"""
        return [
            {
                'keyword': 'IA no Marketing',
                'search_volume': 45200,
                'growth_rate': 150,
                'competition': 'Média',
                'opportunity_score': 8.5,
                'related_topics': ['ChatGPT Marketing', 'AI Tools', 'Automation']
            },
            {
                'keyword': 'Attribution Models',
                'search_volume': 23100,
                'growth_rate': 89,
                'competition': 'Baixa',
                'opportunity_score': 9.2,
                'related_topics': ['Multi-touch', 'First-click', 'Last-click']
            },
            {
                'keyword': 'First-Party Data',
                'search_volume': 34500,
                'growth_rate': 67,
                'competition': 'Alta',
                'opportunity_score': 7.8,
                'related_topics': ['Cookies', 'Privacy', 'LGPD']
            }
        ]
    
    def get_trending_opportunities(self) -> List[Dict[str, Any]]:
        """Retorna oportunidades de conteúdo baseadas em tendências"""
        opportunities = []
        
        for trend in self.trending_data:
            if trend['opportunity_score'] >= 8.0:
                opportunities.append({
                    'title': f"Como usar {trend['keyword']} para acelerar resultados",
                    'keyword': trend['keyword'],
                    'estimated_reach': trend['search_volume'],
                    'competition_level': trend['competition'],
                    'urgency': 'Alta' if trend['growth_rate'] > 100 else 'Média'
                })
        
        return opportunities 