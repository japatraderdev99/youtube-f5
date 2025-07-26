"""
Sistema Completo de SEO para YouTube - F5 Estratégia
Adaptado do modelo Colmeia Solar Academy com integração à API do YouTube
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter
import re

from advanced_seo_generator import generate_complete_seo_package
from config import YouTubeConfig

class F5SEOSystem:
    """Sistema completo de SEO adaptado para F5 Estratégia"""
    
    def __init__(self):
        self.youtube_api_key = YouTubeConfig.API_KEY
        self.f5_tag_unique = "F5Estrategia2025"  # Tag única da F5 (equivalente ao ZDLju9ky)
        self.f5_context = self._load_f5_context()
        
    def _load_f5_context(self) -> Dict:
        """Carrega contexto específico da F5 Estratégia"""
        return {
            'canal_name': 'F5 Estratégia',
            'metodologia': 'CHAVI',
            'audiencia': 'empresários e empreendedores',
            'objetivo': 'crescimento de negócios',
            'temas_principais': [
                'autorresponsabilidade', 'liderança', 'comunicação', 'vendas',
                'marketing digital', 'gestão', 'empreendedorismo', 'estratégia'
            ],
            'links_padrao': {
                'site_principal': 'https://f5estrategia.com',
                'consultoria': 'https://f5estrategia.com/consultoria',
                'contato': 'https://f5estrategia.com/contato',
                'desenvolvimento': 'https://f5estrategia.com/desenvolvimento-pessoal',
                'gestao': 'https://f5estrategia.com/gestao-equipes',
                'comunicacao': 'https://f5estrategia.com/comunicacao-estrategica',
                'vendas': 'https://f5estrategia.com/vendas-estrategicas'
            },
            'redes_sociais': {
                'instagram': '@f5estrategia',
                'linkedin': 'F5 Estratégia',
                'whatsapp': '(11) 99999-9999'
            }
        }
    
    def search_youtube_keywords(self, base_keywords: List[str], max_results: int = 50) -> List[Tuple[str, int]]:
        """
        Pesquisa palavras-chave relacionadas usando a API do YouTube
        Simula a funcionalidade do VidIQ
        """
        try:
            all_keywords = []
            
            for keyword in base_keywords[:5]:  # Limita para não exceder quota
                # Busca vídeos relacionados à palavra-chave
                search_url = "https://www.googleapis.com/youtube/v3/search"
                params = {
                    'part': 'snippet',
                    'q': keyword + ' negócios empreendedorismo',
                    'type': 'video',
                    'maxResults': 10,
                    'key': self.youtube_api_key,
                    'order': 'relevance'
                }
                
                response = requests.get(search_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extrai palavras-chave dos títulos e descrições
                    for item in data.get('items', []):
                        title = item['snippet']['title'].lower()
                        description = item['snippet']['description'].lower()
                        
                        # Extrai palavras relevantes
                        text = f"{title} {description}"
                        words = re.findall(r'\b[a-záàâãéèêíìîóòôõúùû]{4,}\b', text)
                        
                        for word in words:
                            if word not in ['esse', 'essa', 'para', 'como', 'mais', 'você', 'seu', 'sua']:
                                all_keywords.append(word)
            
            # Conta frequência e retorna as mais relevantes
            keyword_counts = Counter(all_keywords)
            
            # Adiciona palavras-chave específicas da F5
            f5_keywords = [
                'autorresponsabilidade', 'liderança', 'gestão', 'vendas', 'marketing digital',
                'empreendedorismo', 'negócios', 'estratégia', 'crescimento', 'performance',
                'comunicação', 'desenvolvimento pessoal', 'metodologia chavi', 'f5 estratégia'
            ]
            
            for kw in f5_keywords:
                if kw not in keyword_counts:
                    keyword_counts[kw] = 5  # Score moderado para palavras F5
            
            return keyword_counts.most_common(max_results)
            
        except Exception as e:
            print(f"Erro na pesquisa do YouTube: {e}")
            # Fallback com palavras-chave básicas
            return [
                ('autorresponsabilidade', 10), ('liderança', 9), ('gestão', 8),
                ('vendas', 8), ('marketing digital', 7), ('empreendedorismo', 7),
                ('negócios', 6), ('estratégia', 6), ('crescimento', 5)
            ]
    
    def generate_f5_prompt_structured(self, transcription: str) -> str:
        """Gera prompt estruturado adaptado para F5 Estratégia"""
        
        prompt = f"""
