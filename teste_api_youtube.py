#!/usr/bin/env python3
"""
Teste Rápido - API YouTube OAuth
Verifica se a autenticação está funcionando
"""

def teste_oauth_youtube():
    """Testa apenas a autenticação OAuth"""
    print("🔐 TESTE DE AUTENTICAÇÃO YOUTUBE")
    print("="*50)
    
    try:
        from youtube_api_manager import initialize_youtube_system
        
        print("🚀 Iniciando autenticação...")
        print("📋 Se abrir o navegador, faça login com: f5estrategia@gmail.com")
        print("⏳ Aguardando autorização...")
        
        system = initialize_youtube_system()
        
        print("✅ AUTENTICAÇÃO FUNCIONANDO!")
        print("✅ APIs do YouTube conectadas!")
        print("✅ Sistema pronto para coletar dados!")
        
        # Teste básico de coleta
        data_collector = system['data_collector']
        print("\n🧪 Testando coleta de dados...")
        
        # Teste simples - buscar vídeos sobre marketing digital
        videos = data_collector.search_competitor_videos("marketing digital", max_results=3)
        
        if videos:
            print(f"✅ Coleta funcionando! Encontrados {len(videos)} vídeos")
            print("📹 Exemplo:", videos[0]['title'][:50] + "...")
        else:
            print("⚠️  Autenticação OK, mas sem dados retornados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        
        if "403" in str(e) or "access_denied" in str(e):
            print("\n🔧 SOLUÇÃO:")
            print("1. Acesse: https://console.cloud.google.com/apis/credentials/consent?project=fabled-orbit-466718-j9")
            print("2. Adicione f5estrategia@gmail.com como testador")
            print("3. Execute este teste novamente")
        
        return False

if __name__ == "__main__":
    teste_oauth_youtube() 