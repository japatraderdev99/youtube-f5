#!/usr/bin/env python3
"""
Otimizador em Massa de Vídeos - F5 Estratégia
Processa banco de vídeos gravados para postagem otimizada
"""

import csv
import json
import os
from datetime import datetime, timedelta
from content_optimizer import create_content_optimizer

def processar_banco_videos(arquivo_csv='banco_videos_f5.csv'):
    """
    Processa banco de vídeos da F5 para otimização SEO
    
    Args:
        arquivo_csv: Arquivo com lista de vídeos (título, descrição, tags)
    """
    
    print("🚀 F5 ESTRATÉGIA - OTIMIZAÇÃO EM MASSA DE VÍDEOS")
    print("="*70)
    print("📌 Focado em: Marketing Digital, Tráfego Pago, Performance, CHAVI")
    print()
    
    # Inicializar otimizador
    try:
        optimizer = create_content_optimizer()
        print("✅ Sistema Gemini 2.5 Pro inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        return
    
    # Verificar se arquivo existe, senão criar exemplo
    if not os.path.exists(arquivo_csv):
        criar_exemplo_csv(arquivo_csv)
        print(f"📝 Arquivo exemplo criado: {arquivo_csv}")
        print("📋 Edite o arquivo com seus vídeos e execute novamente")
        return
    
    # Ler vídeos do CSV
    videos = []
    try:
        with open(arquivo_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            videos = list(reader)
        print(f"📁 {len(videos)} vídeos carregados do banco")
    except Exception as e:
        print(f"❌ Erro ao ler CSV: {e}")
        return
    
    # Processar cada vídeo
    resultados = []
    
    print("\n🤖 INICIANDO OTIMIZAÇÃO COM GEMINI 2.5 PRO...")
    print("="*70)
    
    for i, video in enumerate(videos, 1):
        print(f"\n📹 PROCESSANDO VÍDEO {i}/{len(videos)}:")
        print(f"Título: {video['titulo'][:60]}...")
        
        try:
            # Preparar dados do vídeo
            video_data = {
                'video_id': f'f5_video_{i:03d}',
                'title': video['titulo'],
                'description': video['descricao'],
                'tags': video['tags'].split(',') if video['tags'] else []
            }
            
            # Otimizar com IA
            resultado = optimizer.optimize_content(video_data)
            
            # Adicionar data sugerida de postagem
            data_postagem = datetime.now() + timedelta(days=i-1)
            
            resultado_completo = {
                'original': {
                    'titulo': video['titulo'],
                    'descricao': video['descricao'],
                    'tags': video['tags']
                },
                'otimizado': {
                    'titulo': resultado['optimized']['title'],
                    'descricao': resultado['optimized']['description'],
                    'tags': ', '.join(resultado['optimized']['tags']),
                    'persona_alvo': resultado['persona_target'],
                    'score_seo': resultado['analysis'].seo_score,
                    'melhoria_pontos': resultado['improvement_potential'],
                    'data_sugerida': data_postagem.strftime('%Y-%m-%d'),
                    'sugestoes': resultado['analysis'].optimization_suggestions[:5]
                }
            }
            
            resultados.append(resultado_completo)
            
            print(f"✅ Otimizado! Persona: {resultado['persona_target']}, SEO: {resultado['analysis'].seo_score}/10")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            continue
    
    # Salvar resultados
    salvar_resultados(resultados)
    
    # Mostrar estatísticas
    mostrar_estatisticas(resultados)
    
    # Gerar cronograma de postagem
    gerar_cronograma_postagem(resultados)

def criar_exemplo_csv(arquivo_csv):
    """Cria arquivo CSV de exemplo com vídeos típicos da F5"""
    
    videos_exemplo = [
        {
            'titulo': 'Como Criar Campanhas de Facebook Ads que Convertem 10x Mais',
            'descricao': 'Aprenda as estratégias secretas para criar campanhas de Facebook Ads altamente lucrativas. Metodologia CHAVI aplicada ao tráfego pago.',
            'tags': 'facebook ads,tráfego pago,conversão,marketing digital,ROI'
        },
        {
            'titulo': 'Gestão de Performance: Otimize suas Campanhas e Maximize o ROI',
            'descricao': 'Descubra como monitorar, analisar e otimizar suas campanhas de marketing digital para obter resultados excepcionais.',
            'tags': 'gestão de performance,otimização,ROI,campanhas,análise'
        },
        {
            'titulo': 'Metodologia CHAVI: O Sistema que Transformou Mais de 1000 Negócios',
            'descricao': 'Conheça nossa metodologia exclusiva CHAVI e como ela pode revolucionar seus resultados em vendas e marketing.',
            'tags': 'metodologia CHAVI,vendas,marketing,sistema,negócios'
        },
        {
            'titulo': 'Google Ads vs Facebook Ads: Qual Plataforma Escolher em 2024',
            'descricao': 'Análise completa das duas principais plataformas de tráfego pago. Quando usar cada uma para maximizar resultados.',
            'tags': 'google ads,facebook ads,tráfego pago,comparação,2024'
        },
        {
            'titulo': 'Como Escalar Campanhas de Tráfego sem Perder a Lucratividade',
            'descricao': 'Estratégias avançadas para escalar suas campanhas mantendo ou melhorando o ROI. Casos reais da F5 Estratégia.',
            'tags': 'escalar campanhas,lucratividade,ROI,estratégias,casos reais'
        }
    ]
    
    with open(arquivo_csv, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['titulo', 'descricao', 'tags']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(videos_exemplo)

def salvar_resultados(resultados):
    """Salva resultados da otimização"""
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_saida = f'videos_otimizados_f5_{timestamp}.json'
    
    with open(arquivo_saida, 'w', encoding='utf-8') as file:
        json.dump(resultados, file, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Resultados salvos em: {arquivo_saida}")

def mostrar_estatisticas(resultados):
    """Mostra estatísticas da otimização"""
    
    if not resultados:
        return
    
    scores_seo = [r['otimizado']['score_seo'] for r in resultados]
    melhorias = [r['otimizado']['melhoria_pontos'] for r in resultados]
    personas = [r['otimizado']['persona_alvo'] for r in resultados]
    
    print("\n📊 ESTATÍSTICAS DA OTIMIZAÇÃO:")
    print("="*50)
    print(f"📹 Total de vídeos processados: {len(resultados)}")
    print(f"📈 Score SEO médio: {sum(scores_seo)/len(scores_seo):.1f}/10")
    print(f"🚀 Melhoria média: +{sum(melhorias)/len(melhorias):.1f} pontos")
    print(f"🎯 Personas distribuição:")
    
    for persona in set(personas):
        count = personas.count(persona)
        print(f"   • {persona}: {count} vídeos ({count/len(personas)*100:.1f}%)")

def gerar_cronograma_postagem(resultados):
    """Gera cronograma otimizado de postagem"""
    
    print("\n📅 CRONOGRAMA DE POSTAGEM SUGERIDO:")
    print("="*60)
    print("📌 Baseado em: SEO, Personas, Trending Topics")
    print()
    
    for i, resultado in enumerate(resultados):
        data = resultado['otimizado']['data_sugerida']
        titulo = resultado['otimizado']['titulo'][:50]
        persona = resultado['otimizado']['persona_alvo']
        score = resultado['otimizado']['score_seo']
        
        # Definir melhor horário por persona
        horarios = {
            'estrategico': '14:00',  # Empresários - tarde
            'crescimento': '19:00',   # PMEs - noite
            'smart': '20:00'         # Pequenos - noite
        }
        
        horario = horarios.get(persona.lower(), '19:00')
        
        print(f"📅 {data} às {horario} - [{persona.upper()}] SEO:{score}/10")
        print(f"   🎬 {titulo}...")
        print()

def processar_video_individual(titulo, descricao, tags):
    """Processa um vídeo individual para teste rápido"""
    
    print("🎯 TESTE RÁPIDO - OTIMIZAÇÃO INDIVIDUAL")
    print("="*50)
    
    try:
        optimizer = create_content_optimizer()
        
        video_data = {
            'video_id': 'teste_individual',
            'title': titulo,
            'description': descricao,
            'tags': tags.split(',') if isinstance(tags, str) else tags
        }
        
        resultado = optimizer.optimize_content(video_data)
        
        print(f"📹 ORIGINAL:")
        print(f"   Título: {titulo}")
        print(f"   Tags: {tags}")
        print()
        
        print(f"✨ OTIMIZADO:")
        print(f"   Título: {resultado['optimized']['title']}")
        print(f"   Persona: {resultado['persona_target']}")
        print(f"   Score SEO: {resultado['analysis'].seo_score}/10")
        print(f"   Melhoria: +{resultado['improvement_potential']} pontos")
        print()
        
        print(f"💡 TOP 3 SUGESTÕES:")
        for i, sugestao in enumerate(resultado['analysis'].optimization_suggestions[:3], 1):
            print(f"   {i}. {sugestao}")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    print("🔥 ESCOLHA UMA OPÇÃO:")
    print("1. Processar banco completo de vídeos")
    print("2. Teste rápido com vídeo individual")
    
    escolha = input("\nDigite 1 ou 2: ").strip()
    
    if escolha == "1":
        processar_banco_videos()
    elif escolha == "2":
        titulo = input("Título do vídeo: ")
        descricao = input("Descrição: ")
        tags = input("Tags (separadas por vírgula): ")
        processar_video_individual(titulo, descricao, tags)
    else:
        print("Opção inválida!") 