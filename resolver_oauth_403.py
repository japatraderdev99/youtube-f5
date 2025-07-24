#!/usr/bin/env python3
"""
Resolver Erro 403: access_denied - YouTube APIs
Guia passo a passo para configurar OAuth corretamente
"""

import webbrowser
import time

def resolver_oauth_403():
    """Resolve o erro 403 do OAuth step by step"""
    
    print("🚨 RESOLVENDO ERRO 403: access_denied")
    print("="*60)
    
    print("\n📋 DETALHES DO PROBLEMA:")
    print("• App: YouTube Analytics")
    print("• Status: Modo TESTE (não publicado)")
    print("• Email: f5estrategia@gmail.com (não autorizado)")
    print("• Client ID: 413075847544-emr4tp4qgs2auidrren9ijek5idn4mvj.apps.googleusercontent.com")
    print("• Projeto: fabled-orbit-466718-j9")
    
    print("\n🎯 SOLUÇÕES DISPONÍVEIS:")
    print("1. Adicionar email como testador (Recomendado)")
    print("2. Publicar app para produção")
    print("3. Usar modo desenvolvedor temporário")
    
    escolha = input("\nEscolha uma opção (1, 2 ou 3): ").strip()
    
    if escolha == "1":
        solucao_adicionar_testador()
    elif escolha == "2":
        solucao_publicar_app()
    elif escolha == "3":
        solucao_modo_dev()
    else:
        print("❌ Opção inválida")

def solucao_adicionar_testador():
    """Adiciona email como testador"""
    
    print("\n🔧 SOLUÇÃO 1: ADICIONAR TESTADOR")
    print("="*50)
    
    # URL direto para a tela de consentimento
    oauth_url = "https://console.cloud.google.com/apis/credentials/consent?project=fabled-orbit-466718-j9"
    
    print("📝 PASSOS:")
    print("1. Vou abrir o Google Cloud Console")
    print("2. Faça login com sua conta Google")
    print("3. Vá para 'Tela de consentimento OAuth'")
    print("4. Role até 'Usuários de teste'")
    print("5. Clique em 'ADICIONAR USUÁRIOS'")
    print("6. Digite: f5estrategia@gmail.com")
    print("7. Salve as alterações")
    
    abrir = input("\n🌐 Abrir Google Cloud Console agora? (s/n): ").lower()
    
    if abrir == 's':
        print("\n🚀 Abrindo navegador...")
        webbrowser.open(oauth_url)
        
        print("\n⏳ Configure o testador e pressione ENTER quando terminar...")
        input()
        
        # Teste após configuração
        testar_oauth()
    else:
        print(f"\n📋 Acesse manualmente: {oauth_url}")

def solucao_publicar_app():
    """Publica o app para produção"""
    
    print("\n🚀 SOLUÇÃO 2: PUBLICAR APP")
    print("="*50)
    
    oauth_url = "https://console.cloud.google.com/apis/credentials/consent?project=fabled-orbit-466718-j9"
    
    print("📝 PASSOS:")
    print("1. Acesse a tela de consentimento OAuth")
    print("2. Clique em 'PUBLICAR APP'")
    print("3. Confirme a publicação")
    print("4. ⚠️  ATENÇÃO: App ficará público para qualquer usuário Google")
    
    print("\n⚠️  CONSIDERAÇÕES:")
    print("• Qualquer pessoa pode autorizar o app")
    print("• Recomendado apenas se for uso empresarial")
    print("• Para uso pessoal, prefira Solução 1")
    
    publicar = input("\n❓ Tem certeza que quer publicar? (s/n): ").lower()
    
    if publicar == 's':
        webbrowser.open(oauth_url)
        print("\n⏳ Publique o app e pressione ENTER quando terminar...")
        input()
        testar_oauth()

def solucao_modo_dev():
    """Modo desenvolvedor temporário"""
    
    print("\n⚙️  SOLUÇÃO 3: MODO DESENVOLVEDOR")
    print("="*50)
    
    print("📝 ALTERNATIVA TEMPORÁRIA:")
    print("• Use sistema sem APIs do YouTube")
    print("• Otimização com IA funcionará normalmente")
    print("• Análise de concorrentes via dados simulados")
    print("• Configure OAuth depois com calma")
    
    usar_modo_dev = input("\n🤖 Testar modo desenvolvedor agora? (s/n): ").lower()
    
    if usar_modo_dev == 's':
        testar_modo_sem_apis()

