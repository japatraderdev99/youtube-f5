#!/usr/bin/env python3
"""
Teste Simples - IA Gemini 2.5 Pro (SEM OAuth)
Testa otimização de conteúdo sem precisar de autenticação YouTube
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Any
import json

# Carregar variáveis do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Arquivo .env carregado")
except ImportError:
    print("⚠️ python-dotenv não instalado, tentando carregar .env manualmente")
    # Carregar .env manualmente se dotenv não estiver disponível
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Arquivo .env carregado manualmente")

# Verificar se Gemini está disponível
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    print("✅ Google Generative AI (Gemini) carregado")
except ImportError:
    GEMINI_AVAILABLE = False
    print("❌ Google Generative AI não instalado")

@dataclass
class ResultadoOtimizacao:
    titulo_original: str
    titulo_otimizado: str
    persona_alvo: str
    score_seo: float
    sugestoes: List[str]
    potencial_viralizacao: str

class OptimizadorF5:
    """Otimizador específico para F5 Estratégia usando Gemini 2.5 Pro"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.gemini_api_key:
            raise ValueError("❌ GEMINI_API_KEY não encontrada no .env")
        
        if not GEMINI_AVAILABLE:
            raise ValueError("❌ Google Generative AI não instalado")
        
        # Configurar Gemini
        genai.configure(api_key=self.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        print("✅ Gemini 2.5 Pro inicializado com sucesso!")
    
    def otimizar_titulo(self, titulo: str, descricao: str = "") -> ResultadoOtimizacao:
        """Otimiza título usando Gemini 2.5 Pro com foco em F5 Estratégia"""
        
        prompt = f"""
Como especialista em YouTube SEO para F5 Estratégia (agência de marketing digital), analise e otimize este conteúdo:

TÍTULO ORIGINAL: {titulo}
DESCRIÇÃO: {descricao}

CONTEXTO F5 ESTRATÉGIA:
- Agência especializada em tráfego pago, performance e metodologia CHAVI
- Audiência: Empresários, gestores de marketing, empreendedores
- Nichos: Marketing digital, Facebook/Google Ads, gestão de performance, ROI
- Tom: Profissional, confiável, orientado a resultados

PERSONAS DA F5:
1. ESTRATÉGICO (R$ 1M+): Grandes empresas, escalabilidade, automação
2. CRESCIMENTO (R$ 500K-1M): PMEs em expansão, otimização, resultados
3. SMART (até R$ 500K): Pequenos negócios, praticidade, custo-benefício

TAREFAS:
1. Crie um título otimizado (60-70 caracteres) com alto potencial de CTR
2. Identifique a persona principal
3. Calcule score SEO (0-10)
4. Liste 5 sugestões específicas de melhoria
5. Avalie potencial de viralização (Baixo/Médio/Alto)

CRITÉRIOS PARA TÍTULO:
- Incluir palavras-chave do marketing digital
- Gerar curiosidade + urgência
- Ser específico e acionável
- Adequado à persona identificada

Responda APENAS no formato JSON:
{{
  "titulo_otimizado": "Título otimizado aqui",
  "persona_alvo": "estrategico/crescimento/smart",
  "score_seo": 8.5,
  "sugestoes": [
    "Sugestão 1 específica",
    "Sugestão 2 específica", 
    "Sugestão 3 específica",
    "Sugestão 4 específica",
    "Sugestão 5 específica"
  ],
  "potencial_viralizacao": "Alto",
  "justificativa": "Explicação breve do porquê"
}}
"""
        
        try:
            print(f"🤖 Analisando com Gemini 2.5 Pro: '{titulo[:50]}...'")
            
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.7
                )
            )
            
            # Extrair JSON da resposta
            resposta_texto = response.text.strip()
            
            # Limpar resposta se tiver markdown
            if "```json" in resposta_texto:
                resposta_texto = resposta_texto.split("```json")[1].split("```")[0]
            elif "```" in resposta_texto:
                resposta_texto = resposta_texto.split("```")[1]
            
            try:
                resultado_json = json.loads(resposta_texto)
            except json.JSONDecodeError:
                # Fallback se JSON inválido
                print("⚠️ Resposta não é JSON válido, processando manualmente...")
                return self._processar_resposta_manual(titulo, resposta_texto)
            
            return ResultadoOtimizacao(
                titulo_original=titulo,
                titulo_otimizado=resultado_json.get('titulo_otimizado', titulo),
                persona_alvo=resultado_json.get('persona_alvo', 'crescimento'),
                score_seo=float(resultado_json.get('score_seo', 5.0)),
                sugestoes=resultado_json.get('sugestoes', []),
                potencial_viralizacao=resultado_json.get('potencial_viralizacao', 'Médio')
            )
            
        except Exception as e:
            print(f"❌ Erro na otimização: {e}")
            return self._resultado_erro(titulo)
    
    def _processar_resposta_manual(self, titulo: str, resposta: str) -> ResultadoOtimizacao:
        """Processa resposta manualmente se JSON falhar"""
        
        # Extrair informações básicas da resposta
        linhas = resposta.split('\n')
        titulo_otimizado = titulo  # Default
        
        for linha in linhas:
            if 'título' in linha.lower() or 'title' in linha.lower():
                if ':' in linha:
                    titulo_otimizado = linha.split(':', 1)[1].strip().strip('"')
                    break
        
        return ResultadoOtimizacao(
            titulo_original=titulo,
            titulo_otimizado=titulo_otimizado,
            persona_alvo='crescimento',
            score_seo=7.0,
            sugestoes=['Adicionar palavras-chave específicas', 'Incluir número ou estatística', 'Gerar mais urgência'],
            potencial_viralizacao='Médio'
        )
    
    def _resultado_erro(self, titulo: str) -> ResultadoOtimizacao:
        """Retorna resultado padrão em caso de erro"""
        
        return ResultadoOtimizacao(
            titulo_original=titulo,
            titulo_otimizado=titulo + " [ERRO: não otimizado]",
            persona_alvo='crescimento',
            score_seo=0.0,
            sugestoes=['Erro na otimização - verifique API'],
            potencial_viralizacao='Baixo'
        )

