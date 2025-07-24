"""
Competitor Analyzer - Sistema de Análise de Concorrentes e Tendências
Desenvolvido para F5 Estratégia
"""

import logging
import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from collections import Counter
import re
import statistics

from youtube_api_manager import YouTubeDataCollector, YouTubeAPIManager
from content_optimizer import ContentOptimizer
from config import F5Config, YouTubeConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompetitorDiscovery:
    """Sistema para descobrir e mapear concorrentes"""
    
    def __init__(self, data_collector: YouTubeDataCollector):
        self.data_collector = data_collector
        self.core_keywords = F5Config.CORE_KEYWORDS
        
        # Canais conhecidos do nicho (podem ser expandidos)
        self.known_competitors = [
            'UC-3jIAlnQmbbVMV6gR7K8aQ',  # Erico Rocha
            'UCKdUKlyLH8k5HMhyaGW7dcA',  # Hotmart
            'UCaGLf-iHBVlAFYEONbzGpwg',  # Klober
            # Adicionar mais conforme identificação
        ]
    
    def discover_competitors_by_keywords(self, keywords: List[str], max_channels: int = 20) -> List[Dict[str, Any]]:
        """
        Descobre concorrentes baseado em palavras-chave
        
        Args:
            keywords: Lista de palavras-chave para busca
            max_channels: Número máximo de canais a descobrir
        
        Returns:
            Lista de dados dos canais concorrentes
        """
        competitors = {}
        
        for keyword in keywords:
            try:
                # Buscar vídeos por palavra-chave
                videos = self.data_collector.search_competitor_videos(keyword, max_results=50)
                
                for video in videos:
                    channel_id = video['channel_id']
                    channel_title = video['channel_title']
                    
                    if channel_id not in competitors:
                        competitors[channel_id] = {
                            'channel_id': channel_id,
                            'channel_title': channel_title,
                            'video_count': 0,
                            'keywords_found': set(),
                            'avg_views': 0,
                            'total_views': 0,
                            'videos': []
                        }
                    
                    competitors[channel_id]['video_count'] += 1
                    competitors[channel_id]['keywords_found'].add(keyword)
                    competitors[channel_id]['videos'].append(video)
                
            except Exception as e:
                logger.error(f"Erro ao buscar por '{keyword}': {e}")
        
        # Processar dados dos concorrentes
        processed_competitors = []
        for competitor_data in competitors.values():
            if competitor_data['video_count'] >= 3:  # Filtrar canais com pelo menos 3 vídeos
                # Obter detalhes dos vídeos
                video_ids = [v['video_id'] for v in competitor_data['videos'][:10]]
                video_details = self.data_collector.get_video_details(video_ids)
                
                if video_details:
                    total_views = sum(v['view_count'] for v in video_details)
                    competitor_data['total_views'] = total_views
                    competitor_data['avg_views'] = total_views / len(video_details)
                    competitor_data['keywords_found'] = list(competitor_data['keywords_found'])
                    competitor_data['video_details'] = video_details
                
                processed_competitors.append(competitor_data)
        
        # Ordenar por relevância (views médias + número de keywords)
        processed_competitors.sort(
            key=lambda x: x['avg_views'] * len(x['keywords_found']), 
            reverse=True
        )
        
        return processed_competitors[:max_channels]
    
    def analyze_competitor_channel(self, channel_id: str) -> Dict[str, Any]:
        """
        Análise detalhada de um canal concorrente específico
        
        Args:
            channel_id: ID do canal a analisar
        
        Returns:
            Análise completa do canal
        """
        try:
            # Para análise completa, precisaríamos da Channel API
            # Por ora, vamos simular com dados disponíveis
            channel_analysis = {
                'channel_id': channel_id,
                'analysis_date': datetime.now().isoformat(),
                'video_analysis': {},
                'content_strategy': {},
                'performance_metrics': {}
            }
            
            return channel_analysis
            
        except Exception as e:
            logger.error(f"Erro ao analisar canal {channel_id}: {e}")
            return {}

