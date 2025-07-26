"""
Gerador de Arquivos Específicos para Upload no YouTube - F5 Estratégia
Cria arquivos .txt separados para cada campo necessário na interface do YouTube
"""

import os
import json
from pathlib import Path
from advanced_seo_generator import generate_complete_seo_package

def generate_youtube_upload_files(transcription_file: str) -> dict:
    """
    Gera arquivos .txt separados para upload no YouTube
    
    Args:
        transcription_file (str): Caminho para o arquivo de transcrição
    
    Returns:
        dict: Resultado da operação com caminhos dos arquivos criados
    """
    
    try:
        # Gera a otimização SEO completa
        print("🔄 Analisando transcrição e gerando conteúdo SEO...")
        seo_result = generate_complete_seo_package(transcription_file)
        
        if 'error' in seo_result:
            return {'error': seo_result['error']}
        
        # Diretório do vídeo (mesma pasta da transcrição)
        video_dir = os.path.dirname(transcription_file)
        
        # Dados do SEO
        titulo = seo_result['seo_content']['title']['primary']
        descricao = seo_result['seo_content']['description']['content']
        tags_list = seo_result['seo_content']['tags']['content']
        keywords = seo_result['keywords']['primary']
        
        # 1. ARQUIVO DE TÍTULO
        titulo_file = os.path.join(video_dir, 'titulo.txt')
        with open(titulo_file, 'w', encoding='utf-8') as f:
            f.write(titulo)
        
        # 2. ARQUIVO DE DESCRIÇÃO
        descricao_file = os.path.join(video_dir, 'descricao.txt')
        with open(descricao_file, 'w', encoding='utf-8') as f:
            f.write(descricao)
        
        # 3. ARQUIVO DE TAGS (separadas por vírgula para YouTube)
        # YouTube aceita tags separadas por vírgula
        tags_youtube = ', '.join(tags_list)
        
        # Verifica limite de caracteres do YouTube (500 caracteres para tags)
        if len(tags_youtube) > 500:
            # Reduz tags para caber no limite
            tags_reduced = []
            current_length = 0
            for tag in tags_list:
                if current_length + len(tag) + 2 <= 500:  # +2 para vírgula e espaço
                    tags_reduced.append(tag)
                    current_length += len(tag) + 2
                else:
                    break
            tags_youtube = ', '.join(tags_reduced)
        
        tags_file = os.path.join(video_dir, 'tags.txt')
        with open(tags_file, 'w', encoding='utf-8') as f:
            f.write(tags_youtube)
        
        # 4. ARQUIVO DE METADADOS (palavras-chave separadas por traços para arquivos)
        # Pega as top palavras-chave e junta com traços
        top_keywords = [kw[0] for kw in keywords[:8]]  # Top 8 palavras-chave
        metadados_keywords = '-'.join(top_keywords).replace(' ', '-')
        
        metadados_file = os.path.join(video_dir, 'metadados.txt')
        with open(metadados_file, 'w', encoding='utf-8') as f:
            f.write(metadados_keywords)
        
        # 5. ARQUIVO DE RESUMO (para referência)
        resumo_data = {
            'video_info': {
                'titulo_caracteres': len(titulo),
                'descricao_caracteres': len(descricao),
                'tags_count': len(tags_list),
                'tags_caracteres': len(tags_youtube),
                'tema_detectado': seo_result.get('video_info', {}).get('detected_theme', 'N/A'),
                'data_criacao': seo_result.get('video_info', {}).get('optimization_date', 'N/A')
            },
            'arquivos_criados': {
                'titulo': 'titulo.txt',
                'descricao': 'descricao.txt', 
                'tags': 'tags.txt',
                'metadados': 'metadados.txt'
            },
            'recomendacoes': seo_result.get('recommendations', [])
        }
        
        resumo_file = os.path.join(video_dir, 'resumo_upload.json')
        with open(resumo_file, 'w', encoding='utf-8') as f:
            json.dump(resumo_data, f, ensure_ascii=False, indent=2)
        
        # Resultado da operação
        result = {
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
                'titulo': titulo,
                'titulo_chars': len(titulo),
                'descricao_chars': len(descricao),
                'tags_count': len(tags_list),
                'tags_chars': len(tags_youtube),
                'keywords': metadados_keywords,
                'tema': seo_result.get('video_info', {}).get('detected_theme', 'N/A')
            }
        }
        
        return result
        
    except Exception as e:
        return {'error': str(e)}

