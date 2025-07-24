"""
Content Optimizer - Sistema de Otimização de Conteúdo com IA
Desenvolvido para F5 Estratégia - Baseado na Metodologia CHAVI
Usando Gemini (Google AI) como IA principal
"""

import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

# Importações para IA - Gemini como principal
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Fallback para Claude/Anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

# Fallback para OpenAI
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from config import F5Config, AIConfig, YouTubeConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContentAnalysis:
    """Estrutura para análise de conteúdo"""
    video_id: str
    title: str
    description: str
    tags: List[str]
    persona_target: str
    chavi_score: Dict[str, float]
    seo_score: float
    optimization_suggestions: List[str]
    keyword_density: Dict[str, float]
    sentiment_analysis: str
    estimated_performance: str

class CHAVIAnalyzer:
    """Analisador baseado na metodologia CHAVI da F5"""
    
    def __init__(self):
        self.config = F5Config()
        self.pillars = self.config.CHAVI_PILLARS
        
        # Critérios de avaliação por pilar
        self.evaluation_criteria = {
            'C': {  # Campanha
                'keywords': ['estratégia', 'planejamento', 'pesquisa', 'público', 'mapa mental'],
                'weight': 0.2,
                'description': 'Planejamento estratégico e definição de público'
            },
            'H': {  # Humanização
                'keywords': ['vídeo', 'roteiro', 'oratória', 'humanizar', 'conexão', 'história'],
                'weight': 0.25,
                'description': 'Qualidade do vídeo e conexão humana'
            },
            'A': {  # Anúncios
                'keywords': ['performance', 'conversão', 'otimização', 'segmentação', 'meta', 'google'],
                'weight': 0.2,
                'description': 'Foco em performance e conversão'
            },
            'V': {  # Vendas
                'keywords': ['vendas', 'leads', 'conversão', 'crm', 'oportunidade', 'resultado'],
                'weight': 0.2,
                'description': 'Geração de leads e vendas'
            },
            'I': {  # Inteligência
                'keywords': ['dados', 'métricas', 'análise', 'insights', 'relatórios', 'bi'],
                'weight': 0.15,
                'description': 'Inteligência de dados e análise'
            }
        }
    
    def analyze_content_chavi(self, title: str, description: str, tags: List[str]) -> Dict[str, float]:
        """
        Analisa conteúdo baseado nos pilares CHAVI
        
        Args:
            title (str): Título do vídeo
            description (str): Descrição do vídeo
            tags (List[str]): Tags do vídeo
        
        Returns:
            Dict com pontuação por pilar CHAVI
        """
        content_text = f"{title} {description} {' '.join(tags)}".lower()
        scores = {}
        
        for pilar, criteria in self.evaluation_criteria.items():
            score = 0
            keyword_matches = 0
            
            for keyword in criteria['keywords']:
                if keyword in content_text:
                    keyword_matches += 1
                    # Pontuação extra se estiver no título
                    if keyword in title.lower():
                        score += 2
                    else:
                        score += 1
            
            # Normalizar score (0-10)
            max_possible = len(criteria['keywords']) * 2
            normalized_score = min(10, (score / max_possible) * 10) if max_possible > 0 else 0
            
            scores[pilar] = {
                'score': round(normalized_score, 2),
                'keywords_found': keyword_matches,
                'description': criteria['description'],
                'weight': criteria['weight']
            }
        
        return scores

