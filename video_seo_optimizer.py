"""
Sistema de Otimização SEO para Vídeos YouTube - F5 Estratégia
Análise inteligente de transcrições e geração automatizada de conteúdo SEO
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter
from pathlib import Path

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TranscriptionAnalyzer:
    """Analisador de transcrições para extração de insights e palavras-chave"""
    
    def __init__(self):
        self.stopwords = self._get_stopwords()
        self.f5_keywords = self._get_f5_keywords()
        
    def _get_stopwords(self) -> set:
        """Lista de palavras irrelevantes para SEO"""
        return {
            'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'com', 'como', 'para', 
            'por', 'no', 'na', 'se', 'eu', 'ele', 'ela', 'nós', 'vocês', 'eles', 'elas',
            'que', 'qual', 'quando', 'onde', 'porque', 'então', 'mas', 'ou', 'nem', 'já',
            'ainda', 'só', 'também', 'muito', 'mais', 'menos', 'bem', 'mal', 'todo', 'toda',
            'tudo', 'nada', 'algo', 'alguém', 'ninguém', 'sim', 'não', 'talvez', 'quem',
            'isso', 'aquilo', 'este', 'esta', 'esse', 'essa', 'aquele', 'aquela', 'meu',
            'minha', 'seu', 'sua', 'nosso', 'nossa', 'deles', 'delas', 'ter', 'ser', 'estar',
            'fazer', 'vai', 'vou', 'foi', 'era', 'está', 'estou', 'tem', 'tinha', 'faz',
            'fazia', 'pode', 'podia', 'quer', 'queria', 'sabe', 'sabia', 'vem', 'vinha',
            'ali', 'aqui', 'lá', 'aí', 'cá', 'assim', 'agora', 'hoje', 'ontem', 'amanhã',
            'antes', 'depois', 'sempre', 'nunca', 'às', 'vezes', 'pelo', 'pela', 'pelos',
            'pelas', 'contra', 'sobre', 'sob', 'entre', 'até', 'desde', 'durante', 'através'
        }
    
    def _get_f5_keywords(self) -> Dict[str, List[str]]:
        """Palavras-chave relacionadas à F5 Estratégia e temas de interesse"""
        return {
            'negocio': [
                'empreendedorismo', 'empresário', 'negócio', 'empresa', 'gestão', 'liderança',
                'estratégia', 'planejamento', 'crescimento', 'escalabilidade', 'inovação',
                'produtividade', 'performance', 'resultados', 'metas', 'objetivos'
            ],
            'marketing': [
                'marketing', 'digital', 'vendas', 'tráfego', 'leads', 'conversão', 'funil',
                'campanhas', 'anúncios', 'publicidade', 'branding', 'marca', 'posicionamento',
                'segmentação', 'audiência', 'cliente', 'público', 'mercado'
            ],
            'desenvolvimento': [
                'autoconhecimento', 'autorresponsabilidade', 'desenvolvimento', 'pessoal',
                'profissional', 'competências', 'habilidades', 'mindset', 'mentalidade',
                'consciência', 'reflexão', 'aprendizado', 'evolução', 'transformação'
            ],
            'comunicacao': [
                'comunicação', 'oratória', 'apresentação', 'discurso', 'storytelling',
                'persuasão', 'influência', 'networking', 'relacionamento', 'conexão',
                'diálogo', 'escuta', 'feedback', 'clareza', 'objetividade'
            ],
            'gestao': [
                'equipe', 'time', 'colaborador', 'funcionário', 'talento', 'recrutamento',
                'seleção', 'treinamento', 'capacitação', 'motivação', 'engajamento',
                'cultura', 'organizacional', 'processo', 'sistemática', 'metodologia'
            ]
        }
    
    def clean_text(self, text: str) -> str:
        """Limpa e normaliza o texto da transcrição"""
        # Remove timestamps
        text = re.sub(r'\d{2}:\d{2}:\d{2}:\d{2}\s*-\s*\d{2}:\d{2}:\d{2}:\d{2}', '', text)
        
        # Remove "Desconhecido" (speaker labels)
        text = re.sub(r'Desconhecido\s*', '', text)
        
        # Remove caracteres especiais e normaliza espaços
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip().lower()
    
    def extract_keywords(self, text: str, min_length: int = 4, top_n: int = 30) -> List[Tuple[str, int]]:
        """Extrai palavras-chave relevantes do texto"""
        clean_text = self.clean_text(text)
        words = clean_text.split()
        
        # Filtra palavras por critérios
        filtered_words = [
            word for word in words
            if len(word) >= min_length
            and word not in self.stopwords
            and not word.isdigit()
        ]
        
        # Conta frequência das palavras
        word_freq = Counter(filtered_words)
        
        # Prioriza palavras relacionadas à F5
        scored_words = []
        for word, freq in word_freq.items():
            score = freq
            
            # Aumenta score para palavras da F5
            for category, keywords in self.f5_keywords.items():
                if any(keyword in word or word in keyword for keyword in keywords):
                    score *= 2
                    break
            
            scored_words.append((word, score))
        
        # Ordena por score e retorna top N
        scored_words.sort(key=lambda x: x[1], reverse=True)
        return scored_words[:top_n]
    
    def extract_key_phrases(self, text: str, max_phrases: int = 15) -> List[str]:
        """Extrai frases-chave importantes do texto"""
        sentences = re.split(r'[.!?]+', text)
        phrases = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 20 or len(sentence) > 150:
                continue
                
            # Remove timestamps e limpeza básica
            sentence = re.sub(r'\d{2}:\d{2}:\d{2}:\d{2}', '', sentence)
            sentence = re.sub(r'Desconhecido', '', sentence)
            sentence = sentence.strip()
            
            if not sentence:
                continue
                
            # Verifica se contém palavras-chave da F5
            words = sentence.lower().split()
            f5_match = False
            for category, keywords in self.f5_keywords.items():
                if any(keyword in ' '.join(words) for keyword in keywords):
                    f5_match = True
                    break
            
            if f5_match or any(word in ['problema', 'solução', 'resultado', 'estratégia', 'desenvolvimento'] for word in words):
                phrases.append(sentence)
        
        return phrases[:max_phrases]
    
    def get_main_theme(self, text: str) -> Dict[str, any]:
        """Identifica o tema principal da transcrição"""
        keywords = self.extract_keywords(text, top_n=50)
        keyword_dict = dict(keywords)
        
        # Analisa distribuição por categoria
        category_scores = {}
        for category, category_keywords in self.f5_keywords.items():
            score = 0
            for keyword in category_keywords:
                # Verifica se a palavra-chave aparece no texto
                if keyword in text.lower():
                    # Bonus se estiver nas top keywords extraídas
                    if keyword in keyword_dict:
                        score += keyword_dict[keyword] * 2
                    else:
                        score += 1
            category_scores[category] = score
        
        # Tema principal
        main_category = max(category_scores, key=category_scores.get)
        
        return {
            'main_theme': main_category,
            'category_scores': category_scores,
            'confidence': category_scores[main_category] / sum(category_scores.values()) if sum(category_scores.values()) > 0 else 0
        }

class SEOContentGenerator:
    """Gerador de conteúdo SEO otimizado para YouTube"""
    
    def __init__(self):
        self.analyzer = TranscriptionAnalyzer()
        self.f5_landing_pages = self._get_f5_landing_pages()
        
    def _get_f5_landing_pages(self) -> Dict[str, str]:
        """URLs das landing pages da F5 por categoria"""
        return {
            'negocio': 'https://f5estrategia.com/gestao-empresarial',
            'marketing': 'https://f5estrategia.com/marketing-digital', 
            'desenvolvimento': 'https://f5estrategia.com/desenvolvimento-pessoal',
            'comunicacao': 'https://f5estrategia.com/comunicacao-estrategica',
            'gestao': 'https://f5estrategia.com/gestao-equipes',
            'consultoria': 'https://f5estrategia.com/consultoria',
            'treinamento': 'https://f5estrategia.com/treinamentos',
            'contato': 'https://f5estrategia.com/contato'
        }
    
    def generate_title(self, transcription: str, max_chars: int = 100) -> Dict[str, str]:
        """Gera títulos otimizados para SEO do YouTube"""
        theme_analysis = self.analyzer.get_main_theme(transcription)
        keywords = self.analyzer.extract_keywords(transcription, top_n=10)
        
        # Palavras-chave principais
        top_keywords = [kw[0] for kw in keywords[:5]]
        
        # Templates de título baseados no tema
        title_templates = {
            'desenvolvimento': [
                "Como Desenvolver {keyword} e Transformar sua {area} | F5 Estratégia",
                "{keyword}: A Chave para o Sucesso {area} | Dicas Práticas F5",
                "Desenvolva {keyword} em {tempo} e Mude sua {area} Para Sempre",
                "{keyword} na Prática: Estratégias que Funcionam | F5 Estratégia"
            ],
            'negocio': [
                "Como {keyword} Pode Revolucionar seu Negócio | F5 Estratégia", 
                "{keyword} para Empresários: Estratégias Comprovadas | F5",
                "Aumente seus Resultados com {keyword} | Método F5 Estratégia",
                "{keyword}: O Segredo dos Empresários de Sucesso | F5"
            ],
            'marketing': [
                "{keyword} no Marketing Digital: Estratégias que Vendem | F5",
                "Como Usar {keyword} para Gerar Mais Leads | F5 Estratégia",
                "{keyword}: A Estratégia Secreta para Vender Mais | F5",
                "Aumente suas Vendas com {keyword} | Método F5 Comprovado"
            ],
            'comunicacao': [
                "Comunicação {keyword}: Como Influenciar e Persuadir | F5",
                "{keyword} na Comunicação Empresarial | F5 Estratégia",
                "Domine a Arte da {keyword} e Mude seus Resultados | F5",
                "{keyword}: Comunicação que Gera Resultados | F5 Estratégia"
            ],
            'gestao': [
                "Gestão {keyword}: Como Liderar Equipes de Alta Performance | F5",
                "{keyword} para Gestores: Estratégias Eficazes | F5 Estratégia",
                "Como Aplicar {keyword} na sua Gestão | Método F5",
                "{keyword}: O Diferencial dos Líderes de Sucesso | F5"
            ]
        }
        
        # Escolhe template baseado no tema principal
        main_theme = theme_analysis['main_theme']
        templates = title_templates.get(main_theme, title_templates['desenvolvimento'])
        
        # Gera títulos
        titles = []
        for template in templates:
            for keyword in top_keywords[:3]:
                title = template.format(
                    keyword=keyword.title(),
                    area='Carreira Profissional',
                    tempo='30 Dias'
                )
                
                if len(title) <= max_chars:
                    titles.append(title)
        
        # Títulos específicos para autorresponsabilidade
        if 'autorresponsabilidade' in ' '.join(top_keywords):
            specific_titles = [
                "Autorresponsabilidade: O Segredo do Sucesso Profissional | F5",
                "Como Desenvolver Autorresponsabilidade e Mudar sua Vida | F5",
                "Autorresponsabilidade na Prática: Estratégias Comprovadas | F5",
                "O Poder da Autorresponsabilidade no Mundo dos Negócios | F5"
            ]
            titles.extend([t for t in specific_titles if len(t) <= max_chars])
        
        return {
            'primary': titles[0] if titles else "Desenvolvimento Profissional | F5 Estratégia",
            'alternatives': titles[1:6],
            'keywords_used': top_keywords,
            'theme': main_theme
        }
    
    def generate_description(self, transcription: str, title: str, max_chars: int = 5000) -> str:
        """Gera descrição otimizada para SEO"""
        theme_analysis = self.analyzer.get_main_theme(transcription)
        keywords = self.analyzer.extract_keywords(transcription, top_n=15)
        key_phrases = self.analyzer.extract_key_phrases(transcription, max_phrases=3)
        
        main_theme = theme_analysis['main_theme']
        landing_page = self.f5_landing_pages.get(main_theme, self.f5_landing_pages['consultoria'])
        
        # Extrai pontos principais da transcrição
        key_points = [phrase for phrase in key_phrases if len(phrase) > 30][:3]
        
        # Template de descrição
        description = f"""🎯 {title}

