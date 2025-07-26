"""
Dashboard Moderno F5 - Interface Avançada para Otimização de Conteúdo
Sistema sofisticado com UX intuitivo para transcrições e busca de conteúdos

Desenvolvido para F5 Estratégia
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import re
import os
from typing import Dict, List, Any, Optional
import asyncio
from pathlib import Path

# Imports locais
from content_optimizer import ContentOptimizer
from competitor_analyzer import CompetitorAnalyzer
from youtube_api_manager import initialize_youtube_system
from config import F5Config, AppConfig

# Configuração da página
st.set_page_config(
    page_title="F5 Estratégia - Dashboard Avançado",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para UX moderno
def load_custom_css():
    st.markdown("""
    <style>
    /* Tema principal */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #004E89;
        --accent-color: #1A936F;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 8px 32px rgba(0,0,0,0.1);
        --border-radius: 16px;
    }
    
    /* Layout principal */
    .main-header {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: var(--card-shadow);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    /* Cards modernos */
    .modern-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--card-shadow);
        border: 1px solid #e1e5e9;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    /* Botões estilizados */
    .stButton > button {
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255,107,53,0.3);
    }
    
    .stButton > button:hover {
        background: #e55a2b;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255,107,53,0.4);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e1e5e9;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(255,107,53,0.1);
    }
    
    /* Sidebar moderna */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Métricas KPI */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Drag and drop area */
    .upload-area {
        border: 3px dashed var(--primary-color);
        border-radius: var(--border-radius);
        padding: 3rem;
        text-align: center;
        background: linear-gradient(45deg, rgba(255,107,53,0.05), rgba(0,78,137,0.05));
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: linear-gradient(45deg, rgba(255,107,53,0.1), rgba(0,78,137,0.1));
        transform: scale(1.02);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .status-processing {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    /* Animações */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .modern-card {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Classes auxiliares
class TranscriptionProcessor:
    """Processador avançado de transcrições"""
    
    def __init__(self):
        self.content_optimizer = ContentOptimizer()
    
    def extract_key_insights(self, transcription: str) -> Dict[str, Any]:
        """Extrai insights principais da transcrição"""
        insights = {
            'word_count': len(transcription.split()),
            'estimated_duration': len(transcription.split()) / 150,  # ~150 palavras/minuto
            'key_topics': self._extract_topics(transcription),
            'sentiment_analysis': self._analyze_sentiment(transcription),
            'call_to_actions': self._find_ctas(transcription),
            'technical_terms': self._find_technical_terms(transcription)
        }
        return insights
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extrai tópicos principais usando palavras-chave"""
        marketing_keywords = [
            'marketing digital', 'tráfego pago', 'seo', 'conversão', 
            'roi', 'leads', 'funil', 'vendas', 'crm', 'analytics'
        ]
        
        found_topics = []
        text_lower = text.lower()
        
        for keyword in marketing_keywords:
            if keyword in text_lower:
                found_topics.append(keyword)
        
        return found_topics[:5]  # Top 5 tópicos
    
    def _analyze_sentiment(self, text: str) -> str:
        """Análise básica de sentimento"""
        positive_words = ['sucesso', 'crescimento', 'resultado', 'excelente', 'ótimo']
        negative_words = ['problema', 'dificuldade', 'erro', 'falha', 'ruim']
        
        positive_count = sum(1 for word in positive_words if word in text.lower())
        negative_count = sum(1 for word in negative_words if word in text.lower())
        
        if positive_count > negative_count:
            return "Positivo"
        elif negative_count > positive_count:
            return "Negativo"
        else:
            return "Neutro"
    
    def _find_ctas(self, text: str) -> List[str]:
        """Encontra chamadas para ação no texto"""
        cta_patterns = [
            r'inscreva[-\s]?se',
            r'clique\s+aqui',
            r'acesse\s+o\s+link',
            r'baixe\s+(?:o|a)',
            r'entre\s+em\s+contato',
            r'agende\s+(?:uma|um)',
        ]
        
        found_ctas = []
        for pattern in cta_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            found_ctas.extend(matches)
        
        return list(set(found_ctas))  # Remove duplicatas
    
    def _find_technical_terms(self, text: str) -> List[str]:
        """Encontra termos técnicos relevantes"""
        tech_terms = [
            'pixel', 'utm', 'api', 'dashboard', 'kpi', 'roi', 'roas',
            'ctr', 'cpc', 'cpm', 'lookalike', 'retargeting', 'remarketing'
        ]
        
        found_terms = []
        text_lower = text.lower()
        
        for term in tech_terms:
            if term in text_lower:
                found_terms.append(term.upper())
        
        return found_terms

class ContentSearchEngine:
    """Motor de busca avançado para conteúdos"""
    
    def __init__(self):
        self.content_database = self._load_content_database()
    
    def _load_content_database(self) -> List[Dict[str, Any]]:
        """Carrega banco de dados de conteúdos"""
        # Simulação de banco de dados - em produção seria conectado a uma API
        return [
            {
                'title': 'Como estruturar funil de vendas que converte',
                'category': 'Funil de Vendas',
                'persona': 'crescimento',
                'keywords': ['funil', 'vendas', 'conversão', 'estrutura'],
                'performance_score': 8.5,
                'views': 15420,
                'engagement_rate': 4.2
            },
            {
                'title': 'ROI em tráfego pago: Métricas que importam',
                'category': 'Tráfego Pago',
                'persona': 'estrategico',
                'keywords': ['roi', 'tráfego pago', 'métricas', 'análise'],
                'performance_score': 9.1,
                'views': 23650,
                'engagement_rate': 5.8
            },
            {
                'title': 'Geração de leads: 5 estratégias práticas',
                'category': 'Lead Generation',
                'persona': 'smart',
                'keywords': ['leads', 'geração', 'estratégias', 'prático'],
                'performance_score': 7.9,
                'views': 18330,
                'engagement_rate': 3.9
            }
        ]
    
    def search_content(self, query: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Busca conteúdos baseado em query e filtros"""
        results = []
        query_lower = query.lower()
        
        for content in self.content_database:
            # Calcular score de relevância
            relevance_score = 0
            
            # Busca no título
            if query_lower in content['title'].lower():
                relevance_score += 3
            
            # Busca nas keywords
            for keyword in content['keywords']:
                if query_lower in keyword.lower():
                    relevance_score += 2
            
            # Busca na categoria
            if query_lower in content['category'].lower():
                relevance_score += 1
            
            # Aplicar filtros se fornecidos
            if filters:
                if 'persona' in filters and filters['persona'] != content['persona']:
                    continue
                if 'min_score' in filters and content['performance_score'] < filters['min_score']:
                    continue
            
            if relevance_score > 0:
                content_copy = content.copy()
                content_copy['relevance_score'] = relevance_score
                results.append(content_copy)
        
        # Ordenar por relevância
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results
    
    def get_trending_topics(self) -> List[Dict[str, Any]]:
        """Retorna tópicos em tendência"""
        return [
            {'topic': 'IA no Marketing', 'growth': '+150%', 'searches': 45200},
            {'topic': 'Attribution Models', 'growth': '+89%', 'searches': 23100},
            {'topic': 'First-Party Data', 'growth': '+67%', 'searches': 34500},
            {'topic': 'Marketing Automation', 'growth': '+45%', 'searches': 67800},
            {'topic': 'Customer Journey', 'growth': '+23%', 'searches': 56700}
        ]

# Funções principais da interface
def render_header():
    """Renderiza cabeçalho principal"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 F5 Estratégia</h1>
        <p>Dashboard Avançado para Otimização de Conteúdo YouTube</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renderiza sidebar com navegação"""
    with st.sidebar:
        st.markdown("## 🎯 Navegação")
        
        page = st.selectbox(
            "Escolha uma seção:",
            [
                "📝 Inserir Transcrição",
                "🔍 Buscar Conteúdos", 
                "📊 Analytics Avançado",
                "🏆 Análise Competitiva",
                "💡 Sugestões IA",
                "⚙️ Configurações"
            ]
        )
        
        st.markdown("---")
        
        # Status do sistema
        st.markdown("### 📡 Status do Sistema")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="status-success">🟢 Online</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="status-processing">⚡ IA Ativa</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Métricas rápidas
        st.markdown("### 📈 Métricas Rápidas")
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8.7</div>
            <div class="metric-label">Score SEO Médio</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">156</div>
            <div class="metric-label">Vídeos Analisados</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">+23%</div>
            <div class="metric-label">Crescimento Mensal</div>
        </div>
        """, unsafe_allow_html=True)
    
    return page

def page_transcription_input():
    """Página para inserção de transcrições"""
    st.markdown("## 📝 Análise de Transcrição de Vídeo")
    st.markdown("Insira a transcrição do seu vídeo para análise inteligente e otimização automática.")
    
    # Container principal
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            
            # Método de input
            input_method = st.radio(
                "Como você quer inserir a transcrição?",
                ["📝 Digitar/Colar texto", "📁 Upload de arquivo", "🎤 Áudio para texto (em breve)"],
                horizontal=True
            )
            
            transcription_text = ""
            
            if input_method == "📝 Digitar/Colar texto":
                transcription_text = st.text_area(
                    "Cole ou digite a transcrição aqui:",
                    height=300,
                    placeholder="Cole aqui a transcrição do seu vídeo...\n\nEx: Olá pessoal, bem-vindos ao canal! Hoje vamos falar sobre estratégias de marketing digital que realmente funcionam..."
                )
            
            elif input_method == "📁 Upload de arquivo":
                uploaded_file = st.file_uploader(
                    "Faça upload de um arquivo de texto",
                    type=['txt', 'docx', 'pdf']
                )
                
                if uploaded_file is not None:
                    if uploaded_file.type == "text/plain":
                        transcription_text = str(uploaded_file.read(), "utf-8")
                        st.success("✅ Arquivo carregado com sucesso!")
            
            # Informações do vídeo
            st.markdown("### 📋 Informações do Vídeo (Opcional)")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                video_title = st.text_input("Título do vídeo:")
                video_category = st.selectbox(
                    "Categoria:",
                    ["Marketing Digital", "Tráfego Pago", "Vendas", "Estratégia", "Analytics", "Outros"]
                )
            
            with col_b:
                target_persona = st.selectbox(
                    "Persona alvo:",
                    ["estrategico", "crescimento", "smart"]
                )
                video_duration = st.number_input("Duração estimada (min):", min_value=1, max_value=120, value=10)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="modern-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 Análise Rápida")
            
            if transcription_text:
                processor = TranscriptionProcessor()
                insights = processor.extract_key_insights(transcription_text)
                
                # Métricas básicas
                st.metric("Palavras", f"{insights['word_count']:,}")
                st.metric("Duração estimada", f"{insights['estimated_duration']:.1f} min")
                st.metric("Sentimento", insights['sentiment_analysis'])
                
                # Tópicos encontrados
                if insights['key_topics']:
                    st.markdown("**🏷️ Tópicos identificados:**")
                    for topic in insights['key_topics']:
                        st.markdown(f"• {topic}")
                
                # CTAs encontrados
                if insights['call_to_actions']:
                    st.markdown("**📢 CTAs encontrados:**")
                    for cta in insights['call_to_actions']:
                        st.markdown(f"• {cta}")
            
            else:
                st.info("👆 Insira uma transcrição para ver a análise")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de análise principal
    if st.button("🚀 Analisar e Otimizar Conteúdo", type="primary", use_container_width=True):
        if transcription_text:
            with st.spinner("🤖 Analisando transcrição com IA..."):
                # Simular processamento
                import time
                time.sleep(2)
                
                # Exibir resultados
                render_optimization_results(transcription_text, video_title, target_persona)
        else:
            st.error("❌ Por favor, insira uma transcrição antes de continuar.")

def render_optimization_results(transcription: str, title: str, persona: str):
    """Renderiza resultados da otimização"""
    st.markdown("---")
    st.markdown("## 🎯 Resultados da Otimização")
    
    # Tabs para diferentes resultados
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Score SEO", "📝 Sugestões de Melhoria", "🏷️ Tags Otimizadas", "📈 Projeção de Performance"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">8.5</div>
                <div class="metric-label">Score SEO Geral</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">92%</div>
                <div class="metric-label">Adequação à Persona</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">7.2</div>
                <div class="metric-label">Potencial de Engajamento</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico radar de análise
        categories = ['SEO', 'Engajamento', 'Clareza', 'CTA', 'Persona Fit']
        scores = [8.5, 7.2, 9.1, 6.8, 9.2]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Score Atual',
            line_color='#FF6B35'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            title="Análise Multidimensional do Conteúdo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 💡 Sugestões de Melhoria")
        
        suggestions = [
            {
                'priority': 'Alta',
                'category': 'SEO',
                'suggestion': 'Adicionar palavra-chave principal no primeiro parágrafo',
                'impact': '+15% reach orgânico'
            },
            {
                'priority': 'Média',
                'category': 'Engajamento',
                'suggestion': 'Incluir pergunta interativa aos 2:30min',
                'impact': '+8% retention'
            },
            {
                'priority': 'Alta',
                'category': 'CTA',
                'suggestion': 'Reforçar call-to-action no final do vídeo',
                'impact': '+22% conversão'
            }
        ]
        
        for sugg in suggestions:
            priority_color = "🔴" if sugg['priority'] == 'Alta' else "🟡"
            st.markdown(f"""
            <div class="modern-card">
                <strong>{priority_color} {sugg['priority']} - {sugg['category']}</strong><br>
                {sugg['suggestion']}<br>
                <small style="color: #28a745;">📈 Impacto esperado: {sugg['impact']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🏷️ Tags Otimizadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Tags Atuais:**")
            current_tags = ["marketing digital", "vendas", "estratégia"]
            for tag in current_tags:
                st.markdown(f"• {tag}")
        
        with col2:
            st.markdown("**Tags Sugeridas pela IA:**")
            suggested_tags = [
                "funil de vendas", "conversão", "roi marketing", 
                "tráfego pago", "lead generation", "crm vendas"
            ]
            for tag in suggested_tags:
                st.markdown(f"• {tag} ⭐")
    
    with tab4:
        st.markdown("### 📈 Projeção de Performance")
        
        # Gráfico de projeção
        data = {
            'Métrica': ['Views', 'Curtidas', 'Comentários', 'Compartilhamentos', 'Inscritos'],
            'Atual': [1200, 85, 12, 8, 15],
            'Projeção Otimizada': [1800, 140, 22, 18, 28]
        }
        
        df = pd.DataFrame(data)
        
        fig = px.bar(df, x='Métrica', y=['Atual', 'Projeção Otimizada'], 
                     title="Comparação: Performance Atual vs Otimizada",
                     barmode='group')
        
        st.plotly_chart(fig, use_container_width=True)

def page_content_search():
    """Página de busca de conteúdos"""
    st.markdown("## 🔍 Busca Inteligente de Conteúdos")
    st.markdown("Encontre conteúdos relevantes e analise tendências de mercado.")
    
    # Container de busca
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input(
                "🔎 Digite sua busca:",
                placeholder="Ex: funil de vendas, roi tráfego pago, estratégias de marketing..."
            )
        
        with col2:
            search_button = st.button("Buscar", type="primary", use_container_width=True)
    
    # Filtros avançados
    with st.expander("🎛️ Filtros Avançados"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            persona_filter = st.selectbox("Persona:", ["Todas", "estrategico", "crescimento", "smart"])
        
        with col2:
            min_score = st.slider("Score mínimo:", 0.0, 10.0, 7.0)
        
        with col3:
            category_filter = st.selectbox("Categoria:", ["Todas", "Funil de Vendas", "Tráfego Pago", "Lead Generation"])
    
    # Exibir resultados
    if search_query or search_button:
        search_engine = ContentSearchEngine()
        
        filters = {}
        if persona_filter != "Todas":
            filters['persona'] = persona_filter
        if min_score > 0:
            filters['min_score'] = min_score
        
        results = search_engine.search_content(search_query, filters)
        
        if results:
            st.markdown(f"### 📋 Resultados ({len(results)} encontrados)")
            
            for result in results:
                with st.container():
                    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**{result['title']}**")
                        st.markdown(f"📂 {result['category']} | 👤 {result['persona']}")
                        st.markdown(f"🏷️ {', '.join(result['keywords'])}")
                    
                    with col2:
                        st.metric("Score", f"{result['performance_score']}/10")
                        st.metric("Views", f"{result['views']:,}")
                        st.metric("Engagement", f"{result['engagement_rate']}%")
                    
                    if st.button(f"Ver detalhes", key=f"detail_{result['title'][:20]}"):
                        st.info("🔜 Detalhes completos em breve...")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🔍 Nenhum resultado encontrado. Tente termos diferentes.")
    
    # Trending topics
    st.markdown("---")
    st.markdown("### 🔥 Tópicos em Alta")
    
    search_engine = ContentSearchEngine()
    trending = search_engine.get_trending_topics()
    
    cols = st.columns(len(trending))
    
    for i, topic in enumerate(trending):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">
                    {topic['topic']}
                </div>
                <div class="metric-value" style="font-size: 1.5rem;">
                    {topic['growth']}
                </div>
                <div class="metric-label">
                    {topic['searches']:,} buscas
                </div>
            </div>
            """, unsafe_allow_html=True)

# Função principal
def main():
    """Função principal do dashboard"""
    load_custom_css()
    render_header()
    
    # Navegação
    current_page = render_sidebar()
    
    # Renderizar página selecionada
    if current_page == "📝 Inserir Transcrição":
        page_transcription_input()
    elif current_page == "🔍 Buscar Conteúdos":
        page_content_search()
    elif current_page == "📊 Analytics Avançado":
        st.markdown("## 📊 Analytics Avançado")
        st.info("🔜 Seção em desenvolvimento - Integrando com YouTube Analytics API...")
    elif current_page == "🏆 Análise Competitiva":
        st.markdown("## 🏆 Análise Competitiva")
        st.info("🔜 Seção em desenvolvimento - Sistema de análise de concorrentes...")
    elif current_page == "💡 Sugestões IA":
        st.markdown("## 💡 Sugestões de Conteúdo com IA")
        st.info("🔜 Seção em desenvolvimento - Gerador de ideias baseado em CHAVI...")
    else:  # Configurações
        st.markdown("## ⚙️ Configurações")
        st.info("🔜 Seção em desenvolvimento - Configurações do sistema...")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 1rem;">
        🚀 <strong>F5 Estratégia</strong> - Sistema de Otimização YouTube com IA<br>
        <small>Desenvolvido com ❤️ para maximizar resultados no YouTube</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 