class PersonaTargeting:
    """Sistema de direcionamento por persona"""
    
    def __init__(self):
        self.personas = F5Config.PERSONAS
    
    def identify_target_persona(self, title: str, description: str, tags: List[str]) -> Tuple[str, float]:
        """
        Identifica a persona alvo baseada no conteúdo
        
        Args:
            title (str): Título do vídeo
            description (str): Descrição do vídeo
            tags (List[str]): Tags do vídeo
        
        Returns:
            Tuple com (persona_identificada, confiança)
        """
        content_text = f"{title} {description} {' '.join(tags)}".lower()
        
        persona_scores = {}
        
        # Palavras-chave indicativas por persona
        persona_indicators = {
            'estrategico': [
                'roi', 'kpi', 'métricas', 'escalabilidade', 'enterprise', 'corporativo',
                'dashboard', 'business intelligence', 'previsibilidade', 'sustentável'
            ],
            'crescimento': [
                'pme', 'pequena empresa', 'crescer', 'escalar', 'estruturar',
                'funil', 'processo', 'organizacional', 'otimizar'
            ],
            'smart': [
                'rápido', 'simples', 'prático', 'urgente', 'sobrevivência',
                'início', 'começar', 'básico', 'essencial'
            ]
        }
        
        for persona, indicators in persona_indicators.items():
            score = 0
            for indicator in indicators:
                if indicator in content_text:
                    score += 1
                    # Peso extra se estiver no título
                    if indicator in title.lower():
                        score += 0.5
            
            # Normalizar por número de indicadores
            normalized_score = score / len(indicators) if indicators else 0
            persona_scores[persona] = normalized_score
        
        # Identificar persona com maior score
        best_persona = max(persona_scores, key=persona_scores.get)
        confidence = persona_scores[best_persona]
        
        return best_persona, confidence