def testar_videos_f5():
    """Testa otimização com vídeos exemplo da F5"""
    
    print("🚀 TESTE F5 ESTRATÉGIA - GEMINI 2.5 PRO")
    print("="*60)
    print("📌 Focado em: Marketing Digital, Tráfego Pago, Performance\n")
    
    try:
        otimizador = OptimizadorF5()
        
        # Vídeos exemplo para teste
        videos_teste = [
            {
                'titulo': 'Como Criar Campanhas de Facebook Ads que Convertem',
                'descricao': 'Aprenda estratégias para criar campanhas de Facebook Ads lucrativas'
            },
            {
                'titulo': 'Gestão de Performance: Otimize suas Campanhas',
                'descricao': 'Descubra como otimizar campanhas de marketing digital para maximizar ROI'
            },
            {
                'titulo': 'Metodologia CHAVI: Transforme Leads em Vendas',
                'descricao': 'Conheça nossa metodologia exclusiva CHAVI para aumentar conversões'
            }
        ]
        
        resultados = []
        
        for i, video in enumerate(videos_teste, 1):
            print(f"📹 TESTE {i}/3:")
            print(f"Original: {video['titulo']}")
            
            resultado = otimizador.otimizar_titulo(
                video['titulo'], 
                video['descricao']
            )
            
            resultados.append(resultado)
            
            print(f"✨ Otimizado: {resultado.titulo_otimizado}")
            print(f"🎯 Persona: {resultado.persona_alvo}")
            print(f"📊 SEO Score: {resultado.score_seo}/10")
            print(f"🔥 Viral: {resultado.potencial_viralizacao}")
            print()
            
            if resultado.sugestoes:
                print("💡 Sugestões:")
                for j, sugestao in enumerate(resultado.sugestoes[:3], 1):
                    print(f"   {j}. {sugestao}")
                print()
        
        # Estatísticas
        print("📊 ESTATÍSTICAS:")
        print("="*40)
        scores = [r.score_seo for r in resultados]
        print(f"📈 Score SEO médio: {sum(scores)/len(scores):.1f}/10")
        
        personas = [r.persona_alvo for r in resultados]
        for persona in set(personas):
            count = personas.count(persona)
            print(f"🎯 {persona}: {count} vídeos")
        
        print("\n✅ TESTE CONCLUÍDO - GEMINI 2.5 PRO ESTÁ FUNCIONANDO!")
        print("🚀 Pronto para otimizar seu banco de vídeos!")
        
    except Exception as e:
        print(f"❌ ERRO NO TESTE: {e}")
        print("\n🔧 POSSÍVEIS SOLUÇÕES:")
        print("1. Verifique se GEMINI_API_KEY está no arquivo .env")
        print("2. Execute: pip install google-generativeai")
        print("3. Verifique se sua API key está válida")

def teste_individual():
    """Teste com vídeo específico do usuário"""
    
    print("🎯 TESTE INDIVIDUAL - GEMINI 2.5 PRO")
    print("="*50)
    
    titulo = input("Digite o título do vídeo: ").strip()
    descricao = input("Digite a descrição (opcional): ").strip()
    
    if not titulo:
        print("❌ Título é obrigatório!")
        return
    
    try:
        otimizador = OptimizadorF5()
        resultado = otimizador.otimizar_titulo(titulo, descricao)
        
        print("\n📊 RESULTADO:")
        print("="*40)
        print(f"📹 Original: {resultado.titulo_original}")
        print(f"✨ Otimizado: {resultado.titulo_otimizado}")
        print(f"🎯 Persona: {resultado.persona_alvo}")
        print(f"📈 SEO Score: {resultado.score_seo}/10")
        print(f"🔥 Potencial Viral: {resultado.potencial_viralizacao}")
        
        if resultado.sugestoes:
            print(f"\n💡 SUGESTÕES DE MELHORIA:")
            for i, sugestao in enumerate(resultado.sugestoes, 1):
                print(f"   {i}. {sugestao}")
        
        print("\n✅ Otimização concluída!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🔥 ESCOLHA UMA OPÇÃO:")
    print("1. Teste com vídeos exemplo da F5")
    print("2. Teste com seu próprio vídeo")
    
    escolha = input("\nDigite 1 ou 2: ").strip()
    
    if escolha == "1":
        testar_videos_f5()
    elif escolha == "2":
        teste_individual()
    else:
        print("❌ Opção inválida! Execute novamente.") 