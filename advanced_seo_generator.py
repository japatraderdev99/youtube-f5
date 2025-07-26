"""
Gerador Avançado de SEO para YouTube - F5 Estratégia
Sistema integrado com API do YouTube para otimização completa
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

# Importa o sistema base
from video_seo_optimizer import VideoSEOOptimizer, TranscriptionAnalyzer, SEOContentGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedSEOGenerator:
    """Gerador avançado de SEO com detecção inteligente de temas"""
    
    def __init__(self):
        self.base_optimizer = VideoSEOOptimizer()
        self.analyzer = TranscriptionAnalyzer()
        self.specific_themes = self._load_specific_themes()
    
    def _load_specific_themes(self) -> Dict[str, Dict]:
        """Carrega temas específicos com templates otimizados"""
        return {
            'autorresponsabilidade': {
                'keywords': [
                    'autorresponsabilidade', 'autoconhecimento', 'responsabilidade', 'consciência',
                    'desenvolvimento pessoal', 'reflexão', 'crescimento', 'valores', 'decisões',
                    'comportamento', 'mudança', 'transformação', 'atitude', 'escolhas'
                ],
                'title_templates': [
                    "Autorresponsabilidade: O Segredo do Sucesso Profissional | F5 Estratégia",
                    "Como Desenvolver Autorresponsabilidade e Transformar sua Carreira | F5",
                    "Autorresponsabilidade na Prática: Estratégias Comprovadas | F5 Estratégia",
                    "O Poder da Autorresponsabilidade para Empresários | F5 Estratégia",
                    "Desenvolva Autorresponsabilidade em 30 Dias | Método F5 Estratégia"
                ],
                'description_intro': "Descubra como a autorresponsabilidade pode transformar sua vida profissional e pessoal. Neste vídeo, exploramos estratégias práticas para desenvolver consciência, tomar melhores decisões e assumir controle total dos seus resultados.",
                'landing_page': 'https://f5estrategia.com/desenvolvimento-pessoal',
                'cta': "Transforme sua mentalidade e alcance resultados extraordinários"
            },
            'lideranca': {
                'keywords': [
                    'liderança', 'gestão', 'equipe', 'management', 'líder', 'time',
                    'performance', 'motivação', 'engajamento', 'cultura organizacional',
                    'comunicação', 'feedback', 'desenvolvimento de talentos'
                ],
                'title_templates': [
                    "Liderança de Alta Performance: Estratégias Comprovadas | F5",
                    "Como Liderar Equipes de Sucesso | Método F5 Estratégia",
                    "Gestão de Equipes: Técnicas que Funcionam | F5 Estratégia",
                    "Liderança Eficaz para Empresários | F5 Estratégia",
                    "Desenvolva sua Liderança em 30 Dias | F5 Estratégia"
                ],
                'description_intro': "Aprenda as estratégias de liderança que transformam equipes comuns em times de alta performance. Técnicas práticas para motivar, engajar e desenvolver talentos em sua organização.",
                'landing_page': 'https://f5estrategia.com/gestao-equipes',
                'cta': "Torne-se um líder extraordinário"
            },
            'comunicacao': {
                'keywords': [
                    'comunicação', 'apresentação', 'oratória', 'persuasão', 'influência',
                    'networking', 'relacionamento', 'diálogo', 'escuta', 'clareza',
                    'storytelling', 'negociação', 'conflitos'
                ],
                'title_templates': [
                    "Comunicação Estratégica: Como Influenciar e Persuadir | F5",
                    "Domine a Arte da Comunicação Empresarial | F5 Estratégia",
                    "Comunicação de Alta Performance | Método F5 Estratégia",
                    "Como se Comunicar com Impacto | F5 Estratégia",
                    "Desenvolva sua Comunicação em 30 Dias | F5 Estratégia"
                ],
                'description_intro': "Descubra como dominar a comunicação estratégica para influenciar, persuadir e gerar resultados extraordinários em seus negócios e relacionamentos profissionais.",
                'landing_page': 'https://f5estrategia.com/comunicacao-estrategica',
                'cta': "Comunique-se com impacto e autoridade"
            },
            'vendas': {
                'keywords': [
                    'vendas', 'negociação', 'fechamento', 'prospecção', 'cliente',
                    'conversão', 'funil', 'leads', 'relacionamento comercial',
                    'objeções', 'argumentação', 'proposta', 'valor'
                ],
                'title_templates': [
                    "Técnicas de Vendas que Funcionam | F5 Estratégia",
                    "Como Vender Mais e Melhor | Método F5 Estratégia",
                    "Vendas de Alta Performance | F5 Estratégia",
                    "Domine a Arte da Negociação | F5 Estratégia",
                    "Aumente suas Vendas em 30 Dias | F5 Estratégia"
                ],
                'description_intro': "Aprenda as técnicas de vendas e negociação que os profissionais de sucesso usam para fechar mais negócios e aumentar sua receita de forma consistente.",
                'landing_page': 'https://f5estrategia.com/vendas-estrategicas',
                'cta': "Multiplique seus resultados em vendas"
            }
        }
    
    def detect_specific_theme(self, transcription: str) -> Optional[str]:
        """Detecta tema específico com maior precisão"""
        clean_text = self.analyzer.clean_text(transcription).lower()
        
        theme_scores = {}
        
        for theme_name, theme_data in self.specific_themes.items():
            score = 0
            keywords = theme_data['keywords']
            
            for keyword in keywords:
                # Busca exata e variações
                if keyword.lower() in clean_text:
                    # Conta ocorrências
                    occurrences = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', clean_text))
                    score += occurrences * 2
                
                # Busca parcial para palavras compostas
                for word in keyword.split():
                    if len(word) > 3 and word in clean_text:
                        score += 1
            
            theme_scores[theme_name] = score
        
        # Retorna tema com maior score se significativo
        if theme_scores:
            max_theme = max(theme_scores, key=theme_scores.get)
            if theme_scores[max_theme] > 3:  # Threshold mínimo
                return max_theme
        
        return None
    
    def generate_optimized_content(self, transcription_file: str) -> Dict[str, any]:
        """Gera conteúdo SEO otimizado com detecção avançada"""
        try:
            # Lê transcrição
            with open(transcription_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
            
            # Detecta tema específico
            specific_theme = self.detect_specific_theme(transcription)
            
            if specific_theme:
                return self._generate_theme_specific_content(transcription, specific_theme, transcription_file)
            else:
                # Fallback para análise geral
                return self.base_optimizer.optimize_video_from_transcription(transcription_file)
                
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo otimizado: {e}")
            return {'error': str(e)}
    
    def _generate_theme_specific_content(self, transcription: str, theme: str, source_file: str) -> Dict[str, any]:
        """Gera conteúdo específico para tema detectado"""
        theme_data = self.specific_themes[theme]
        keywords = self.analyzer.extract_keywords(transcription, top_n=15)
        key_phrases = self.analyzer.extract_key_phrases(transcription, max_phrases=5)
        
        # Título otimizado para o tema
        title = self._select_best_title(theme_data['title_templates'], keywords)
        
        # Descrição especializada
        description = self._generate_theme_description(
            transcription, theme_data, title, keywords, key_phrases
        )
        
        # Tags específicas
        tags = self._generate_theme_tags(theme, keywords)
        
        # Metadados
        metadata = self._generate_theme_metadata(theme, title, keywords)
        
        return {
            'video_info': {
                'source_file': source_file,
                'optimization_date': datetime.now().isoformat(),
                'detected_theme': theme,
                'theme_confidence': 'high',
                'optimization_type': 'theme_specific'
            },
            'seo_content': {
                'title': {
                    'primary': title,
                    'alternatives': theme_data['title_templates'][:5],
                    'character_count': len(title),
                    'theme_optimized': True
                },
                'description': {
                    'content': description,
                    'character_count': len(description),
                    'within_limit': len(description) <= 5000,
                    'theme_optimized': True
                },
                'tags': {
                    'content': tags,
                    'count': len(tags),
                    'formatted': ' | '.join(tags),
                    'theme_optimized': True
                },
                'metadata': metadata
            },
            'keywords': {
                'primary': keywords,
                'theme_specific': theme_data['keywords'][:10],
                'key_phrases': key_phrases
            },
            'recommendations': self._generate_theme_recommendations(theme, len(transcription))
        }
    
    def _select_best_title(self, templates: List[str], keywords: List[Tuple[str, int]]) -> str:
        """Seleciona o melhor título baseado nas palavras-chave encontradas"""
        # Se há palavras-chave relevantes no conteúdo, mantém template padrão
        # Senão, adapta com palavras-chave do conteúdo
        
        if not keywords:
            return templates[0]
        
        # Verifica se alguma palavra-chave principal está nos templates
        top_keyword = keywords[0][0]
        
        for template in templates:
            if any(kw[0] in template.lower() for kw in keywords[:3]):
                return template
        
        # Se não encontrar match, retorna o primeiro template
        return templates[0]
    
    def _generate_theme_description(self, transcription: str, theme_data: Dict, 
                                   title: str, keywords: List, key_phrases: List) -> str:
        """Gera descrição específica para o tema"""
        
        intro = theme_data['description_intro']
        landing_page = theme_data['landing_page']
        cta = theme_data['cta']
        
        # Pontos principais (máximo 3)
        main_points = [phrase.strip() for phrase in key_phrases[:3] if len(phrase.strip()) > 30]
        
        # Top keywords para SEO
        top_keywords = [kw[0] for kw in keywords[:6]]
        
        description = f"""🎯 {title}