class SEOAnalyzer:
    """Analisador de SEO específico para YouTube"""
    
    def __init__(self):
        self.core_keywords = F5Config.CORE_KEYWORDS
    
    def analyze_seo_score(self, title: str, description: str, tags: List[str]) -> Dict[str, Any]:
        """
        Analisa aspectos de SEO do conteúdo
        
        Args:
            title (str): Título do vídeo
            description (str): Descrição do vídeo
            tags (List[str]): Tags do vídeo
        
        Returns:
            Dict com análise de SEO
        """
        analysis = {
            'title_analysis': self._analyze_title(title),
            'description_analysis': self._analyze_description(description),
            'tags_analysis': self._analyze_tags(tags),
            'keyword_density': self._calculate_keyword_density(title, description, tags),
            'overall_score': 0
        }
        
        # Calcular score geral
        title_score = analysis['title_analysis']['score']
        desc_score = analysis['description_analysis']['score']
        tags_score = analysis['tags_analysis']['score']
        
        analysis['overall_score'] = round((title_score * 0.4 + desc_score * 0.4 + tags_score * 0.2), 2)
        
        return analysis
    
    def _analyze_title(self, title: str) -> Dict[str, Any]:
        """Analisa qualidade SEO do título"""
        score = 0
        issues = []
        suggestions = []
        
        # Verificar comprimento
        if 60 <= len(title) <= 70:
            score += 2
        elif 50 <= len(title) < 60 or 70 < len(title) <= 80:
            score += 1
            suggestions.append("Considere ajustar título para 60-70 caracteres para melhor exibição")
        else:
            issues.append("Título muito curto ou muito longo")
            suggestions.append("Mantenha o título entre 60-70 caracteres")
        
        # Verificar palavras-chave principais
        title_lower = title.lower()
        keyword_found = False
        for keyword in self.core_keywords:
            if keyword in title_lower:
                score += 2
                keyword_found = True
                break
        
        if not keyword_found:
            issues.append("Nenhuma palavra-chave principal encontrada no título")
            suggestions.append(f"Inclua uma das palavras-chave: {', '.join(self.core_keywords[:3])}")
        
        # Verificar elementos emocionais/clique
        emotional_words = ['como', 'segredo', 'dicas', 'estratégia', 'resultado', 'aumento', 'melhores']
        if any(word in title_lower for word in emotional_words):
            score += 1
        else:
            suggestions.append("Considere adicionar palavras que geram interesse como 'como', 'dicas', 'estratégia'")
        
        return {
            'score': min(10, score),
            'issues': issues,
            'suggestions': suggestions,
            'length': len(title)
        }
    
    def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analisa qualidade SEO da descrição"""
        score = 0
        issues = []
        suggestions = []
        
        # Verificar comprimento
        if len(description) >= 125:
            score += 2
        else:
            issues.append("Descrição muito curta")
            suggestions.append("Descrição deve ter pelo menos 125 caracteres")
        
        # Verificar palavras-chave
        desc_lower = description.lower()
        keywords_found = sum(1 for keyword in self.core_keywords if keyword in desc_lower)
        
        if keywords_found >= 3:
            score += 3
        elif keywords_found >= 1:
            score += 1
        else:
            issues.append("Poucas palavras-chave na descrição")
            suggestions.append("Inclua mais palavras-chave relevantes na descrição")
        
        # Verificar call-to-action
        cta_words = ['inscreva', 'curtir', 'comentar', 'compartilhar', 'link', 'acesse']
        if any(word in desc_lower for word in cta_words):
            score += 1
        else:
            suggestions.append("Adicione call-to-action (inscreva-se, curtir, comentar)")
        
        # Verificar timestamps
        if re.search(r'\d{1,2}:\d{2}', description):
            score += 1
        else:
            suggestions.append("Considere adicionar timestamps para vídeos longos")
        
        return {
            'score': min(10, score),
            'issues': issues,
            'suggestions': suggestions,
            'length': len(description),
            'keywords_found': keywords_found
        }
    
    def _analyze_tags(self, tags: List[str]) -> Dict[str, Any]:
        """Analisa qualidade das tags"""
        score = 0
        issues = []
        suggestions = []
        
        # Verificar quantidade
        if 10 <= len(tags) <= 15:
            score += 2
        elif 5 <= len(tags) < 10:
            score += 1
            suggestions.append("Considere adicionar mais tags (10-15 é ideal)")
        else:
            if len(tags) < 5:
                issues.append("Muito poucas tags")
            else:
                issues.append("Muitas tags podem diluir relevância")
        
        # Verificar palavras-chave nas tags
        tags_text = ' '.join(tags).lower()
        core_keywords_in_tags = sum(1 for keyword in self.core_keywords if keyword in tags_text)
        
        if core_keywords_in_tags >= 3:
            score += 3
        elif core_keywords_in_tags >= 1:
            score += 1
        else:
            issues.append("Poucas palavras-chave principais nas tags")
        
        # Verificar variações de palavras-chave
        variations_found = False
        for tag in tags:
            if any(keyword in tag.lower() for keyword in self.core_keywords):
                variations_found = True
                break
        
        if variations_found:
            score += 1
        
        return {
            'score': min(10, score),
            'issues': issues,
            'suggestions': suggestions,
            'total_tags': len(tags),
            'core_keywords_found': core_keywords_in_tags
        }
    
    def _calculate_keyword_density(self, title: str, description: str, tags: List[str]) -> Dict[str, float]:
        """Calcula densidade de palavras-chave"""
        all_text = f"{title} {description} {' '.join(tags)}".lower()
        word_count = len(all_text.split())
        
        density = {}
        for keyword in self.core_keywords:
            count = all_text.count(keyword.lower())
            density[keyword] = round((count / word_count) * 100, 2) if word_count > 0 else 0
        
        return density

class GeminiContentOptimizer:
    """Otimizador de conteúdo usando Gemini (Google AI)"""
    
    def __init__(self):
        self.ai_config = AIConfig()
        
        # Inicializar Gemini se disponível
        if GEMINI_AVAILABLE and self.ai_config.GEMINI_API_KEY:
            genai.configure(api_key=self.ai_config.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel(self.ai_config.GEMINI_MODEL)
            self.use_gemini = True
            logger.info("Gemini (Google AI) inicializado como IA principal")
        
        # Fallback para Claude se Gemini não estiver disponível
        elif ANTHROPIC_AVAILABLE and self.ai_config.ANTHROPIC_API_KEY:
            self.claude_client = anthropic.Anthropic(
                api_key=self.ai_config.ANTHROPIC_API_KEY
            )
            self.use_gemini = False
            self.use_claude = True
            logger.info("Claude (Anthropic) configurado como fallback")
        
        # Fallback para OpenAI se nem Gemini nem Claude estiverem disponíveis
        elif OPENAI_AVAILABLE and self.ai_config.OPENAI_API_KEY:
            openai.api_key = self.ai_config.OPENAI_API_KEY
            self.use_gemini = False
            self.use_claude = False
            logger.info("OpenAI configurado como fallback")
        
        else:
            logger.error("Nenhuma API de IA configurada")
            raise ValueError("Configure pelo menos uma API de IA (Gemini, Claude ou OpenAI)")
    
    def generate_optimization_suggestions(self, content_analysis: ContentAnalysis) -> List[str]:
        """
        Gera sugestões de otimização usando IA
        
        Args:
            content_analysis: Análise completa do conteúdo
        
        Returns:
            Lista de sugestões específicas
        """
        try:
            persona_info = F5Config.PERSONAS[content_analysis.persona_target]
            
            prompt = f"""
            Como especialista em YouTube SEO e metodologia CHAVI da F5 Estratégia, analise este conteúdo:
            
            TÍTULO: {content_analysis.title}
            DESCRIÇÃO: {content_analysis.description[:500]}...
            PERSONA ALVO: {persona_info['name']} ({persona_info['revenue']})
            FOCO DA PERSONA: {', '.join(persona_info['focus'])}
            
            SCORES CHAVI:
            {json.dumps(content_analysis.chavi_score, indent=2)}
            
            SCORE SEO: {content_analysis.seo_score}/10
            
            CONTEXTO F5 ESTRATÉGIA:
            - Agência de marketing digital especializada
            - Metodologia CHAVI (Campanha, Humanização, Anúncios, Vendas, Inteligência)
            - Arquétipos de marca: Sábio + Herói (confiável, analítico, determinado)
            - Foco em resultados mensuráveis e dados
            
            Forneça 5-7 sugestões ESPECÍFICAS e ACIONÁVEIS para otimizar este conteúdo, considerando:
            1. Metodologia CHAVI (melhorar pilares com menor pontuação)
            2. SEO para YouTube
            3. Adequação à persona alvo
            4. Tom de voz da F5 (Sábio + Herói: confiável, analítico, determinado)
            
            Formato: Lista numerada com sugestões diretas e específicas.
            """
            
            if self.use_gemini:
                # Usar Gemini
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.ai_config.MAX_TOKENS,
                        temperature=self.ai_config.TEMPERATURE,
                    )
                )
                suggestions_text = response.text
            elif hasattr(self, 'use_claude') and self.use_claude:
                # Fallback para Claude
                response = self.claude_client.messages.create(
                    model=self.ai_config.CLAUDE_MODEL,
                    max_tokens=self.ai_config.MAX_TOKENS,
                    temperature=self.ai_config.TEMPERATURE,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )
                suggestions_text = response.content[0].text
            else:
                # Fallback para OpenAI
                response = openai.chat.completions.create(
                    model=self.ai_config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "Você é um especialista em YouTube SEO e Growth Marketing da F5 Estratégia."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.ai_config.MAX_TOKENS,
                    temperature=self.ai_config.TEMPERATURE
                )
                suggestions_text = response.choices[0].message.content
            
            # Extrair sugestões numeradas
            suggestions = []
            for line in suggestions_text.split('\n'):
                if re.match(r'^\d+\.', line.strip()):
                    suggestions.append(line.strip())
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Erro ao gerar sugestões com IA: {e}")
            return [
                "Erro ao gerar sugestões automáticas",
                "Verifique sua configuração de API de IA",
                "Consulte os logs para mais detalhes"
            ]
    
    def generate_optimized_title(self, current_title: str, persona: str, keywords: List[str]) -> str:
        """Gera sugestão de título otimizado"""
        try:
            persona_info = F5Config.PERSONAS[persona]
            
            prompt = f"""
            Crie um título otimizado para YouTube baseado nestas informações:
            
            TÍTULO ATUAL: {current_title}
            PERSONA ALVO: {persona_info['name']} - {persona_info['revenue']}
            FOCO: {', '.join(persona_info['focus'])}
            PALAVRAS-CHAVE: {', '.join(keywords[:3])}
            
            CONTEXTO F5 ESTRATÉGIA:
            - Agência de marketing digital
            - Tom de voz: Confiável, analítico, determinado (Sábio + Herói)
            - Metodologia CHAVI
            
            CRITÉRIOS:
            - 60-70 caracteres
            - Incluir palavra-chave principal
            - Gerar curiosidade/urgência
            - Adequado à persona
            - Tom profissional mas acessível
            
            Retorne apenas o título otimizado, sem explicações.
            """
            
            if self.use_gemini:
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=100,
                        temperature=0.8,
                    )
                )
                return response.text.strip().replace('"', '')
            elif hasattr(self, 'use_claude') and self.use_claude:
                response = self.claude_client.messages.create(
                    model=self.ai_config.CLAUDE_MODEL,
                    max_tokens=100,
                    temperature=0.8,
                    messages=[{
                        "role": "user", 
                        "content": prompt
                    }]
                )
                return response.content[0].text.strip().replace('"', '')
            else:
                response = openai.chat.completions.create(
                    model=self.ai_config.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "Você é um especialista em títulos para YouTube da F5 Estratégia."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.8
                )
                return response.choices[0].message.content.strip().replace('"', '')
            
        except Exception as e:
            logger.error(f"Erro ao gerar título otimizado: {e}")
            return current_title

class ContentOptimizer:
    """Classe principal do otimizador de conteúdo"""
    
    def __init__(self):
        self.chavi_analyzer = CHAVIAnalyzer()
        self.persona_targeting = PersonaTargeting()
        self.seo_analyzer = SEOAnalyzer()
        self.ai_optimizer = GeminiContentOptimizer()
    
    def analyze_content(self, video_data: Dict[str, Any]) -> ContentAnalysis:
        """
        Análise completa de conteúdo
        
        Args:
            video_data: Dados do vídeo (título, descrição, tags, etc.)
        
        Returns:
            ContentAnalysis com análise completa
        """
        title = video_data.get('title', '')
        description = video_data.get('description', '')
        tags = video_data.get('tags', [])
        video_id = video_data.get('video_id', '')
        
        # Análise CHAVI
        chavi_scores = self.chavi_analyzer.analyze_content_chavi(title, description, tags)
        
        # Identificação de persona
        target_persona, persona_confidence = self.persona_targeting.identify_target_persona(title, description, tags)
        
        # Análise SEO
        seo_analysis = self.seo_analyzer.analyze_seo_score(title, description, tags)
        
        # Criar objeto de análise
        content_analysis = ContentAnalysis(
            video_id=video_id,
            title=title,
            description=description,
            tags=tags,
            persona_target=target_persona,
            chavi_score=chavi_scores,
            seo_score=seo_analysis['overall_score'],
            optimization_suggestions=[],
            keyword_density=seo_analysis['keyword_density'],
            sentiment_analysis="Neutro",  # Placeholder - pode ser expandido
            estimated_performance="Médio"  # Placeholder - pode ser expandido
        )
        
        # Gerar sugestões com IA
        ai_suggestions = self.ai_optimizer.generate_optimization_suggestions(content_analysis)
        content_analysis.optimization_suggestions = ai_suggestions
        
        return content_analysis
    
    def optimize_existing_content(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Otimiza conteúdo existente
        
        Args:
            video_data: Dados do vídeo
        
        Returns:
            Dict com versão otimizada
        """
        analysis = self.analyze_content(video_data)
        
        # Gerar título otimizado
        optimized_title = self.ai_optimizer.generate_optimized_title(
            analysis.title,
            analysis.persona_target,
            F5Config.CORE_KEYWORDS
        )
        
        return {
            'original': {
                'title': analysis.title,
                'description': analysis.description,
                'tags': analysis.tags
            },
            'optimized': {
                'title': optimized_title,
                'description': analysis.description,  # Pode ser expandido
                'tags': analysis.tags  # Pode ser expandido
            },
            'analysis': analysis,
            'persona_target': analysis.persona_target,
            'improvement_potential': 10 - analysis.seo_score,
            'ai_used': 'Gemini (Google AI)' if self.ai_optimizer.use_gemini else ('Claude (Anthropic)' if hasattr(self.ai_optimizer, 'use_claude') and self.ai_optimizer.use_claude else 'OpenAI')
        }

def create_content_optimizer():
    """Factory function para criar otimizador"""
    return ContentOptimizer()

if __name__ == "__main__":
    # Teste básico
    optimizer = create_content_optimizer()
    
    test_video = {
        'video_id': 'test123',
        'title': 'Como Aumentar Vendas com Marketing Digital',
        'description': 'Neste vídeo você vai aprender estratégias de marketing digital para aumentar suas vendas...',
        'tags': ['marketing digital', 'vendas', 'estratégia']
    }
    
    analysis = optimizer.analyze_content(test_video)
    print(f"Análise concluída para: {analysis.title}")
    print(f"Persona alvo: {analysis.persona_target}")
    print(f"Score SEO: {analysis.seo_score}/10") 