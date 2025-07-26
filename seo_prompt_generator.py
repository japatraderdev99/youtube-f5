"""
Gerador de Prompts Estruturados para SEO - F5 Estratégia
Sistema automatizado para criação de conteúdo SEO a partir de transcrições
"""

import json
import os
from datetime import datetime
from typing import Dict, List
from advanced_seo_generator import generate_complete_seo_package

class SEOPromptGenerator:
    """Gerador de prompts estruturados para automatização completa"""
    
    def __init__(self):
        self.template_prompts = self._load_template_prompts()
    
    def _load_template_prompts(self) -> Dict[str, str]:
        """Carrega templates de prompts para diferentes temas"""
        return {
            'universal': """
SISTEMA DE OTIMIZAÇÃO SEO YOUTUBE - F5 ESTRATÉGIA

TRANSCRIÇÃO:
{transcription}

INSTRUÇÕES:
Analise a transcrição acima e gere conteúdo SEO otimizado seguindo estas especificações:

1. TÍTULO (máx. 100 caracteres):
   - Inclua palavras-chave principais
   - Use formato: "[Tema Principal]: [Benefício/Resultado] | F5 Estratégia"
   - Seja chamativo e otimizado para busca

2. DESCRIÇÃO (máx. 5000 caracteres):
   - Introdução com palavras-chave (150 caracteres)
   - 3-5 pontos principais do vídeo
   - Call-to-action para landing page da F5
   - Links para redes sociais e contato
   - Hashtags relevantes (#F5Estrategia, #tema, etc.)
   - Metodologia CHAVI explicada
   - Rodapé com copyright

3. TAGS (15 tags separadas por traços):
   - f5-estrategia, metodologia-chavi, empreendedorismo
   - Tags específicas do tema detectado
   - Palavras-chave do conteúdo

4. METADADOS PARA ARQUIVO:
   - Title: [título gerado]
   - Keywords: [principais palavras-chave separadas por traços]
   - Category: [tema detectado]
   - Author: F5 Estratégia
   - Date: {date}

CONTEXTO F5 ESTRATÉGIA:
- Metodologia CHAVI (Campanha, Humanização, Anúncios, Vendas, Inteligência)
- Foco em empresários e crescimento de negócios
- Tom: Sábio + Herói (confiável, analítico, determinado)
- Landing pages: desenvolvimento-pessoal, gestao-equipes, comunicacao-estrategica, vendas-estrategicas

FORMATO DE SAÍDA:
```json
{{
  "titulo": "...",
  "descricao": "...",
  "tags": ["tag1", "tag2", ...],
  "metadados": {{...}},
  "tema_detectado": "...",
  "recomendacoes": ["...", "..."]
}}
```
""",
            
            'autorresponsabilidade': """
OTIMIZAÇÃO SEO ESPECÍFICA - AUTORRESPONSABILIDADE

TRANSCRIÇÃO:
{transcription}

FOCO ESPECÍFICO: AUTORRESPONSABILIDADE
Gere conteúdo otimizado para autorresponsabilidade, desenvolvimento pessoal e crescimento profissional.

TÍTULO SUGERIDO:
"Autorresponsabilidade: O Segredo do Sucesso Profissional | F5 Estratégia"

PALAVRAS-CHAVE PRIORITÁRIAS:
autorresponsabilidade, autoconhecimento, desenvolvimento pessoal, consciência, responsabilidade, crescimento profissional, mindset, transformação pessoal, decisões, valores

LANDING PAGE:
https://f5estrategia.com/desenvolvimento-pessoal

CTA ESPECÍFICO:
"Transforme sua mentalidade e alcance resultados extraordinários"

PONTOS DE DESTAQUE:
- Como desenvolver consciência sobre escolhas e decisões
- Estratégias para assumir controle dos resultados
- Diferença entre culpa e responsabilidade
- Técnicas de autorreflexão prática
- Cases de transformação pessoal
""",
            
            'comunicacao': """
OTIMIZAÇÃO SEO ESPECÍFICA - COMUNICAÇÃO

TRANSCRIÇÃO:
{transcription}

FOCO ESPECÍFICO: COMUNICAÇÃO ESTRATÉGICA
Gere conteúdo otimizado para comunicação, oratória, persuasão e influência.

TÍTULO SUGERIDO:
"Comunicação Estratégica: Como Influenciar e Persuadir | F5 Estratégia"

PALAVRAS-CHAVE PRIORITÁRIAS:
comunicação estratégica, oratória, apresentação, persuasão, influência, networking, storytelling, negociação, relacionamento profissional

LANDING PAGE:
https://f5estrategia.com/comunicacao-estrategica

CTA ESPECÍFICO:
"Comunique-se com impacto e autoridade"
""",
            
            'lideranca': """
OTIMIZAÇÃO SEO ESPECÍFICA - LIDERANÇA

TRANSCRIÇÃO:
{transcription}

FOCO ESPECÍFICO: LIDERANÇA E GESTÃO
Gere conteúdo otimizado para liderança, gestão de equipes e alta performance.

TÍTULO SUGERIDO:
"Liderança de Alta Performance: Estratégias Comprovadas | F5 Estratégia"

PALAVRAS-CHAVE PRIORITÁRIAS:
liderança, gestão de equipes, alta performance, motivação, engajamento, cultura organizacional, feedback, desenvolvimento de talentos

LANDING PAGE:
https://f5estrategia.com/gestao-equipes

CTA ESPECÍFICO:
"Torne-se um líder extraordinário"
""",
            
            'vendas': """
OTIMIZAÇÃO SEO ESPECÍFICA - VENDAS

TRANSCRIÇÃO:
{transcription}

FOCO ESPECÍFICO: VENDAS E NEGOCIAÇÃO
Gere conteúdo otimizado para técnicas de vendas, negociação e fechamento.

TÍTULO SUGERIDO:
"Técnicas de Vendas que Funcionam | F5 Estratégia"

PALAVRAS-CHAVE PRIORITÁRIAS:
vendas, negociação, fechamento, conversão, funil de vendas, prospecção, relacionamento comercial, objeções, técnicas de vendas

LANDING PAGE:
https://f5estrategia.com/vendas-estrategicas

CTA ESPECÍFICO:
"Multiplique seus resultados em vendas"
"""
        }
    
    def generate_structured_prompt(self, transcription_file: str, output_file: str = None) -> Dict[str, str]:
        """Gera prompt estruturado para uso futuro com IA"""
        try:
            # Primeiro, executa análise completa
            seo_result = generate_complete_seo_package(transcription_file)
            
            if 'error' in seo_result:
                return {'error': seo_result['error']}
            
            # Lê transcrição
            with open(transcription_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
            
            # Detecta tema para escolher prompt específico
            detected_theme = seo_result.get('video_info', {}).get('detected_theme', 'universal')
            
            # Seleciona template apropriado
            if detected_theme in self.template_prompts:
                template = self.template_prompts[detected_theme]
            else:
                template = self.template_prompts['universal']
            
            # Gera prompt preenchido
            prompt = template.format(
                transcription=transcription,
                date=datetime.now().strftime('%Y-%m-%d')
            )
            
            # Dados do resultado atual como exemplo
            example_result = {
                'titulo': seo_result['seo_content']['title']['primary'],
                'descricao': seo_result['seo_content']['description']['content'],
                'tags': seo_result['seo_content']['tags']['content'],
                'metadados': seo_result['seo_content']['metadata'],
                'tema_detectado': detected_theme,
                'recomendacoes': seo_result['recommendations']
            }
            
            # Compila resultado final
            result = {
                'prompt_estruturado': prompt,
                'exemplo_resultado': example_result,
                'tema_detectado': detected_theme,
                'arquivo_fonte': transcription_file,
                'data_geracao': datetime.now().isoformat()
            }
            
            # Salva se especificado
            if output_file:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            
            return result
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_batch_prompts(self, transcription_directory: str) -> Dict[str, any]:
        """Gera prompts para múltiplas transcrições em lote"""
        results = {}
        
        # Busca arquivos de transcrição
        transcription_files = []
        for root, dirs, files in os.walk(transcription_directory):
            for file in files:
                if file.endswith('.txt'):
                    transcription_files.append(os.path.join(root, file))
        
        # Processa cada arquivo
        for file_path in transcription_files:
            try:
                file_name = os.path.basename(file_path)
                print(f"Processando: {file_name}")
                
                result = self.generate_structured_prompt(file_path)
                results[file_name] = result
                
            except Exception as e:
                results[file_name] = {'error': str(e)}
        
        # Salva resultados em lote
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        batch_output = f"reports/batch_seo_prompts_{timestamp}.json"
        
        os.makedirs('reports', exist_ok=True)
        with open(batch_output, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        return {
            'processed_files': len(transcription_files),
            'successful': len([r for r in results.values() if 'error' not in r]),
            'failed': len([r for r in results.values() if 'error' in r]),
            'output_file': batch_output,
            'results': results
        }
    
    def create_automation_template(self) -> str:
        """Cria template final para automação completa"""
        return """
# TEMPLATE DE AUTOMAÇÃO SEO - F5 ESTRATÉGIA

## USO RÁPIDO
1. Substitua {TRANSCRICAO} pela transcrição do vídeo
2. Execute o prompt em qualquer IA (ChatGPT, Claude, Gemini)
3. Receba título, descrição, tags e metadados prontos para uso

## PROMPT UNIVERSAL
```
SISTEMA DE OTIMIZAÇÃO SEO YOUTUBE - F5 ESTRATÉGIA

TRANSCRIÇÃO:
{TRANSCRICAO}

INSTRUÇÕES:
Analise a transcrição e gere:

1. TÍTULO (máx. 100 chars): [Tema]: [Benefício] | F5 Estratégia
2. DESCRIÇÃO (máx. 5000 chars): Intro + pontos principais + CTA + links + hashtags
3. TAGS (15 tags): f5-estrategia, tema-especifico, palavras-chave-conteudo
4. METADADOS: title, keywords, category, author: F5 Estratégia

CONTEXTO: F5 = Metodologia CHAVI, empresários, tom confiável+analítico

FORMATO JSON:
{
  "titulo": "...",
  "descricao": "...",
  "tags": [...],
  "metadados": {...}
}
```

## TEMAS ESPECÍFICOS
- Autorresponsabilidade: desenvolvimento-pessoal
- Liderança: gestao-equipes  
- Comunicação: comunicacao-estrategica
- Vendas: vendas-estrategicas

## LANDING PAGES F5
- Geral: https://f5estrategia.com
- Desenvolvimento: https://f5estrategia.com/desenvolvimento-pessoal
- Gestão: https://f5estrategia.com/gestao-equipes
- Comunicação: https://f5estrategia.com/comunicacao-estrategica
- Vendas: https://f5estrategia.com/vendas-estrategicas
- Contato: https://f5estrategia.com/contato

## ESTRUTURA PADRÃO DESCRIÇÃO
🎯 [TÍTULO]
[Introdução 150 chars com palavras-chave]

📋 PRINCIPAIS PONTOS:
✅ [Ponto 1]
✅ [Ponto 2] 
✅ [Ponto 3]

🔍 PALAVRAS-CHAVE: [6 principais]
🚀 [CTA ESPECÍFICO DO TEMA]

👉 Landing page específica
📞 https://f5estrategia.com/contato

💡 METODOLOGIA CHAVI:
• Campanha • Humanização • Anúncios • Vendas • Inteligência

🔔 Inscreva-se para mais conteúdos
📱 Redes sociais

#F5Estrategia #[Tema] #DesenvolvimentoProfissional #Empreendedorismo

---
© 2025 F5 Estratégia - Transformando negócios através de estratégias comprovadas.
"""

def quick_optimize(transcription_file: str) -> None:
    """Função rápida para otimização com saída formatada"""
    generator = SEOPromptGenerator()
    
    print("🚀 GERANDO OTIMIZAÇÃO SEO COMPLETA...")
    
    # Gera análise completa
    result = generator.generate_structured_prompt(transcription_file)
    
    if 'error' in result:
        print(f"❌ Erro: {result['error']}")
        return
    
    exemplo = result['exemplo_resultado']
    
    print(f"\n✅ OTIMIZAÇÃO CONCLUÍDA!")
    print(f"🎯 TEMA: {exemplo['tema_detectado']}")
    print(f"📝 TÍTULO ({len(exemplo['titulo'])} chars):")
    print(f"   {exemplo['titulo']}")
    
    print(f"\n🏷️ TAGS ({len(exemplo['tags'])} tags):")
    print(f"   {' | '.join(exemplo['tags'])}")
    
    print(f"\n📊 DESCRIÇÃO ({len(exemplo['descricao'])} chars):")
    print(f"   {exemplo['descricao'][:200]}...")
    
    print(f"\n💡 RECOMENDAÇÕES:")
    for i, rec in enumerate(exemplo['recomendacoes'][:3], 1):
        print(f"   {i}. {rec}")
    
    # Salva prompt estruturado
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    prompt_file = f"reports/prompt_estruturado_{timestamp}.txt"
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(result['prompt_estruturado'])
    
    print(f"\n💾 Prompt estruturado salvo em: {prompt_file}")
    print("\n🔄 PRÓXIMOS PASSOS:")
    print("1. Use o prompt salvo em qualquer IA")
    print("2. Substitua a transcrição no template")
    print("3. Receba conteúdo SEO otimizado instantaneamente")

if __name__ == "__main__":
    # Execução rápida
    transcription_path = "Transcricoes de Videos/Video 1/f5-youtube-video1-Autorresponsabilidade_01mp4.txt"
    
    if os.path.exists(transcription_path):
        quick_optimize(transcription_path)
    else:
        print(f"❌ Arquivo não encontrado: {transcription_path}")
    
    # Gera template de automação
    generator = SEOPromptGenerator()
    template = generator.create_automation_template()
    
    with open('TEMPLATE_AUTOMACAO_SEO.md', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"\n📋 Template de automação criado: TEMPLATE_AUTOMACAO_SEO.md") 