{intro}

📋 PRINCIPAIS PONTOS ABORDADOS:
"""
        
        # Adiciona pontos principais
        for i, point in enumerate(main_points, 1):
            description += f"\n✅ {point}"
        
        # Se não há pontos suficientes, adiciona pontos genéricos baseados no tema
        if len(main_points) < 2:
            theme_points = self._get_theme_default_points(theme_data)
            for point in theme_points[:3-len(main_points)]:
                description += f"\n✅ {point}"
        
        description += f"""

🔍 PALAVRAS-CHAVE PRINCIPAIS:
{' | '.join(top_keywords)}

🚀 {cta.upper()}:
Quer implementar essas estratégias no seu negócio? A F5 Estratégia oferece consultoria especializada para empresários que buscam crescimento sustentável e resultados extraordinários.

👉 Conheça nossos serviços: {landing_page}
📞 Agende uma consultoria gratuita: https://f5estrategia.com/contato

💡 METODOLOGIA CHAVI (F5 ESTRATÉGIA):
• Campanha - Estratégias de atração e posicionamento
• Humanização - Conexão autêntica com o público
• Anúncios - Tráfego pago otimizado e conversão
• Vendas - Processos estruturados e fechamento
• Inteligência - Dados e análises para decisões

🔔 INSCREVA-SE para mais conteúdos sobre:
• Desenvolvimento empresarial e pessoal
• Estratégias de marketing e vendas
• Liderança e gestão de equipes
• Crescimento sustentável de negócios
• Metodologias comprovadas F5