Aja como um especialista em SEO do YouTube, sua missão é a partir da transcrição do vídeo a ser postado no canal da F5 Estratégia, cuja finalidade principal é compartilhar conteúdo de valor para sua audiência interessada em empreendedorismo, liderança, vendas, marketing digital e crescimento de negócios, criar toda estrutura de texto otimizada e assim atingir o máximo de pessoas possíveis e ser um canal de tráfego orgânico para gerar vendas de nossos treinamentos e consultorias empresariais.

O objetivo final é criar descrições de vídeos, tags otimizadas para SEO, baseadas em palavras-chave que compõem o conteúdo e que faça com que nossos vídeos estejam sempre nas primeiras posições de pesquisa nos temas relativos aos vídeos que produzirmos.

Você formulará o formato e o conteúdo do texto solicitado que reflete as regras em `<regras></regras>`. E a saída final será conforme a lista de '##Comandos Iniciais' e no formato exemplificado em `<output1></output1>`, `<output2></output2>`, `<output3></output3>`, `<output4></output4>`.

TRANSCRIÇÃO:
{transcription}

<regras>

A partir do input inicial e do comando inicial, crie:

1. A relação das palavras-chave que compõem a transcrição do vídeo que julgar que serão melhor ranqueadas nas métricas de SEO, separadas primeiramente por vírgulas entre cada palavra-chave.

2. A partir da lista de palavras-chave fornecidas após pesquisa de ranqueamento de métricas de SEO, separe todas as palavras-chave por traços (-) de forma a não ter nenhum espaço ou vírgula entre as mesmas, de forma a inserir no arquivo do vídeo a ser upado na plataforma a fim de otimizar os metadados do mesmo. Não esquecer de inserir nossa tag única que é '{self.f5_tag_unique}'

3. A partir da lista de palavras-chave fornecidas após pesquisa de ranqueamento de métricas de SEO, crie uma descrição para o vídeo inserindo todas as palavras-chave no contexto da descrição para que o SEO seja otimizado ao máximo. Siga o modelo de descrição de nossos vídeos, com links e exemplos de formatação padrão do canal. Caso necessário alguma adaptação será solicitado.

4. Dê 5 sugestões de título e de thumbnail, baseado no conteúdo do vídeo e que fomentem a curiosidade na audiência de clicar no vídeo e assistir, tente utilizar elementos principais do conteúdo do vídeo cuja a solução para esclarecer a curiosidade ao ver a thumbnail e o título seja clicar no vídeo e assistir até o final.

5. Analise se o número total de caracteres da lista de palavras-chave fornecidas para as tags do YouTube não excedeu 500 caracteres e caso falte de sugestões de palavras-chave para completar o número de caracteres o mais próximo possível desse limite.

</regras>

## Output Formatting

<output1>
Palavra chave 1, Palavra chave 2, Palavra chave 3, Palavra chave 4, Palavra chave 5, Palavra chave 6, Palavra chave 7, Palavra chave 8, Palavra chave 9, Palavra chave 10, Palavra chave n, ...., {self.f5_tag_unique} [limite de 500 caracteres]
</output1>

<output2>
Palavra-chave-1-Palavra-chave-2-Palavra-chave-3-Palavra-chave-4-Palavra-chave-5-Palavra-chave-6-Palavra-chave-7-Palavra-chave-8-Palavra-chave-9-Palavra-chave-10-Palavra-chave-n-...-{self.f5_tag_unique}
</output2>

