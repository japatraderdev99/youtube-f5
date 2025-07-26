#!/usr/bin/env python3
"""
🚀 F5 Estratégia - Dashboard Launcher
Inicialização automática do dashboard moderno com verificação de dependências

Execute este arquivo para iniciar o sistema completo.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Exibe banner de inicialização"""
    banner = """
    ███████╗███████╗    ███████╗███████╗████████╗██████╗  █████╗ ████████╗███████╗ ██████╗ ██╗ █████╗ 
    ██╔════╝██╔════╝    ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝ ██║██╔══██╗
    █████╗  ███████╗    █████╗  ███████╗   ██║   ██████╔╝███████║   ██║   █████╗  ██║  ███╗██║███████║
    ██╔══╝  ╚════██║    ██╔══╝  ╚════██║   ██║   ██╔══██╗██╔══██║   ██║   ██╔══╝  ██║   ██║██║██╔══██║
    ██║     ███████║    ███████╗███████║   ██║   ██║  ██║██║  ██║   ██║   ███████╗╚██████╔╝██║██║  ██║
    ╚═╝     ╚══════╝    ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═╝
    
    🎯 Dashboard Avançado para Otimização de Conteúdo YouTube
    📊 Sistema de Análise com IA e UX Moderno
    """
    print(banner)
    print("=" * 100)

def check_python_version():
    """Verifica versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")

def install_package(package):
    """Instala um pacote específico"""
    try:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--quiet"
        ])
        print(f"✅ {package} instalado")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")
        return False

def check_and_install_dependencies():
    """Verifica e instala dependências necessárias"""
    print("\n🔍 Verificando dependências...")
    
    required_packages = {
        'streamlit': 'streamlit>=1.28.0',
        'plotly': 'plotly>=5.17.0',
        'pandas': 'pandas>=2.0.0',
        'numpy': 'numpy>=1.24.0'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - não encontrado")
            missing_packages.append(pip_name)
    
    if missing_packages:
        print(f"\n🔧 Instalando {len(missing_packages)} dependências...")
        for package in missing_packages:
            install_package(package)
        print("✅ Todas as dependências foram instaladas!")
    else:
        print("✅ Todas as dependências já estão instaladas!")

def check_files():
    """Verifica se os arquivos necessários existem"""
    print("\n📁 Verificando arquivos do sistema...")
    
    required_files = [
        'modern_dashboard.py',
        'config.py',
        'content_optimizer.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - não encontrado")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ Arquivos faltantes: {', '.join(missing_files)}")
        print("   Certifique-se de que todos os arquivos do sistema estão no diretório")
        return False
    
    return True

def start_dashboard():
    """Inicia o dashboard Streamlit"""
    print("\n🚀 Iniciando Dashboard Moderno...")
    print("📱 Interface será aberta em: http://localhost:8501")
    print("🔗 Use Ctrl+C para parar o servidor")
    print("=" * 60)
    
    try:
        # Adicionar delay para dar tempo de ler as mensagens
        time.sleep(2)
        
        # Executar Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'modern_dashboard.py',
            '--server.port=8501',
            '--server.headless=false',
            '--browser.serverAddress=localhost',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false'
        ])
    
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard finalizado pelo usuário")
        print("   Obrigado por usar o Sistema F5!")
    
    except FileNotFoundError:
        print("\n❌ Streamlit não encontrado!")
        print("   Tentando instalação automática...")
        install_package('streamlit')
        print("   Tente executar novamente: python startup_dashboard.py")
    
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("   Entre em contato com o suporte técnico")

def show_help():
    """Exibe informações de ajuda"""
    help_text = """
    🆘 AJUDA - Dashboard F5 Estratégia
    
    📋 COMO USAR:
    1. Execute: python startup_dashboard.py
    2. Aguarde a instalação das dependências (primeira vez)
    3. O dashboard abrirá automaticamente no navegador
    4. Use Ctrl+C para parar o servidor
    
    🔧 SOLUÇÃO DE PROBLEMAS:
    • Erro de permissão: Execute com privilégios de admin
    • Erro de rede: Verifique conexão com internet
    • Erro de Python: Certifique-se de usar Python 3.8+
    
    📞 SUPORTE:
    • Documentação: README.md
    • Issues: GitHub do projeto
    • Email: suporte@f5estrategia.com
    """
    print(help_text)

def main():
    """Função principal"""
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        return
    
    # Banner de inicialização
    print_banner()
    
    # Verificações do sistema
    print("🔍 Executando verificações do sistema...")
    check_python_version()
    
    # Instalar dependências
    check_and_install_dependencies()
    
    # Verificar arquivos
    if not check_files():
        print("\n❌ Sistema incompleto. Verifique os arquivos e tente novamente.")
        return
    
    print("\n✅ Sistema pronto para iniciar!")
    print("⏳ Iniciando em 3 segundos...")
    time.sleep(3)
    
    # Iniciar dashboard
    start_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Inicialização cancelada pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        print("   Execute com --help para mais informações") 