def process_video_directory(video_directory: str) -> dict:
    """
    Processa todos os vídeos em um diretório
    
    Args:
        video_directory (str): Diretório contendo pastas de vídeos
    
    Returns:
        dict: Resultado do processamento
    """
    results = {}
    
    # Busca pastas de vídeo
    for item in os.listdir(video_directory):
        item_path = os.path.join(video_directory, item)
        if os.path.isdir(item_path):
            # Busca arquivos .txt (transcrições) na pasta
            txt_files = [f for f in os.listdir(item_path) if f.endswith('.txt')]
            
            for txt_file in txt_files:
                transcription_path = os.path.join(item_path, txt_file)
                print(f"\n📁 Processando: {item}/{txt_file}")
                
                result = generate_youtube_upload_files(transcription_path)
                results[f"{item}/{txt_file}"] = result
    
    return results

if __name__ == "__main__":
    # Processa o vídeo específico
    transcription_path = "Transcricoes de Videos/Video 1/f5-youtube-video1-Autorresponsabilidade_01mp4.txt"
    
    if os.path.exists(transcription_path):
        print("🚀 GERANDO ARQUIVOS PARA UPLOAD NO YOUTUBE...")
        
        result = generate_youtube_upload_files(transcription_path)
        
        if result.get('success'):
            print("\n✅ ARQUIVOS CRIADOS COM SUCESSO!")
            print(f"📁 Diretório: {result['video_directory']}")
            
            print(f"\n📝 TÍTULO ({result['content_summary']['titulo_chars']} caracteres):")
            print(f"   └── {result['content_summary']['titulo']}")
            
            print(f"\n📄 DESCRIÇÃO ({result['content_summary']['descricao_chars']} caracteres):")
            print(f"   └── arquivo: descricao.txt")
            
            print(f"\n🏷️ TAGS ({result['content_summary']['tags_count']} tags, {result['content_summary']['tags_chars']} caracteres):")
            print(f"   └── arquivo: tags.txt")
            
            print(f"\n🔗 METADADOS PARA ARQUIVOS:")
            print(f"   └── {result['content_summary']['keywords']}")
            print(f"   └── arquivo: metadados.txt")
            
            print(f"\n🎯 TEMA DETECTADO: {result['content_summary']['tema']}")
            
            print(f"\n📋 ARQUIVOS CRIADOS:")
            for tipo, caminho in result['files_created'].items():
                print(f"   ✓ {tipo}.txt")
            
            print(f"\n🔄 PRÓXIMOS PASSOS:")
            print(f"1. Abra a pasta: {result['video_directory']}")
            print(f"2. Use titulo.txt no campo título do YouTube")
            print(f"3. Use descricao.txt no campo descrição do YouTube") 
            print(f"4. Use tags.txt no campo tags do YouTube")
            print(f"5. Use metadados.txt nos nomes dos arquivos de vídeo/thumb")
            
        else:
            print(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
    else:
        print(f"❌ Arquivo não encontrado: {transcription_path}")
        
        # Processa todos os vídeos se arquivo específico não existir
        transcriptions_dir = "Transcricoes de Videos"
        if os.path.exists(transcriptions_dir):
            print(f"\n🔄 Processando todos os vídeos em: {transcriptions_dir}")
            results = process_video_directory(transcriptions_dir)
            
            success_count = len([r for r in results.values() if r.get('success')])
            total_count = len(results)
            
            print(f"\n📊 RESULTADO FINAL:")
            print(f"   ✅ Processados com sucesso: {success_count}/{total_count}")
            
            for video, result in results.items():
                if result.get('success'):
                    print(f"   ✓ {video}")
                else:
                    print(f"   ✗ {video}: {result.get('error', 'Erro')}") 