<output3>
[Links Padrão F5 Estratégia:

🚀💼 Transforme seu Negócio com a Metodologia CHAVI: {self.f5_context['links_padrao']['consultoria']} 🚀💼

📈 Acelere seu Crescimento Empresarial: {self.f5_context['links_padrao']['site_principal']}

👥 Conecte-se com Nossa Comunidade de Empresários:
Conecte-se com especialistas e empreendedores de sucesso. Compartilhe experiências, tire dúvidas e mantenha-se atualizado com as melhores estratégias de negócios. [Participe agora: {self.f5_context['links_padrao']['contato']}]

[Conteúdo a ser criado a partir das palavras-chave do vídeo a ser postado]:

Exemplo de descrição (use como modelo, porém insira as palavras-chave e contexto do que será apresentado no vídeo em questão):

🎯 [TÍTULO DO VÍDEO]: Estratégias Comprovadas para [TEMA PRINCIPAL]! 🎯

Neste vídeo detalhado, exploramos [TEMA/CONCEITO PRINCIPAL] e como aplicar na prática para transformar seus resultados empresariais. Se você busca orientações claras e estratégias comprovadas, este vídeo é essencial para você.

🌟 Tópicos Abordados:
• [Ponto principal 1 do vídeo]
• [Ponto principal 2 do vídeo]  
• [Ponto principal 3 do vídeo]
• Metodologia CHAVI aplicada ao tema
• Cases práticos e resultados reais

📌 Mais do Nosso Canal:
LIDERANÇA DE ALTA PERFORMANCE: [link]
VENDAS ESTRATÉGICAS: [link]
COMUNICAÇÃO EMPRESARIAL: [link]

👍 Gostou do nosso conteúdo? Inscreva-se, curte e compartilhe! Deixe seus comentários e perguntas abaixo.

📱 CONECTE-SE CONOSCO:
🌐 Site: {self.f5_context['links_padrao']['site_principal']}
📸 Instagram: {self.f5_context['redes_sociais']['instagram']}
💼 LinkedIn: {self.f5_context['redes_sociais']['linkedin']}
📞 WhatsApp: {self.f5_context['redes_sociais']['whatsapp']}

#F5Estrategia #MetodologiaCHAVI #[PalavrasChavePrincipais] #Empreendedorismo #Lideranca #Vendas #MarketingDigital #CrescimentoEmpresarial
</output3>

<output4>
Título 1:
Sugestão de thumbnail 1:

Título 2:
Sugestão de thumbnail 2:

Título 3:
Sugestão de thumbnail 3:

Título 4:
Sugestão de thumbnail 4:

Título 5:
Sugestão de thumbnail 5:
</output4>

<output5>
Palavras-chave sugeridas:
</output5>

## Comandos Iniciais
/1 = escreva as palavras-chave para serem utilizadas no SEO do vídeo a ser postado baseado na transcrição inputada e escreva no formato `<output1></output1>`.

/2 = A partir da lista de palavras-chave fornecidas, separe todas as palavras-chave por traços (-) de forma a não ter nenhum espaço ou vírgula entre as mesmas. Não esquecer de inserir nossa tag única que é '{self.f5_tag_unique}' escreva no formato `<output2></output2>`.

/3 = Crie a descrição do vídeo baseado nas regras estabelecidas e no padrão do nosso canal, baseado no exemplo fornecido e escreva no formato `<output3></output3>`.

/4 = Dê 5 sugestões de título e de thumbnail, baseado no conteúdo do vídeo e que fomentem a curiosidade na audiência de clicar no vídeo e assistir, escreva no formato `<output4></output4>`

/5 = Analise se o número total de caracteres da lista de palavras-chave fornecidas para as tags do YouTube não excedeu 500 caracteres e caso falte de sugestões de palavras-chave para completar o número de caracteres o mais próximo possível desse limite e escreva no formato `<output5></output5>`.
"""
        return prompt
    
    def process_transcription_f5_style(self, transcription_file: str) -> Dict:
        """
        Processa transcrição no estilo F5 Estratégia
        Integra pesquisa do YouTube + geração de conteúdo
        """
        try:
            # Lê transcrição
            with open(transcription_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
            
            # Primeiro, faz análise básica para extrair palavras-chave iniciais
            basic_seo = generate_complete_seo_package(transcription_file)
            
            if 'error' in basic_seo:
                return {'error': basic_seo['error']}
            
            # Extrai palavras-chave iniciais
            initial_keywords = [kw[0] for kw in basic_seo['keywords']['primary'][:10]]
            
            # Pesquisa no YouTube para palavras-chave relacionadas
            print("🔍 Pesquisando palavras-chave no YouTube...")
            youtube_keywords = self.search_youtube_keywords(initial_keywords)
            
            # Combina palavras-chave
            all_keywords = []
            
            # Adiciona palavras do YouTube
            for kw, score in youtube_keywords[:15]:
                all_keywords.append(kw)
            
            # Adiciona palavras específicas do tema detectado
            theme = basic_seo.get('video_info', {}).get('detected_theme', 'desenvolvimento')
            theme_keywords = {
                'autorresponsabilidade': [
                    'desenvolvimento pessoal', 'autoconhecimento', 'responsabilidade',
                    'crescimento profissional', 'mindset', 'transformação pessoal'
                ],
                'lideranca': [
                    'gestão de equipes', 'alta performance', 'motivação',
                    'engajamento', 'cultura organizacional', 'feedback'
                ],
                'comunicacao': [
                    'comunicação estratégica', 'oratória', 'apresentação',
                    'persuasão', 'influência', 'networking'
                ],
                'vendas': [
                    'técnicas de vendas', 'negociação', 'fechamento',
                    'conversão', 'funil de vendas', 'prospecção'
                ]
            }
            
            if theme in theme_keywords:
                all_keywords.extend(theme_keywords[theme])
            
            # Remove duplicatas
            unique_keywords = list(dict.fromkeys(all_keywords))
            
            # Gera os 4 outputs no formato exato dos exemplos
            output1 = self._generate_output1(unique_keywords)
            output2 = self._generate_output2(unique_keywords)
            output3 = self._generate_output3(transcription, unique_keywords, theme)
            output4 = self._generate_output4(transcription, unique_keywords)
            
            return {
                'success': True,
                'transcription_file': transcription_file,
                'theme_detected': theme,
                'youtube_keywords_found': len(youtube_keywords),
                'outputs': {
                    'tags_virgula': output1,
                    'metadados_traco': output2, 
                    'descricao_completa': output3,
                    'titulos_thumbnails': output4
                },
                'keywords_used': unique_keywords[:20]
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _generate_output1(self, keywords: List[str]) -> str:
        """Gera output1: tags separadas por vírgula"""
        # Limita a 500 caracteres
        tags = []
        current_length = 0
        
        for keyword in keywords:
            tag_length = len(keyword) + 2  # +2 para vírgula e espaço
            if current_length + tag_length + len(self.f5_tag_unique) + 2 <= 500:
                tags.append(keyword)
                current_length += tag_length
            else:
                break
        
        # Adiciona tag única da F5
        tags.append(self.f5_tag_unique)
        
        return ', '.join(tags)
    
    def _generate_output2(self, keywords: List[str]) -> str:
        """Gera output2: metadados separados por traços"""
        # Usa as mesmas keywords do output1, mas com traços
        tags = []
        current_length = 0
        
        for keyword in keywords:
            keyword_clean = keyword.replace(' ', '-').replace(',', '')
            tag_length = len(keyword_clean) + 1  # +1 para traço
            if current_length + tag_length + len(self.f5_tag_unique) + 1 <= 500:
                tags.append(keyword_clean)
                current_length += tag_length
            else:
                break
        
        # Adiciona tag única da F5
        tags.append(self.f5_tag_unique)
        
        return '-'.join(tags)
    
    def _generate_output3(self, transcription: str, keywords: List[str], theme: str) -> str:
        """Gera output3: descrição completa do vídeo"""
        
        # Mapeia tema para landing page
        theme_pages = {
            'autorresponsabilidade': self.f5_context['links_padrao']['desenvolvimento'],
            'lideranca': self.f5_context['links_padrao']['gestao'],
            'comunicacao': self.f5_context['links_padrao']['comunicacao'],
            'vendas': self.f5_context['links_padrao']['vendas']
        }
        
        landing_page = theme_pages.get(theme, self.f5_context['links_padrao']['consultoria'])
        
        # Extrai pontos principais da transcrição (simplificado)
        sentences = transcription.split('.')[:10]
        main_points = []
        for sentence in sentences:
            if len(sentence.strip()) > 50 and any(kw in sentence.lower() for kw in keywords[:5]):
                clean_sentence = sentence.strip().replace('\n', ' ')
                if clean_sentence:
                    main_points.append(clean_sentence[:100] + '...')
                if len(main_points) >= 3:
                    break
        
        # Se não encontrar pontos, usa pontos genéricos
        if len(main_points) < 3:
            theme_points = {
                'autorresponsabilidade': [
                    'Como desenvolver consciência sobre suas escolhas e decisões',
                    'Estratégias para assumir controle total dos seus resultados',
                    'A diferença entre culpa e responsabilidade no crescimento profissional'
                ],
                'lideranca': [
                    'Técnicas para motivar e engajar equipes de alta performance',
                    'Como desenvolver uma cultura organizacional sólida',
                    'Estratégias de feedback eficaz para desenvolvimento de talentos'
                ],
                'comunicacao': [
                    'Técnicas de comunicação persuasiva e influência',
                    'Como estruturar apresentações de impacto',
                    'Estratégias para networking e relacionamentos profissionais'
                ],
                'vendas': [
                    'Técnicas de fechamento e superação de objeções',
                    'Como estruturar um processo de vendas eficaz',
                    'Estratégias para aumentar conversão e ticket médio'
                ]
            }
            main_points = theme_points.get(theme, main_points)
        
        # Monta descrição
        theme_titles = {
            'autorresponsabilidade': 'Autorresponsabilidade',
            'lideranca': 'Liderança de Alta Performance',
            'comunicacao': 'Comunicação Estratégica',
            'vendas': 'Vendas Estratégicas'
        }
        
        titulo_tema = theme_titles.get(theme, 'Desenvolvimento Empresarial')
        
        description = f"""🚀💼 Transforme seu Negócio com a Metodologia CHAVI: {self.f5_context['links_padrao']['consultoria']} 🚀💼

📈 Acelere seu Crescimento Empresarial: {self.f5_context['links_padrao']['site_principal']}

👥 Conecte-se com Nossa Comunidade de Empresários:
Conecte-se com especialistas e empreendedores de sucesso. Compartilhe experiências, tire dúvidas e mantenha-se atualizado com as melhores estratégias de negócios. [Participe agora: {self.f5_context['links_padrao']['contato']}]

🎯 {titulo_tema}: Estratégias Comprovadas para o Sucesso Empresarial! 🎯

Neste vídeo detalhado, exploramos {theme} e como aplicar na prática para transformar seus resultados empresariais. Se você busca orientações claras e estratégias comprovadas, este vídeo é essencial para você.

🌟 Tópicos Abordados:"""

        for i, point in enumerate(main_points[:4], 1):
            description += f"\n• {point}"
        
        description += f"""
• Metodologia CHAVI aplicada ao tema
• Cases práticos e resultados reais

📌 Mais do Nosso Canal:
LIDERANÇA DE ALTA PERFORMANCE: {self.f5_context['links_padrao']['gestao']}
VENDAS ESTRATÉGICAS: {self.f5_context['links_padrao']['vendas']}
COMUNICAÇÃO EMPRESARIAL: {self.f5_context['links_padrao']['comunicacao']}

👍 Gostou do nosso conteúdo? Inscreva-se, curta e compartilhe! Deixe seus comentários e perguntas abaixo.

📱 CONECTE-SE CONOSCO:
🌐 Site: {self.f5_context['links_padrao']['site_principal']}
📸 Instagram: {self.f5_context['redes_sociais']['instagram']}
💼 LinkedIn: {self.f5_context['redes_sociais']['linkedin']}
📞 WhatsApp: {self.f5_context['redes_sociais']['whatsapp']}

#F5Estrategia #MetodologiaCHAVI #{' #'.join(keywords[:6]).replace(' ', '')} #Empreendedorismo #Lideranca #Vendas #MarketingDigital #CrescimentoEmpresarial"""
        
        return description
    
    def _generate_output4(self, transcription: str, keywords: List[str]) -> str:
        """Gera output4: sugestões de títulos e thumbnails"""
        
        # Gera títulos baseados nas palavras-chave principais
        main_keyword = keywords[0] if keywords else 'desenvolvimento empresarial'
        
        titles_thumbnails = f"""Título 1: {main_keyword.title()}: O Segredo do Sucesso Empresarial | F5 Estratégia
Sugestão de thumbnail 1: Texto "{main_keyword.upper()}" em destaque + logo F5 + expressão confiante do apresentador

Título 2: Como Dominar {main_keyword.title()} e Transformar seus Resultados | F5
Sugestão de thumbnail 2: Antes/depois visual + palavra "{main_keyword.upper()}" + seta de crescimento

Título 3: {main_keyword.title()} na Prática: Estratégias Comprovadas | F5 Estratégia  
Sugestão de thumbnail 3: Checklist visual + "{main_keyword.upper()}" + elementos da metodologia CHAVI

Título 4: O Poder de {main_keyword.title()} para Empresários de Sucesso | F5
Sugestão de thumbnail 4: Gráfico de crescimento + "{main_keyword.upper()}" + logo F5 + cores corporativas

Título 5: Desenvolva {main_keyword.title()} em 30 Dias | Método F5 Estratégia
Sugestão de thumbnail 5: Calendário/cronômetro + "{main_keyword.upper()}" + call-to-action visual"""
        
        return titles_thumbnails
    
    def save_f5_youtube_files(self, transcription_file: str) -> Dict:
        """
        Salva arquivos no formato exato dos exemplos de energia solar
        Adaptado para F5 Estratégia
        """
        try:
            # Processa transcrição
            result = self.process_transcription_f5_style(transcription_file)
            
            if 'error' in result:
                return result
            
            # Diretório do vídeo
            video_dir = os.path.dirname(transcription_file)
            
            # 1. ARQUIVO TITULO
            titulo_content = result['outputs']['titulos_thumbnails'].split('\n')[0].replace('Título 1: ', '')
            titulo_file = os.path.join(video_dir, 'titulo.txt')
            with open(titulo_file, 'w', encoding='utf-8') as f:
                f.write(titulo_content)
            
            # 2. ARQUIVO DESCRIÇÃO  
            descricao_file = os.path.join(video_dir, 'descricao.txt')
            with open(descricao_file, 'w', encoding='utf-8') as f:
                f.write(result['outputs']['descricao_completa'])
            
            # 3. ARQUIVO TAGS (vírgulas)
            tags_file = os.path.join(video_dir, 'tags.txt')
            with open(tags_file, 'w', encoding='utf-8') as f:
                f.write(result['outputs']['tags_virgula'])
            
            # 4. ARQUIVO METADADOS (traços)  
            metadados_file = os.path.join(video_dir, 'metadados.txt')
            with open(metadados_file, 'w', encoding='utf-8') as f:
                f.write(result['outputs']['metadados_traco'])
            
            # 5. ARQUIVO RESUMO (bonus)
            resumo_data = {
                'video_info': {
                    'tema_detectado': result['theme_detected'],
                    'keywords_youtube_encontradas': result['youtube_keywords_found'],
                    'titulo_caracteres': len(titulo_content),
                    'descricao_caracteres': len(result['outputs']['descricao_completa']),
                    'tags_caracteres': len(result['outputs']['tags_virgula']),
                    'metadados_caracteres': len(result['outputs']['metadados_traco']),
                    'data_processamento': datetime.now().isoformat()
                },
                'arquivos_criados': [
                    'titulo.txt', 'descricao.txt', 'tags.txt', 'metadados.txt'
                ],
                'keywords_utilizadas': result['keywords_used']
            }
            
            resumo_file = os.path.join(video_dir, 'resumo_f5_seo.json')
            with open(resumo_file, 'w', encoding='utf-8') as f:
                json.dump(resumo_data, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'video_directory': video_dir,
                'files_created': {
                    'titulo': titulo_file,
                    'descricao': descricao_file,
                    'tags': tags_file,
                    'metadados': metadados_file,
                    'resumo': resumo_file
                },
                'content_summary': {
                    'titulo': titulo_content,
                    'tema': result['theme_detected'],
                    'keywords_count': len(result['keywords_used']),
                    'youtube_research': result['youtube_keywords_found']
                }
            }
            
        except Exception as e:
            return {'error': str(e)}

def process_f5_video(transcription_file: str) -> None:
    """Função principal para processar vídeo F5"""
    
    system = F5SEOSystem()
    
    print("🚀 SISTEMA F5 SEO - PROCESSANDO VÍDEO...")
    print("🔍 Integrando com API do YouTube para pesquisa de palavras-chave...")
    
    result = system.save_f5_youtube_files(transcription_file)
    
    if result.get('success'):
        print("\n✅ ARQUIVOS F5 CRIADOS COM SUCESSO!")
        print(f"📁 Diretório: {result['video_directory']}")
        print(f"🎯 Tema detectado: {result['content_summary']['tema']}")
        print(f"🔍 Palavras-chave do YouTube: {result['content_summary']['youtube_research']}")
        print(f"📝 Título: {result['content_summary']['titulo']}")
        
        print(f"\n📋 ARQUIVOS CRIADOS (formato exato dos exemplos):")
        for tipo, caminho in result['files_created'].items():
            print(f"   ✓ {os.path.basename(caminho)}")
        
        print(f"\n🔄 PRÓXIMOS PASSOS:")
        print(f"1. Use titulo.txt no campo título do YouTube")
        print(f"2. Use descricao.txt no campo descrição do YouTube")
        print(f"3. Use tags.txt no campo tags do YouTube")
        print(f"4. Use metadados.txt nos nomes dos arquivos de vídeo/thumb")
        
    else:
        print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")

if __name__ == "__main__":
    # Testa com o vídeo de autorresponsabilidade
    transcription_path = "Transcricoes de Videos/Video 1/f5-youtube-video1-Autorresponsabilidade_01mp4.txt"
    
    if os.path.exists(transcription_path):
        process_f5_video(transcription_path)
    else:
        print(f"❌ Arquivo não encontrado: {transcription_path}") 