class TrendAnalyzer:
    """Analisador de tendências de conteúdo"""
    
    def __init__(self, data_collector: YouTubeDataCollector):
        self.data_collector = data_collector
        self.content_optimizer = ContentOptimizer()
    
    def analyze_trending_topics(self, keywords: List[str], days_back: int = 30) -> Dict[str, Any]:
        """
        Analisa tópicos em tendência
        
        Args:
            keywords: Palavras-chave para análise
            days_back: Número de dias para análise histórica
        
        Returns:
            Análise de tendências
        """
        trends_data = {
            'analysis_period': f"Últimos {days_back} dias",
            'keywords_analyzed': keywords,
            'trending_topics': [],
            'content_opportunities': [],
            'performance_patterns': {}
        }
        
        all_videos = []
        
        # Coletar vídeos para cada palavra-chave
        for keyword in keywords:
            try:
                videos = self.data_collector.search_competitor_videos(
                    keyword, 
                    max_results=25
                )
                
                # Filtrar por data (últimos X dias)
                filtered_videos = []
                cutoff_date = datetime.now() - timedelta(days=days_back)
                
                for video in videos:
                    video_date = datetime.fromisoformat(video['published_at'].replace('Z', '+00:00'))
                    if video_date >= cutoff_date:
                        video['keyword_source'] = keyword
                        filtered_videos.append(video)
                
                all_videos.extend(filtered_videos)
                
            except Exception as e:
                logger.error(f"Erro ao analisar tendências para '{keyword}': {e}")
        
        if all_videos:
            # Obter detalhes dos vídeos
            video_ids = [v['video_id'] for v in all_videos[:100]]  # Limitar para não sobrecarregar
            video_details = self.data_collector.get_video_details(video_ids)
            
            if video_details:
                trends_data.update(self._analyze_video_trends(video_details, keywords))
        
        return trends_data
    
    def _analyze_video_trends(self, videos: List[Dict[str, Any]], keywords: List[str]) -> Dict[str, Any]:
        """Analisa tendências nos vídeos coletados"""
        
        # Análise de títulos
        title_words = []
        for video in videos:
            title_words.extend(video['title'].lower().split())
        
        # Encontrar palavras mais frequentes (excluindo stopwords)
        stopwords = {'de', 'da', 'do', 'para', 'com', 'em', 'no', 'na', 'e', 'o', 'a', 'que', 'como', 'por'}
        filtered_words = [word for word in title_words if len(word) > 3 and word not in stopwords]
        word_freq = Counter(filtered_words)
        
        # Análise de performance
        view_counts = [v['view_count'] for v in videos]
        like_counts = [v['like_count'] for v in videos]
        
        performance_stats = {
            'avg_views': statistics.mean(view_counts) if view_counts else 0,
            'median_views': statistics.median(view_counts) if view_counts else 0,
            'avg_likes': statistics.mean(like_counts) if like_counts else 0,
            'total_videos': len(videos)
        }
        
        # Identificar padrões de títulos de sucesso
        high_performing_videos = sorted(videos, key=lambda x: x['view_count'], reverse=True)[:10]
        title_patterns = self._extract_title_patterns(high_performing_videos)
        
        # Análise de tags
        all_tags = []
        for video in videos:
            all_tags.extend(video.get('tags', []))
        
        tag_freq = Counter([tag.lower() for tag in all_tags])
        
        return {
            'trending_topics': word_freq.most_common(20),
            'performance_patterns': performance_stats,
            'title_patterns': title_patterns,
            'popular_tags': tag_freq.most_common(15),
            'content_opportunities': self._identify_content_gaps(videos, keywords)
        }
    
    def _extract_title_patterns(self, videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extrai padrões de títulos de alto desempenho"""
        patterns = []
        
        for video in videos:
            title = video['title']
            pattern_analysis = {
                'title': title,
                'view_count': video['view_count'],
                'length': len(title),
                'has_numbers': bool(re.search(r'\d+', title)),
                'has_question': '?' in title,
                'has_exclamation': '!' in title,
                'starts_with_how': title.lower().startswith('como'),
                'emotional_words': self._count_emotional_words(title)
            }
            patterns.append(pattern_analysis)
        
        return patterns
    
    def _count_emotional_words(self, title: str) -> int:
        """Conta palavras emocionais no título"""
        emotional_words = [
            'segredo', 'incrível', 'surpreendente', 'exclusivo', 'urgente',
            'definitivo', 'completo', 'essencial', 'revolucionário', 'simples',
            'rápido', 'eficaz', 'comprovado', 'garantido'
        ]
        title_lower = title.lower()
        return sum(1 for word in emotional_words if word in title_lower)
    
    def _identify_content_gaps(self, videos: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """Identifica lacunas de conteúdo (oportunidades)"""
        gaps = []
        
        # Análise de keywords não exploradas
        all_titles = ' '.join([v['title'].lower() for v in videos])
        
        keyword_combinations = [
            'marketing digital + automação',
            'vendas online + funil',
            'tráfego pago + conversão',
            'crm + integração',
            'leads + qualificação'
        ]
        
        for combination in keyword_combinations:
            keywords_in_combo = combination.split(' + ')
            if all(kw in all_titles for kw in keywords_in_combo):
                # Tópico já bem explorado
                continue
            else:
                # Oportunidade identificada
                gaps.append({
                    'topic': combination,
                    'opportunity_level': 'Alta',
                    'reason': 'Pouco conteúdo encontrado para esta combinação',
                    'suggested_angle': f'Como integrar {keywords_in_combo[0]} com {keywords_in_combo[1]}'
                })
        
        return gaps

class CompetitorAnalyzer:
    """Analisador principal de concorrentes"""
    
    def __init__(self, api_manager: YouTubeAPIManager):
        self.api_manager = api_manager
        self.data_collector = YouTubeDataCollector(api_manager)
        self.competitor_discovery = CompetitorDiscovery(self.data_collector)
        self.trend_analyzer = TrendAnalyzer(self.data_collector)
        self.content_optimizer = ContentOptimizer()
    
    def generate_competitive_analysis(self, focus_keywords: List[str] = None) -> Dict[str, Any]:
        """
        Gera análise competitiva completa
        
        Args:
            focus_keywords: Palavras-chave específicas para focar
        
        Returns:
            Relatório completo de análise competitiva
        """
        if not focus_keywords:
            focus_keywords = F5Config.CORE_KEYWORDS[:5]  # Usar top 5 keywords
        
        logger.info(f"Iniciando análise competitiva para: {', '.join(focus_keywords)}")
        
        analysis_report = {
            'analysis_date': datetime.now().isoformat(),
            'keywords_analyzed': focus_keywords,
            'competitors': [],
            'trends': {},
            'content_opportunities': [],
            'recommendations': []
        }
        
        try:
            # 1. Descobrir concorrentes
            logger.info("Descobrindo concorrentes...")
            competitors = self.competitor_discovery.discover_competitors_by_keywords(
                focus_keywords, 
                max_channels=15
            )
            analysis_report['competitors'] = competitors
            
            # 2. Analisar tendências
            logger.info("Analisando tendências...")
            trends = self.trend_analyzer.analyze_trending_topics(focus_keywords)
            analysis_report['trends'] = trends
            
            # 3. Identificar oportunidades de conteúdo
            analysis_report['content_opportunities'] = self._identify_content_opportunities(
                competitors, trends
            )
            
            # 4. Gerar recomendações estratégicas
            analysis_report['recommendations'] = self._generate_strategic_recommendations(
                competitors, trends
            )
            
            logger.info("Análise competitiva concluída")
            
        except Exception as e:
            logger.error(f"Erro na análise competitiva: {e}")
            analysis_report['error'] = str(e)
        
        return analysis_report
    
    def _identify_content_opportunities(self, competitors: List[Dict], trends: Dict) -> List[Dict[str, Any]]:
        """Identifica oportunidades específicas de conteúdo"""
        opportunities = []
        
        # Análise de lacunas baseada em concorrentes
        if competitors and trends:
            # Encontrar tópicos com boa performance mas pouca saturação
            trending_topics = trends.get('trending_topics', [])
            
            for topic, frequency in trending_topics[:10]:
                # Verificar se F5 já tem conteúdo sobre este tópico
                opportunity = {
                    'topic': topic,
                    'trend_score': frequency,
                    'competition_level': self._assess_competition_level(topic, competitors),
                    'recommended_angle': self._suggest_f5_angle(topic),
                    'target_persona': self._suggest_target_persona(topic),
                    'priority': 'Alta'
                }
                opportunities.append(opportunity)
        
        return opportunities[:15]  # Top 15 oportunidades
    
    def _assess_competition_level(self, topic: str, competitors: List[Dict]) -> str:
        """Avalia nível de competição para um tópico"""
        topic_mentions = 0
        total_videos = 0
        
        for competitor in competitors:
            for video in competitor.get('video_details', []):
                total_videos += 1
                if topic.lower() in video['title'].lower() or topic.lower() in video['description'].lower():
                    topic_mentions += 1
        
        if total_videos == 0:
            return 'Baixa'
        
        mention_rate = topic_mentions / total_videos
        
        if mention_rate < 0.1:
            return 'Baixa'
        elif mention_rate < 0.3:
            return 'Média'
        else:
            return 'Alta'
    
    def _suggest_f5_angle(self, topic: str) -> str:
        """Sugere ângulo específico da F5 para o tópico"""
        f5_angles = {
            'dados': 'Como usar dados para tomar decisões de marketing mais inteligentes',
            'automação': 'Automação de marketing que gera resultados reais',
            'conversão': 'Estratégias de conversão baseadas na metodologia CHAVI',
            'performance': 'Performance marketing com foco em ROI comprovado',
            'leads': 'Geração de leads qualificados que realmente vendem'
        }
        
        for key, angle in f5_angles.items():
            if key in topic.lower():
                return angle
        
        return f"Como a metodologia CHAVI pode otimizar {topic} para melhores resultados"
    
    def _suggest_target_persona(self, topic: str) -> str:
        """Sugere persona alvo baseada no tópico"""
        persona_mapping = {
            'roi': 'estrategico',
            'kpi': 'estrategico',
            'dashboard': 'estrategico',
            'funil': 'crescimento',
            'processo': 'crescimento',
            'estruturar': 'crescimento',
            'rápido': 'smart',
            'simples': 'smart',
            'básico': 'smart'
        }
        
        topic_lower = topic.lower()
        for keyword, persona in persona_mapping.items():
            if keyword in topic_lower:
                return persona
        
        return 'crescimento'  # Default para persona de crescimento
    
    def _generate_strategic_recommendations(self, competitors: List[Dict], trends: Dict) -> List[str]:
        """Gera recomendações estratégicas baseadas na análise"""
        recommendations = []
        
        if competitors:
            avg_competitor_views = statistics.mean([c['avg_views'] for c in competitors if c['avg_views'] > 0])
            
            recommendations.extend([
                f"Benchmark de performance: Concorrentes têm média de {avg_competitor_views:,.0f} visualizações",
                "Foque em conteúdos com base na metodologia CHAVI para diferenciação",
                "Aproveite lacunas identificadas nos tópicos de tendência"
            ])
        
        if trends and trends.get('trending_topics'):
            top_trend = trends['trending_topics'][0][0] if trends['trending_topics'] else 'marketing digital'
            recommendations.append(f"Crie conteúdo sobre '{top_trend}' com ângulo da F5 Estratégia")
        
        # Recomendações específicas da metodologia CHAVI
        recommendations.extend([
            "Integre dados de performance real nos vídeos (pilar I - Inteligência)",
            "Use cases de clientes reais para humanizar o conteúdo (pilar H)",
            "Inclua CTAs claros para geração de leads (pilar V - Vendas)",
            "Otimize títulos e descrições com base nas análises de SEO"
        ])
        
        return recommendations

def create_competitor_analyzer(api_manager: YouTubeAPIManager) -> CompetitorAnalyzer:
    """Factory function para criar o analisador de concorrentes"""
    return CompetitorAnalyzer(api_manager)

if __name__ == "__main__":
    # Teste básico
    from youtube_api_manager import initialize_youtube_system
    
    try:
        system = initialize_youtube_system()
        analyzer = create_competitor_analyzer(system['api_manager'])
        
        # Executar análise com palavras-chave de teste
        test_keywords = ['marketing digital', 'tráfego pago']
        analysis = analyzer.generate_competitive_analysis(test_keywords)
        
        print("Análise competitiva concluída!")
        print(f"Concorrentes encontrados: {len(analysis.get('competitors', []))}")
        print(f"Oportunidades identificadas: {len(analysis.get('content_opportunities', []))}")
        
    except Exception as e:
        logger.error(f"Erro no teste: {e}") 