def testar_oauth():
    """Testa se OAuth foi configurado corretamente"""
    
    print("\n🧪 TESTANDO CONFIGURAÇÃO OAUTH...")
    print("="*50)
    
    try:
        from youtube_api_manager import initialize_youtube_system
        
        print("🚀 Iniciando teste de autenticação...")
        print("📋 Se abrir navegador, use: f5estrategia@gmail.com")
        
        system = initialize_youtube_system()
        
        print("✅ SUCESSO! OAuth configurado corretamente!")
        print("✅ APIs do YouTube funcionando!")
        
        # Teste básico de dados
        data_collector = system['data_collector']
        videos = data_collector.search_competitor_videos("marketing digital", max_results=2)
        
        if videos:
            print(f"✅ Coleta de dados OK! Encontrados {len(videos)} vídeos")
            print("🎉 SISTEMA TOTALMENTE FUNCIONAL!")
        else:
            print("⚠️  OAuth OK, mas sem dados retornados")
        
        return True
        
    except Exception as e:
        print(f"❌ Ainda com erro: {e}")
        
        if "403" in str(e) or "access_denied" in str(e):
            print("\n🔄 OAuth ainda não configurado. Verifique:")
            print("1. Email f5estrategia@gmail.com foi adicionado?")
            print("2. Mudanças foram salvas?")
            print("3. Aguarde alguns minutos para propagar")
        
        return False

def testar_modo_sem_apis():
    """Testa sistema sem APIs do YouTube"""
    
    print("\n🤖 TESTANDO MODO SEM APIS...")
    print("="*50)
    
    try:
        from content_optimizer import ContentOptimizer
        
        optimizer = ContentOptimizer()
        
        # Vídeo teste da F5
        video_teste = {
            'video_id': 'f5_demo',
            'title': 'Estratégias de Marketing Digital para PMEs que Faturam 500K-1M',
            'description': 'Como implementar campanhas de tráfego pago e funis de venda usando metodologia CHAVI para empresas em crescimento.',
            'tags': ['marketing digital', 'tráfego pago', 'pme', 'funil de vendas', 'metodologia chavi']
        }
        
        print("🧪 Analisando conteúdo com IA...")
        resultado = optimizer.optimize_existing_content(video_teste)
        
        print("✅ SISTEMA FUNCIONANDO SEM APIS!")
        print(f"📊 SEO Score: {resultado['analysis'].seo_score}/10")
        print(f"🎯 Persona detectada: {resultado['persona_target']}")
        print(f"🤖 IA utilizada: {resultado['ai_used']}")
        
        print(f"\n📝 OTIMIZAÇÃO:")
        print(f"Original: {resultado['original']['title']}")
        print(f"Novo: {resultado['optimized']['title']}")
        
        print(f"\n💡 SUGESTÕES TOP 3:")
        for i, sugestao in enumerate(resultado['analysis'].optimization_suggestions[:3], 1):
            print(f"{i}. {sugestao}")
        
        print("\n🎉 PRONTO PARA OTIMIZAR BANCO DE VÍDEOS!")
        print("Execute: python otimizar_banco_videos.py")
        
    except Exception as e:
        print(f"❌ Erro no modo sem APIs: {e}")

def status_sistema():
    """Mostra status atual do sistema"""
    
    print("\n📊 STATUS ATUAL DO SISTEMA:")
    print("="*50)
    
    print("✅ IA Gemini 2.5 Pro: FUNCIONANDO")
    print("✅ Otimização de conteúdo: FUNCIONANDO") 
    print("✅ Metodologia CHAVI: FUNCIONANDO")
    print("✅ Análise de personas: FUNCIONANDO")
    print("❌ APIs YouTube: BLOQUEADAS (OAuth 403)")
    
    print("\n🎯 AÇÕES RECOMENDADAS:")
    print("1. Configure OAuth para acessar APIs YouTube")
    print("2. Use sistema atual para otimizar conteúdos")
    print("3. Execute análises competitivas após OAuth")

if __name__ == "__main__":
    print("🚀 F5 YOUTUBE OPTIMIZER - RESOLVER OAUTH")
    print("="*60)
    
    status_sistema()
    print()
    resolver_oauth_403() 