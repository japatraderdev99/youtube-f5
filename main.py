"""
Sistema Principal de Otimização YouTube - F5 Estratégia
Desenvolvido para maximizar performance, SEO e geração de leads no YouTube

Este sistema integra:
- APIs nativas do YouTube (Analytics e Data API v3)
- Otimização de conteúdo com IA baseada na metodologia CHAVI
- Análise de concorrentes e tendências
- Dashboard em tempo real
- Geração de leads integrada

Autor: Sistema F5 Estratégia
"""

import os
import sys
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

# Imports locais
from youtube_api_manager import initialize_youtube_system
from content_optimizer import ContentOptimizer
from competitor_analyzer import CompetitorAnalyzer
from dashboard import create_f5_dashboard
from config import validate_config, AppConfig, F5Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class F5YouTubeOptimizer:
    """Classe principal do sistema de otimização YouTube da F5"""
    
    def __init__(self):
        """Inicializa o sistema completo"""
        print("🚀 Iniciando Sistema de Otimização YouTube - F5 Estratégia")
        print("=" * 60)
        
        try:
            # Validar configurações
            validate_config()
            
            # Criar diretórios necessários
            AppConfig.ensure_directories()
            
            # Inicializar sistemas
            self.youtube_system = initialize_youtube_system()
            self.content_optimizer = ContentOptimizer()
            self.competitor_analyzer = CompetitorAnalyzer(self.youtube_system['api_manager'])
            
            print("✅ Sistema inicializado com sucesso!")
            self._print_system_info()
            
        except Exception as e:
            logger.error(f"Erro ao inicializar sistema: {e}")
            print(f"❌ Erro na inicialização: {e}")
            sys.exit(1)
    
    def _print_system_info(self):
        """Exibe informações do sistema"""
        print("\n📋 Informações do Sistema:")
        print(f"📁 Diretório de dados: {AppConfig.DATA_DIR}")
        print(f"📊 Diretório de relatórios: {AppConfig.REPORTS_DIR}")
        print(f"📝 Diretório de logs: {AppConfig.LOGS_DIR}")
        print(f"🎯 Canal: {F5Config.BRAND_ARCHETYPES['primary']} + {F5Config.BRAND_ARCHETYPES['secondary']}")
        print(f"🔧 Metodologia: CHAVI ({', '.join(F5Config.CHAVI_PILLARS.values())})")
        print("=" * 60)
    
    def analyze_channel_performance(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Analisa performance do canal nos últimos X dias
        
        Args:
            days_back: Número de dias para análise
        
        Returns:
            Dict com dados de performance
        """
        print(f"\n🔍 Analisando performance do canal (últimos {days_back} dias)...")
        
        try:
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            # Coletar dados do Analytics
            performance_data = self.youtube_system['analytics_collector'].get_channel_performance(
                start_date, end_date
            )
            
            traffic_data = self.youtube_system['analytics_collector'].get_traffic_sources(
                start_date, end_date
            )
            
            demographics_data = self.youtube_system['analytics_collector'].get_audience_demographics(
                start_date, end_date
            )
            
            analysis_result = {
                'period': f"{start_date} a {end_date}",
                'performance': performance_data,
                'traffic_sources': traffic_data,
                'demographics': demographics_data,
                'analysis_date': datetime.now().isoformat()
            }
            
            # Salvar relatório
            self._save_report('channel_performance', analysis_result)
            print("✅ Análise de performance concluída!")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Erro na análise de performance: {e}")
            return {}
    
    def optimize_video_content(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Otimiza conteúdo de um vídeo específico
        
        Args:
            video_data: Dados do vídeo (título, descrição, tags)
        
        Returns:
            Análise e sugestões de otimização
        """
        print(f"\n🎯 Otimizando conteúdo: '{video_data.get('title', 'Sem título')}'...")
        
        try:
            # Executar análise completa
            optimization_result = self.content_optimizer.optimize_existing_content(video_data)
            
            # Exibir resultados principais
            analysis = optimization_result['analysis']
            print(f"📊 Score SEO: {analysis.seo_score}/10")
            print(f"👥 Persona alvo: {analysis.persona_target}")
            print(f"🚀 Potencial de melhoria: {optimization_result['improvement_potential']:.1f} pontos")
            
            # Salvar relatório
            self._save_report('content_optimization', optimization_result)
            print("✅ Otimização de conteúdo concluída!")
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Erro na otimização de conteúdo: {e}")
            return {}
    
    def analyze_competitors(self, keywords: List[str] = None) -> Dict[str, Any]:
        """
        Executa análise competitiva completa
        
        Args:
            keywords: Palavras-chave para análise (usa defaults se None)
        
        Returns:
            Relatório de análise competitiva
        """
        if not keywords:
            keywords = F5Config.CORE_KEYWORDS[:5]
        
        print(f"\n🏆 Executando análise competitiva para: {', '.join(keywords)}")
        
        try:
            analysis_result = self.competitor_analyzer.generate_competitive_analysis(keywords)
            
            # Exibir resumo
            competitors_count = len(analysis_result.get('competitors', []))
            opportunities_count = len(analysis_result.get('content_opportunities', []))
            
            print(f"📊 Concorrentes identificados: {competitors_count}")
            print(f"💡 Oportunidades encontradas: {opportunities_count}")
            
            # Salvar relatório
            self._save_report('competitive_analysis', analysis_result)
            print("✅ Análise competitiva concluída!")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Erro na análise competitiva: {e}")
            return {}
    
    def generate_content_suggestions(self, persona: str = 'crescimento', count: int = 5) -> List[Dict[str, Any]]:
        """
        Gera sugestões de conteúdo baseadas na metodologia CHAVI
        
        Args:
            persona: Persona alvo ('estrategico', 'crescimento', 'smart')
            count: Número de sugestões a gerar
        
        Returns:
            Lista de sugestões de conteúdo
        """
        print(f"\n💡 Gerando {count} sugestões de conteúdo para persona: {persona}")
        
        try:
            persona_info = F5Config.PERSONAS[persona]
            suggestions = []
            
            # Templates de conteúdo baseados na metodologia CHAVI
            chavi_templates = {
                'C': [
                    "Como criar uma estratégia de {topic} que realmente funciona",
                    "Planejamento de {topic}: O guia completo para {persona_focus}",
                    "Pesquisa de mercado para {topic}: Métodos comprovados"
                ],
                'H': [
                    "Cases reais: Como transformamos {topic} em resultados",
                    "A história por trás dos melhores {topic}",
                    "Humanizando {topic}: Conectando com sua audiência"
                ],
                'A': [
                    "Performance em {topic}: Métricas que importam",
                    "Como otimizar {topic} para máxima conversão",
                    "Anúncios de {topic} que geram ROI"
                ],
                'V': [
                    "De {topic} para vendas: O processo completo",
                    "Como {topic} pode triplicar seus leads",
                    "Convertendo {topic} em oportunidades de negócio"
                ],
                'I': [
                    "Dados de {topic}: Insights que você não conhecia",
                    "Analytics de {topic}: Como interpretar e agir",
                    "BI em {topic}: Dashboards que geram resultados"
                ]
            }
            
            # Gerar sugestões para cada pilar CHAVI
            for pilar, templates in chavi_templates.items():
                if len(suggestions) >= count:
                    break
                
                for template in templates:
                    if len(suggestions) >= count:
                        break
                    
                    # Escolher tópico baseado na persona
                    if persona == 'estrategico':
                        topic = 'marketing digital'
                        focus = 'crescimento sustentável'
                    elif persona == 'crescimento':
                        topic = 'tráfego pago'
                        focus = 'estruturação de funil'
                    else:  # smart
                        topic = 'leads'
                        focus = 'resultados rápidos'
                    
                    suggestion = {
                        'title': template.format(topic=topic, persona_focus=focus),
                        'chavi_pillar': F5Config.CHAVI_PILLARS[pilar],
                        'target_persona': persona,
                        'estimated_length': '8-12 minutos',
                        'key_points': self._generate_key_points(pilar, topic),
                        'cta_suggestion': self._generate_cta(persona),
                        'tags_suggestion': self._generate_tags(topic, persona)
                    }
                    suggestions.append(suggestion)
            
            # Salvar relatório
            self._save_report('content_suggestions', {
                'persona': persona,
                'suggestions': suggestions[:count],
                'generation_date': datetime.now().isoformat()
            })
            
            print("✅ Sugestões de conteúdo geradas!")
            return suggestions[:count]
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões: {e}")
            return []
    
    def _generate_key_points(self, pilar: str, topic: str) -> List[str]:
        """Gera pontos-chave baseados no pilar CHAVI"""
        key_points_templates = {
            'C': [
                f"Pesquisa de mercado para {topic}",
                f"Definição de público-alvo específico",
                f"Planejamento estratégico com mapa mental"
            ],
            'H': [
                f"Cases reais de sucesso com {topic}",
                f"Storytelling aplicado ao {topic}",
                f"Técnicas de oratória para vídeos"
            ],
            'A': [
                f"Configuração de campanhas de {topic}",
                f"Otimização de performance",
                f"Análise de ROI e conversões"
            ],
            'V': [
                f"Processo de qualificação de leads",
                f"CRM e acompanhamento de vendas",
                f"Scripts de abordagem eficazes"
            ],
            'I': [
                f"Métricas essenciais de {topic}",
                f"Dashboards e relatórios em tempo real",
                f"Interpretação de dados para decisões"
            ]
        }
        return key_points_templates.get(pilar, [])
    
    def _generate_cta(self, persona: str) -> str:
        """Gera CTA específico por persona"""
        ctas = {
            'estrategico': "Agende uma consultoria estratégica para escalar seu marketing digital",
            'crescimento': "Baixe nosso guia completo de estruturação de funil de vendas",
            'smart': "Acesse nossa planilha gratuita de controle de leads"
        }
        return ctas.get(persona, "Entre em contato para uma análise personalizada")
    
    def _generate_tags(self, topic: str, persona: str) -> List[str]:
        """Gera tags relevantes"""
        base_tags = F5Config.CORE_KEYWORDS[:5]
        persona_tags = {
            'estrategico': ['roi', 'kpi', 'escalabilidade'],
            'crescimento': ['funil', 'processo', 'estruturação'],
            'smart': ['rápido', 'prático', 'essencial']
        }
        return base_tags + persona_tags.get(persona, [])
    
    def _save_report(self, report_type: str, data: Dict[str, Any]):
        """Salva relatório em arquivo JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_type}_{timestamp}.json"
        filepath = os.path.join(AppConfig.REPORTS_DIR, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Relatório salvo: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")
    
    def run_dashboard(self):
        """Inicia o dashboard web"""
        print("\n🚀 Iniciando Dashboard Web...")
        dashboard = create_f5_dashboard()
        dashboard.run_server(debug=False, port=8050)
    
    def run_complete_analysis(self):
        """Executa análise completa do sistema"""
        print("\n🔄 Executando análise completa do sistema...")
        
        results = {
            'analysis_date': datetime.now().isoformat(),
            'channel_performance': None,
            'competitive_analysis': None,
            'content_suggestions': None
        }
        
        try:
            # 1. Análise de performance do canal
            results['channel_performance'] = self.analyze_channel_performance()
            
            # 2. Análise competitiva
            results['competitive_analysis'] = self.analyze_competitors()
            
            # 3. Sugestões de conteúdo para cada persona
            for persona in ['estrategico', 'crescimento', 'smart']:
                suggestions = self.generate_content_suggestions(persona, 3)
                results[f'content_suggestions_{persona}'] = suggestions
            
            # Salvar análise completa
            self._save_report('complete_analysis', results)
            
            print("\n✅ Análise completa finalizada!")
            print("📊 Todos os relatórios foram salvos no diretório de reports")
            
            return results
            
        except Exception as e:
            logger.error(f"Erro na análise completa: {e}")
            return results

def main():
    """Função principal com interface CLI"""
    parser = argparse.ArgumentParser(
        description="Sistema de Otimização YouTube - F5 Estratégia"
    )
    
    parser.add_argument(
        '--mode', 
        choices=['dashboard', 'analysis', 'optimize', 'competitors', 'suggestions'],
        default='dashboard',
        help='Modo de operação do sistema'
    )
    
    parser.add_argument('--title', help='Título do vídeo para otimização')
    parser.add_argument('--description', help='Descrição do vídeo para otimização')
    parser.add_argument('--tags', help='Tags do vídeo (separadas por vírgula)')
    parser.add_argument('--persona', choices=['estrategico', 'crescimento', 'smart'], 
                       default='crescimento', help='Persona alvo')
    parser.add_argument('--days', type=int, default=30, help='Dias para análise histórica')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    optimizer = F5YouTubeOptimizer()
    
    if args.mode == 'dashboard':
        optimizer.run_dashboard()
    
    elif args.mode == 'analysis':
        optimizer.run_complete_analysis()
    
    elif args.mode == 'optimize':
        if not args.title:
            print("❌ Título é obrigatório para otimização")
            return
        
        video_data = {
            'title': args.title,
            'description': args.description or '',
            'tags': args.tags.split(',') if args.tags else []
        }
        optimizer.optimize_video_content(video_data)
    
    elif args.mode == 'competitors':
        optimizer.analyze_competitors()
    
    elif args.mode == 'suggestions':
        suggestions = optimizer.generate_content_suggestions(args.persona)
        print("\n💡 Sugestões de Conteúdo:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['title']}")
            print(f"   Pilar CHAVI: {suggestion['chavi_pillar']}")
            print(f"   Persona: {suggestion['target_persona']}")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Sistema finalizado pelo usuário")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        print(f"❌ Erro fatal: {e}")
        sys.exit(1) 