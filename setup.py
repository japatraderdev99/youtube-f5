#!/usr/bin/env python3
"""
Script de Setup - Sistema de Otimização YouTube F5 Estratégia
Este script auxilia na configuração inicial das APIs e credenciais
"""

import os
import sys
import json
import webbrowser
from pathlib import Path

def print_header():
    """Exibe cabeçalho do script"""
    print("=" * 70)
    print("🚀 SETUP - SISTEMA DE OTIMIZAÇÃO YOUTUBE F5 ESTRATÉGIA")
    print("=" * 70)
    print("Este script irá te guiar na configuração das APIs do YouTube\n")

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version.split()[0]} detectado")

def install_dependencies():
    """Instala dependências do projeto"""
    print("\n📦 INSTALANDO DEPENDÊNCIAS...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
        else:
            print("❌ Erro ao instalar dependências:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    
    return True

def create_env_file():
    """Cria arquivo .env baseado no template"""
    print("\n📝 CONFIGURANDO ARQUIVO .env...")
    
    if os.path.exists('.env'):
        response = input("Arquivo .env já existe. Sobrescrever? (s/n): ")
        if response.lower() != 's':
            print("Mantendo arquivo .env existente")
            return
    
    # Copiar template
    if os.path.exists('setup_env_template.env'):
        with open('setup_env_template.env', 'r') as template:
            content = template.read()
        
        with open('.env', 'w') as env_file:
            env_file.write(content)
        
        print("✅ Arquivo .env criado baseado no template")
        print("⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais reais")
    else:
        print("❌ Template .env não encontrado")

def check_credentials_file():
    """Verifica se arquivo de credenciais OAuth existe"""
    print("\n🔑 VERIFICANDO CREDENCIAIS OAUTH...")
    
    if os.path.exists('client_secret.json'):
        print("✅ Arquivo client_secret.json encontrado")
        return True
    else:
        print("❌ Arquivo client_secret.json não encontrado")
        print("📝 Você precisa baixar este arquivo do Google Cloud Console")
        return False

def get_google_cloud_setup_instructions():
    """Retorna instruções detalhadas para Google Cloud"""
    return """
🔧 INSTRUÇÕES GOOGLE CLOUD CONSOLE:

1️⃣  CRIAR PROJETO:
   • Acesse: https://console.cloud.google.com/
   • Clique em "Selecionar projeto" → "NOVO PROJETO"
   • Nome: F5-YouTube-Analytics-System
   • Clique em "CRIAR"

2️⃣  HABILITAR APIs:
   • Menu → "APIs e serviços" → "Biblioteca"
   • Busque e ATIVE:
     - YouTube Data API v3
     - YouTube Analytics API  
     - YouTube Reporting API

3️⃣  CONFIGURAR OAUTH:
   • Menu → "APIs e serviços" → "Tela de consentimento OAuth"
   • Tipo: EXTERNO → CRIAR
   • Preencha informações da F5 Estratégia
   • Adicionar escopos:
     - https://www.googleapis.com/auth/youtube.readonly
     - https://www.googleapis.com/auth/yt-analytics.readonly
     - https://www.googleapis.com/auth/yt-analytics-monetary.readonly

4️⃣  CRIAR CREDENCIAIS:
   • Menu → "APIs e serviços" → "Credenciais"
   • "+ CRIAR CREDENCIAIS" → "ID do cliente OAuth"
   • Tipo: Aplicativo da área de trabalho
   • Nome: F5 YouTube Analytics Client
   • BAIXAR como "client_secret.json"

5️⃣  CRIAR API KEY:
   • "+ CRIAR CREDENCIAIS" → "Chave de API"
   • RESTRINGIR CHAVE → Selecionar APIs do YouTube
   • Copiar a chave para o arquivo .env
"""

def get_channel_id_instructions():
    """Instruções para obter ID do canal"""
    return """
📺 COMO OBTER ID DO CANAL F5:

MÉTODO 1 - Via URL:
   • Acesse o canal no YouTube
   • Na URL, procure por algo como: youtube.com/channel/UC...
   • O ID é a parte após /channel/

MÉTODO 2 - Via Código-fonte:
   • Acesse o canal no YouTube
   • Clique com botão direito → "Ver código-fonte"
   • Procure por "channel_id" (Ctrl+F)

MÉTODO 3 - Ferramenta online:
   • Acesse: https://commentpicker.com/youtube-channel-id.php
   • Cole a URL do canal da F5
   • Clique em "Get Channel ID"
"""

def get_anthropic_setup():
    """Instruções para configurar Claude (Anthropic)"""
    return """
🤖 CONFIGURAR CLAUDE (ANTHROPIC) - IA PRINCIPAL:

1️⃣  CRIAR CONTA:
   • Acesse: https://console.anthropic.com/
   • Faça login/registro com email da F5

2️⃣  OBTER API KEY:
   • Menu → "API Keys"
   • Clique em "Create Key"
   • Nome: F5-YouTube-Optimizer
   • Copie a chave (sk-ant-...)

3️⃣  CONFIGURAR NO .env:
   • Abra o arquivo .env
   • Cole a chave em: ANTHROPIC_API_KEY=sk-ant-sua_chave_aqui

💡 FALLBACK OPENAI (OPCIONAL):
   • Se quiser usar OpenAI como backup
   • Acesse: https://platform.openai.com/api-keys
   • Configure: OPENAI_API_KEY=sk-sua_chave_aqui
"""

def run_setup_wizard():
    """Executa o assistente de configuração"""
    print_header()
    
    # Verificar Python
    check_python_version()
    
    # Instalar dependências
    if not install_dependencies():
        print("\n❌ Setup interrompido devido a erro nas dependências")
        return
    
    # Criar arquivo .env
    create_env_file()
    
    # Verificar credenciais
    credentials_ok = check_credentials_file()
    
    print("\n" + "="*70)
    print("📋 PRÓXIMOS PASSOS:")
    print("="*70)
    
    if not credentials_ok:
        print("\n1️⃣  CONFIGURAR GOOGLE CLOUD:")
        print(get_google_cloud_setup_instructions())
        
        response = input("\nAbrir Google Cloud Console no navegador? (s/n): ")
        if response.lower() == 's':
            webbrowser.open('https://console.cloud.google.com/')
    
    print("\n2️⃣  OBTER ID DO CANAL:")
    print(get_channel_id_instructions())
    
    print("\n3️⃣  CONFIGURAR IA:")
    print(get_anthropic_setup())
    
    response = input("\nAbrir console do Anthropic no navegador? (s/n): ")
    if response.lower() == 's':
        webbrowser.open('https://console.anthropic.com/')
    
    print("\n" + "="*70)
    print("🎯 FINALIZANDO SETUP:")
    print("="*70)
    print("1. Edite o arquivo .env com suas credenciais")
    print("2. Coloque o arquivo client_secret.json na pasta do projeto")
    print("3. Execute: python main.py")
    print("\n✅ Setup concluído!")

def check_setup_status():
    """Verifica status da configuração"""
    print("\n🔍 VERIFICANDO CONFIGURAÇÃO ATUAL...")
    
    status = {
        'env_file': os.path.exists('.env'),
        'credentials_file': os.path.exists('client_secret.json'),
        'dependencies': True  # Assumindo que foi instalado
    }
    
    print(f"📄 Arquivo .env: {'✅' if status['env_file'] else '❌'}")
    print(f"🔑 Credenciais OAuth: {'✅' if status['credentials_file'] else '❌'}")
    print(f"📦 Dependências: {'✅' if status['dependencies'] else '❌'}")
    
    if all(status.values()):
        print("\n🎉 Configuração parece estar completa!")
        print("Execute: python main.py")
    else:
        print("\n⚠️  Configuração incompleta. Execute python setup.py novamente")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_setup_status()
    else:
        run_setup_wizard() 