📱 CONECTE-SE CONOSCO:
🌐 Site: https://f5estrategia.com
📸 Instagram: @f5estrategia
💼 LinkedIn: F5 Estratégia
📞 WhatsApp: (11) 99999-9999

#F5Estrategia #{top_keywords[0].title().replace(' ', '')} #DesenvolvimentoProfissional #Empreendedorismo #MarketingDigital #Vendas #Lideranca #Gestao #Estrategia #Resultados #Sucesso #MetodologiaCHAVI

---
© 2025 F5 Estratégia - Todos os direitos reservados.
Transformando negócios através de estratégias comprovadas."""
        
        return description
    
    def _get_theme_default_points(self, theme_data: Dict) -> List[str]:
        """Retorna pontos padrão para cada tema quando não há suficientes na transcrição"""
        theme_name = None
        for name, data in self.specific_themes.items():
            if data == theme_data:
                theme_name = name
                break
        
        default_points = {
            'autorresponsabilidade': [
                "Como desenvolver consciência sobre suas escolhas e decisões",
                "Estratégias para assumir controle total dos seus resultados",
                "A diferença entre culpa e responsabilidade no crescimento profissional"
            ],
            'lideranca': [
                "Técnicas para motivar e engajar equipes de alta performance",
                "Como desenvolver uma cultura organizacional sólida",
                "Estratégias de feedback eficaz para desenvolvimento de talentos"
            ],
            'comunicacao': [
                "Técnicas de comunicação persuasiva e influência",
                "Como estruturar apresentações de impacto",
                "Estratégias para networking e relacionamentos profissionais"
            ],
            'vendas': [
                "Técnicas de fechamento e superação de objeções",
                "Como estruturar um processo de vendas eficaz",
                "Estratégias para aumentar conversão e ticket médio"
            ]
        }
        
        return default_points.get(theme_name, [])
    
    def _generate_theme_tags(self, theme: str, keywords: List) -> List[str]:
        """Gera tags específicas para o tema"""
        # Tags base F5
        base_tags = ['f5-estrategia', 'metodologia-chavi', 'empreendedorismo']
        
        # Tags específicas do tema
        theme_tags = {
            'autorresponsabilidade': [
                'autorresponsabilidade', 'autoconhecimento', 'desenvolvimento-pessoal',
                'crescimento-profissional', 'mindset', 'transformacao-pessoal',
                'consciencia', 'responsabilidade', 'mudanca-comportamental'
            ],
            'lideranca': [
                'lideranca', 'gestao-equipes', 'alta-performance', 'motivacao',
                'engajamento', 'cultura-organizacional', 'desenvolvimento-talentos',
                'feedback', 'management', 'lider'
            ],
            'comunicacao': [
                'comunicacao-estrategica', 'oratoria', 'apresentacao', 'persuasao',
                'influencia', 'networking', 'storytelling', 'negociacao',
                'relacionamento-profissional', 'comunicacao-empresarial'
            ],
            'vendas': [
                'vendas', 'negociacao', 'fechamento', 'conversao', 'funil-vendas',
                'prospecção', 'relacionamento-comercial', 'objecoes',
                'tecnicas-vendas', 'vendas-estrategicas'
            ]
        }
        
        # Tags do conteúdo (palavras-chave extraídas)
        content_tags = [kw[0].replace(' ', '-') for kw, freq in keywords[:5]]
        
        # Combina todas
        all_tags = base_tags + theme_tags.get(theme, []) + content_tags
        
        # Remove duplicatas e limita
        unique_tags = []
        seen = set()
        for tag in all_tags:
            if tag not in seen and len(tag) >= 3:
                unique_tags.append(tag)
                seen.add(tag)
                if len(unique_tags) >= 15:
                    break
        
        return unique_tags
    
    def _generate_theme_metadata(self, theme: str, title: str, keywords: List) -> Dict:
        """Gera metadados específicos para o tema"""
        return {
            'title': title,
            'description': f'{theme.title()} - Conteúdo F5 Estratégia',
            'keywords': '-'.join([kw[0] for kw in keywords[:8]]),
            'category': theme,
            'author': 'F5 Estratégia',
            'creation_date': datetime.now().strftime('%Y-%m-%d'),
            'theme': theme,
            'optimization_type': 'theme_specific',
            'optimization_version': '2.0'
        }
    
    def _generate_theme_recommendations(self, theme: str, content_length: int) -> List[str]:
        """Gera recomendações específicas para cada tema"""
        base_recommendations = [
            "Criar thumbnail com palavras-chave do tema em destaque",
            "Usar cards e end screens para direcionar para landing page específica",
            "Adicionar timestamps na descrição para melhor navegação",
            "Incluir call-to-action específico do tema nos primeiros 15 segundos"
        ]
        
        theme_recommendations = {
            'autorresponsabilidade': [
                "Criar série sobre desenvolvimento pessoal",
                "Incluir exercícios práticos de autorreflexão",
                "Destacar cases de transformação pessoal"
            ],
            'lideranca': [
                "Criar conteúdo sobre gestão de conflitos",
                "Incluir templates de feedback estruturado",
                "Destacar cases de transformação de equipes"
            ],
            'comunicacao': [
                "Criar série sobre técnicas de apresentação",
                "Incluir exercícios práticos de oratória",
                "Destacar exemplos de comunicação eficaz"
            ],
            'vendas': [
                "Criar série sobre técnicas de fechamento",
                "Incluir scripts de abordagem comercial",
                "Destacar cases de aumento de conversão"
            ]
        }
        
        return base_recommendations + theme_recommendations.get(theme, [])

def generate_complete_seo_package(transcription_file: str) -> Dict[str, any]:
    """
    Função principal para gerar pacote completo de SEO
    
    Args:
        transcription_file (str): Caminho para arquivo de transcrição
    
    Returns:
        Dict com conteúdo SEO otimizado
    """
    generator = AdvancedSEOGenerator()
    return generator.generate_optimized_content(transcription_file)

if __name__ == "__main__":
    # Teste com a transcrição de autorresponsabilidade
    transcription_path = "Transcricoes de Videos/Video 1/f5-youtube-video1-Autorresponsabilidade_01mp4.txt"
    
    if os.path.exists(transcription_path):
        print("🚀 Gerando pacote SEO avançado...")
        result = generate_complete_seo_package(transcription_path)
        
        if 'error' not in result:
            print("\n✅ PACOTE SEO GERADO COM SUCESSO!")
            print(f"\n🎯 TEMA DETECTADO: {result['video_info']['detected_theme']}")
            print(f"📝 TÍTULO: {result['seo_content']['title']['primary']}")
            print(f"🏷️ TAGS: {result['seo_content']['tags']['formatted']}")
            print(f"📊 CARACTERES DESCRIÇÃO: {result['seo_content']['description']['character_count']}")
            
            # Salva resultado
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"reports/advanced_seo_{timestamp}.json"
            os.makedirs('reports', exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 Relatório salvo em: {output_file}")
            
        else:
            print(f"❌ Erro: {result['error']}")
    else:
        print(f"❌ Arquivo não encontrado: {transcription_path}") 