Neste vídeo, exploramos conceitos fundamentais sobre {keywords[0][0]} e como aplicar na prática para transformar seus resultados.

📋 PRINCIPAIS PONTOS ABORDADOS:
"""
        
        # Adiciona pontos principais
        for i, point in enumerate(key_points, 1):
            description += f"\n{i}. {point.strip()}"
        
        # Seção de palavras-chave
        top_keywords = [kw[0] for kw in keywords[:8]]
        description += f"""

🔍 PALAVRAS-CHAVE:
{' | '.join(top_keywords[:6])}

🚀 TRANSFORME SEUS RESULTADOS:
Quer implementar essas estratégias no seu negócio? A F5 Estratégia oferece consultoria especializada para empresários que buscam crescimento sustentável e resultados extraordinários.

👉 Conheça nossos serviços: {landing_page}
📞 Agende uma consultoria gratuita: {self.f5_landing_pages['contato']}

💡 SOBRE A F5 ESTRATÉGIA:
Somos especialistas em transformar negócios através de estratégias comprovadas. Nossa metodologia CHAVI (Campanha, Humanização, Anúncios, Vendas, Inteligência) já ajudou centenas de empresários a alcançar seus objetivos.

🔔 INSCREVA-SE no canal para mais conteúdos sobre:
• Desenvolvimento empresarial
• Marketing digital estratégico  
• Liderança e gestão
• Crescimento de negócios
• Metodologias comprovadas

