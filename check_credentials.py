#!/usr/bin/env python3
"""
Script de Verificação de Credenciais - F5 YouTube Optimizer
Verifica se todas as credenciais necessárias estão configuradas
"""

import os
import json
import sys
from pathlib import Path

def print_header():
    """Cabeçalho do script"""
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DE CREDENCIAIS - F5 YOUTUBE OPTIMIZER")
    print("=" * 70)

def check_oauth_credentials():
    """Verifica credenciais OAuth"""
    print("\n🔑 VERIFICANDO CREDENCIAIS OAUTH...")
    
    client_secret_file = "client_secret.json"
    
    if os.path.exists(client_secret_file):
        try:
            with open(client_secret_file, 'r') as f:
                credentials = json.load(f)
            
            # Extrair informações
            installed = credentials.get('installed', {})
            client_id = installed.get('client_id', '')
            project_id = installed.get('project_id', '')
            client_secret = installed.get('client_secret', '')
            
            print("✅ Arquivo client_secret.json encontrado")
            print(f"   📋 Project ID: {project_id}")
            print(f"   🔐 Client ID: {client_id[:20]}...")
            print(f"   🗝️  Client Secret: {client_secret[:15]}...")
            
            return True, project_id, client_id
            
        except Exception as e:
            print(f"❌ Erro ao ler client_secret.json: {e}")
            return False, None, None
    else:
        print("❌ Arquivo client_secret.json não encontrado")
        return False, None, None

def check_env_file():
    """Verifica arquivo .env"""
    print("\n📄 VERIFICANDO ARQUIVO .env...")
    
    env_files = ['.env', 'credentials_configured.env']
    env_found = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"✅ Encontrado: {env_file}")
            env_found = True
            
            # Verificar conteúdo
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                
                # Verificar variáveis importantes
                vars_to_check = {
                    'YOUTUBE_API_KEY': 'API Key do YouTube',
                    'F5_CHANNEL_ID': 'ID do Canal F5',
                    'GEMINI_API_KEY': 'Gemini API Key (IA Principal)'
                }
                
                print(f"\n   📝 Verificando variáveis em {env_file}:")
                for var_name, description in vars_to_check.items():
                    if f"{var_name}=" in content:
                        # Extrair valor
                        for line in content.split('\n'):
                            if line.startswith(f"{var_name}="):
                                value = line.split('=', 1)[1].strip()
                                if value and not value.startswith('SUA_') and not value.startswith('sk-ant-sua_'):
                                    print(f"   ✅ {description}: Configurado")
                                else:
                                    print(f"   ❌ {description}: NECESSÁRIO CONFIGURAR")
                                break
                    else:
                        print(f"   ❌ {description}: Variável não encontrada")
                
            except Exception as e:
                print(f"   ❌ Erro ao ler {env_file}: {e}")
    
    if not env_found:
        print("❌ Nenhum arquivo .env encontrado")
        print("   Renomeie 'credentials_configured.env' para '.env'")
    
    return env_found

def check_apis_status(project_id):
    """Verifica status das APIs (informativo)"""
    print(f"\n🌐 STATUS DAS APIS (Projeto: {project_id})...")
    
    api_console_url = f"https://console.cloud.google.com/apis/dashboard?project={project_id}"
    credentials_url = f"https://console.cloud.google.com/apis/credentials?project={project_id}"
    
    print("Para verificar se as APIs estão habilitadas:")
    print(f"   🔗 Dashboard APIs: {api_console_url}")
    print(f"   🔗 Credenciais: {credentials_url}")
    
    required_apis = [
        "YouTube Data API v3",
        "YouTube Analytics API", 
        "YouTube Reporting API"
    ]
    
    print("\n   📋 APIs necessárias:")
    for api in required_apis:
        print(f"   • {api}")

def get_next_steps():
    """Retorna próximos passos"""
    return """
🎯 PRÓXIMOS PASSOS:

1️⃣  CONFIGURAR API KEY:
   • Acesse: https://console.cloud.google.com/apis/credentials?project=fabled-orbit-466718-j9
   • Clique em "CRIAR CREDENCIAIS" > "Chave de API"
   • Restrinja para as APIs do YouTube
   • Copie a chave para o arquivo .env

2️⃣  OBTER ID DO CANAL F5:
   • Use: https://commentpicker.com/youtube-channel-id.php
   • Cole a URL do canal da F5
   • Copie o ID (UC...) para o arquivo .env

3️⃣  CONFIGURAR CLAUDE (IA):
   • Acesse: https://console.anthropic.com/
   • Crie API Key
   • Copie a chave (sk-ant-...) para o arquivo .env

4️⃣  TESTAR SISTEMA:
   • Execute: python main.py
   • Ou: python main.py --mode suggestions
"""

def main():
    """Função principal"""
    print_header()
    
    # Verificar credenciais OAuth
    oauth_ok, project_id, client_id = check_oauth_credentials()
    
    # Verificar arquivo .env
    env_ok = check_env_file()
    
    # Verificar APIs se temos project_id
    if project_id:
        check_apis_status(project_id)
    
    # Status geral
    print("\n" + "="*70)
    print("📊 RESUMO DA CONFIGURAÇÃO:")
    print("="*70)
    
    print(f"🔑 Credenciais OAuth: {'✅' if oauth_ok else '❌'}")
    print(f"📄 Arquivo .env: {'✅' if env_ok else '❌'}")
    print(f"🌐 Projeto Google Cloud: {'✅' if project_id else '❌'}")
    
    if oauth_ok and env_ok:
        print("\n🎉 Configuração base OK!")
        print("Finalize configurando as 3 variáveis no arquivo .env")
    else:
        print("\n⚠️  Configuração incompleta")
    
    # Próximos passos
    print(get_next_steps())

if __name__ == "__main__":
    main() 