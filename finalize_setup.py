#!/usr/bin/env python3
"""
Script de Finalização - F5 YouTube Optimizer
Ajuda a configurar as últimas 3 variáveis necessárias
"""

import os
import webbrowser

def print_header():
    print("=" * 70)
    print("🎯 FINALIZAÇÃO DA CONFIGURAÇÃO - F5 YOUTUBE OPTIMIZER")
    print("=" * 70)
    print("Vamos configurar as 3 últimas variáveis necessárias!\n")

def collect_credentials():
    """Coleta as credenciais do usuário"""
    credentials = {}
    
    print("📝 VAMOS COLETAR AS 3 CREDENCIAIS NECESSÁRIAS:")
    print()
    
    # 1. API Key do YouTube
    print("1️⃣  API KEY DO YOUTUBE:")
    print("   • Se ainda não criou, digite 'abrir' para abrir o Google Cloud Console")
    api_key = input("   • Cole sua API Key aqui: ").strip()
    
    if api_key.lower() == 'abrir':
        webbrowser.open('https://console.cloud.google.com/apis/credentials?project=fabled-orbit-466718-j9')
        api_key = input("   • Após criar, cole a API Key aqui: ").strip()
    
    credentials['YOUTUBE_API_KEY'] = api_key
    
    # 2. Channel ID
    print("\n2️⃣  ID DO CANAL F5:")
    print("   • Se não souber o ID, digite 'abrir' para usar a ferramenta online")
    channel_id = input("   • Cole o Channel ID (UC...): ").strip()
    
    if channel_id.lower() == 'abrir':
        webbrowser.open('https://commentpicker.com/youtube-channel-id.php')
        channel_id = input("   • Após obter, cole o Channel ID aqui: ").strip()
    
    credentials['F5_CHANNEL_ID'] = channel_id
    
    # 3. Claude API Key
    print("\n3️⃣  CLAUDE API KEY:")
    print("   • Se ainda não criou, digite 'abrir' para abrir o console da Anthropic")
    claude_key = input("   • Cole sua Claude API Key (sk-ant-...): ").strip()
    
    if claude_key.lower() == 'abrir':
        webbrowser.open('https://console.anthropic.com/')
        claude_key = input("   • Após criar, cole a Claude API Key aqui: ").strip()
    
    credentials['ANTHROPIC_API_KEY'] = claude_key
    
    return credentials

def create_final_env_file(credentials):
    """Cria arquivo .env final"""
    env_content = f"""# ========================================
# F5 YOUTUBE OPTIMIZER - CONFIGURAÇÃO COMPLETA
# ========================================

# APIS DO YOUTUBE - CONFIGURADAS ✅
YOUTUBE_API_KEY={credentials['YOUTUBE_API_KEY']}
F5_CHANNEL_ID={credentials['F5_CHANNEL_ID']}

# CREDENCIAIS OAUTH - CONFIGURADAS ✅
YOUTUBE_CLIENT_SECRETS_FILE=client_secret.json

# GOOGLE CLOUD - CONFIGURADO ✅
GOOGLE_CLOUD_PROJECT=fabled-orbit-466718-j9

# IA PRINCIPAL - CONFIGURADA ✅
ANTHROPIC_API_KEY={credentials['ANTHROPIC_API_KEY']}

# IA FALLBACK (OPCIONAL)
OPENAI_API_KEY=sk-sua_openai_key_aqui

# CONFIGURAÇÕES PADRÃO
ENVIRONMENT=development
DEBUG=True
DATA_COLLECTION_INTERVAL=3600
MAX_VIDEOS_PER_REQUEST=50
API_RATE_LIMIT=100
DATABASE_URL=sqlite:///f5_youtube_optimizer.db
DATABASE_ECHO=False

# STATUS: CONFIGURAÇÃO COMPLETA ✅
"""
    
    # Salvar arquivo .env
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Arquivo .env criado com sucesso!")

def validate_credentials(credentials):
    """Valida formato das credenciais"""
    errors = []
    
    # Validar API Key (deve ter pelo menos 30 caracteres)
    if len(credentials['YOUTUBE_API_KEY']) < 30:
        errors.append("API Key do YouTube parece inválida (muito curta)")
    
    # Validar Channel ID (deve começar com UC)
    if not credentials['F5_CHANNEL_ID'].startswith('UC'):
        errors.append("Channel ID deve começar com 'UC'")
    
    # Validar Claude Key (deve começar com sk-ant-)
    if not credentials['ANTHROPIC_API_KEY'].startswith('sk-ant-'):
        errors.append("Claude API Key deve começar com 'sk-ant-'")
    
    if errors:
        print("\n⚠️  AVISOS:")
        for error in errors:
            print(f"   • {error}")
        
        confirm = input("\nContinuar mesmo assim? (s/n): ")
        return confirm.lower() == 's'
    
    return True

def test_system():
    """Testa o sistema"""
    print("\n🧪 TESTANDO SISTEMA...")
    
    try:
        # Testar importação básica
        from config import validate_config
        validate_config()
        print("✅ Configuração válida!")
        
        print("\n🚀 SISTEMA PRONTO!")
        print("Execute um dos comandos:")
        print("   python main.py                          # Dashboard")
        print("   python main.py --mode suggestions       # Sugestões de conteúdo")
        print("   python main.py --mode analysis          # Análise completa")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        print("Verifique as credenciais e tente novamente")

def main():
    """Função principal"""
    print_header()
    
    # Verificar se já temos .env
    if os.path.exists('.env'):
        response = input("Arquivo .env já existe. Recriar? (s/n): ")
        if response.lower() != 's':
            print("Mantendo configuração existente.")
            return
    
    # Coletar credenciais
    credentials = collect_credentials()
    
    # Validar
    if not validate_credentials(credentials):
        print("Configuração cancelada.")
        return
    
    # Criar arquivo .env
    create_final_env_file(credentials)
    
    # Testar sistema
    test_system()
    
    print("\n🎉 CONFIGURAÇÃO FINALIZADA!")
    print("=" * 70)

if __name__ == "__main__":
    main() 