📱 NOS SIGA NAS REDES SOCIAIS:
Instagram: @f5estrategia
LinkedIn: F5 Estratégia
Site: https://f5estrategia.com

#F5Estrategia #{keywords[0][0].title()} #DesenvolvimentoProfissional #Empreendedorismo #Gestao #MarketingDigital #Lideranca #Negocios #Estrategia #Resultados #Sucesso

---
© F5 Estratégia - Todos os direitos reservados."""
        
        # Ajusta tamanho se necessário
        if len(description) > max_chars:
            # Remove hashtags extras se exceder limite
            description = description.split('#F5Estrategia')[0] + '#F5Estrategia #' + keywords[0][0].title()
        
        return description
    
    def generate_tags(self, transcription: str, max_tags: int = 15) -> List[str]:
        """Gera tags otimizadas para SEO (separadas por traços)"""
        theme_analysis = self.analyzer.get_main_theme(transcription)
        keywords = self.analyzer.extract_keywords(transcription, top_n=20)
        
        # Tags base da F5
        base_tags = [
            'f5-estrategia',
            'marketing-digital', 
            'empreendedorismo',
            'desenvolvimento-profissional',
            'gestao-empresarial',
            'lideranca',
            'estrategia-empresarial'
        ]
        
        # Tags específicas do conteúdo
        content_tags = []
        for keyword, freq in keywords:
            if len(keyword) >= 4:
                # Converte para formato de tag (com traços)
                tag = keyword.replace(' ', '-').lower()
                if tag not in base_tags:
                    content_tags.append(tag)
        
        # Tags por tema
        theme_tags = {
            'desenvolvimento': ['autoconhecimento', 'crescimento-pessoal', 'soft-skills', 'mindset'],
            'negocio': ['crescimento-empresarial', 'inovacao-negocios', 'escalabilidade', 'resultados'],
            'marketing': ['trafego-pago', 'leads', 'conversao', 'vendas-digitais'],
            'comunicacao': ['oratoria', 'apresentacao', 'persuasao', 'networking'],
            'gestao': ['gestao-equipes', 'alta-performance', 'cultura-organizacional', 'processos']
        }
        
        main_theme = theme_analysis['main_theme']
        specific_tags = theme_tags.get(main_theme, [])
        
        # Combina todas as tags
        all_tags = base_tags + content_tags[:5] + specific_tags
        
        # Remove duplicatas e limita quantidade
        unique_tags = []
        seen = set()
        for tag in all_tags:
            if tag not in seen and len(tag) >= 3:
                unique_tags.append(tag)
                seen.add(tag)
                if len(unique_tags) >= max_tags:
                    break
        
        return unique_tags
    
    def generate_metadata(self, transcription: str) -> Dict[str, str]:
        """Gera metadados completos para o arquivo de vídeo"""
        theme_analysis = self.analyzer.get_main_theme(transcription)
        keywords = self.analyzer.extract_keywords(transcription, top_n=10)
        
        # Metadados para arquivo
        metadata = {
            'title': self.generate_title(transcription)['primary'],
            'description': keywords[0][0].title() + ' - Conteúdo F5 Estratégia',
            'keywords': '-'.join([kw[0] for kw in keywords[:8]]),
            'category': theme_analysis['main_theme'],
            'author': 'F5 Estratégia',
            'creation_date': datetime.now().strftime('%Y-%m-%d'),
            'theme_confidence': f"{theme_analysis['confidence']:.2f}",
            'optimization_version': '1.0'
        }
        
        return metadata

class VideoSEOOptimizer:
    """Sistema principal de otimização SEO para vídeos"""
    
    def __init__(self):
        self.generator = SEOContentGenerator()
        self.analyzer = TranscriptionAnalyzer()
        
    def optimize_video_from_transcription(self, transcription_file: str) -> Dict[str, any]:
        """Otimiza vídeo completo a partir de arquivo de transcrição"""
        try:
            # Lê arquivo de transcrição
            with open(transcription_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
            
            # Gera conteúdo SEO
            title_data = self.generator.generate_title(transcription)
            description = self.generator.generate_description(transcription, title_data['primary'])
            tags = self.generator.generate_tags(transcription)
            metadata = self.generator.generate_metadata(transcription)
            
            # Análise do tema
            theme_analysis = self.analyzer.get_main_theme(transcription)
            
            # Resultado completo
            optimization_result = {
                'video_info': {
                    'source_file': transcription_file,
                    'optimization_date': datetime.now().isoformat(),
                    'theme': theme_analysis
                },
                'seo_content': {
                    'title': {
                        'primary': title_data['primary'],
                        'alternatives': title_data['alternatives'],
                        'character_count': len(title_data['primary'])
                    },
                    'description': {
                        'content': description,
                        'character_count': len(description),
                        'within_limit': len(description) <= 5000
                    },
                    'tags': {
                        'content': tags,
                        'count': len(tags),
                        'formatted': ' | '.join(tags)
                    },
                    'metadata': metadata
                },
                'keywords': {
                    'primary': self.analyzer.extract_keywords(transcription, top_n=15),
                    'key_phrases': self.analyzer.extract_key_phrases(transcription)
                },
                'recommendations': self._generate_recommendations(theme_analysis, len(transcription))
            }
            
            return optimization_result
            
        except Exception as e:
            logger.error(f"Erro ao otimizar vídeo: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, theme_analysis: Dict, content_length: int) -> List[str]:
        """Gera recomendações personalizadas de otimização"""
        recommendations = []
        
        # Recomendações baseadas no tema
        if theme_analysis['confidence'] < 0.4:
            recommendations.append("Conteúdo tem tema disperso - considere focar em um tópico principal")
        
        # Recomendações baseadas no tamanho do conteúdo
        if content_length < 1000:
            recommendations.append("Transcrição curta - considere adicionar mais detalhes na descrição")
        elif content_length > 5000:
            recommendations.append("Conteúdo extenso - considere criar série de vídeos")
        
        # Recomendações de SEO
        recommendations.extend([
            "Use cards e end screens para direcionar para landing pages",
            "Adicione timestamps na descrição para melhor experiência",
            "Inclua call-to-action claro para conversão",
            "Considere criar thumbnail personalizada com palavras-chave"
        ])
        
        return recommendations
    
    def save_optimization_report(self, optimization_result: Dict, output_file: str = None) -> str:
        """Salva relatório de otimização em arquivo JSON"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"reports/seo_optimization_{timestamp}.json"
        
        # Cria diretório se não existir
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(optimization_result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Relatório de otimização salvo em: {output_file}")
        return output_file

# Função principal para uso direto
def optimize_video_seo(transcription_file: str, save_report: bool = True) -> Dict[str, any]:
    """
    Função principal para otimizar SEO de vídeo a partir de transcrição
    
    Args:
        transcription_file (str): Caminho para arquivo de transcrição
        save_report (bool): Se deve salvar relatório em arquivo
    
    Returns:
        Dict com todos os dados de otimização SEO
    """
    optimizer = VideoSEOOptimizer()
    result = optimizer.optimize_video_from_transcription(transcription_file)
    
    if save_report and 'error' not in result:
        optimizer.save_optimization_report(result)
    
    return result

if __name__ == "__main__":
    # Teste com a transcrição existente
    transcription_path = "Transcricoes de Videos/Video 1/f5-youtube-video1-Autorresponsabilidade_01mp4.txt"
    
    if os.path.exists(transcription_path):
        print("🚀 Iniciando otimização SEO...")
        result = optimize_video_seo(transcription_path)
        
        if 'error' not in result:
            print("\n✅ OTIMIZAÇÃO CONCLUÍDA!")
            print(f"\n📝 TÍTULO PRINCIPAL:")
            print(result['seo_content']['title']['primary'])
            
            print(f"\n🏷️ TAGS ({len(result['seo_content']['tags']['content'])}):")
            print(result['seo_content']['tags']['formatted'])
            
            print(f"\n📊 TEMA PRINCIPAL: {result['video_info']['theme']['main_theme']}")
            print(f"Confiança: {result['video_info']['theme']['confidence']:.2%}")
            
        else:
            print(f"❌ Erro: {result['error']}")
    else:
        print(f"❌ Arquivo de transcrição não encontrado: {transcription_path}") 