#!/usr/bin/env python3
"""
Script Launcher - Dashboard Moderno F5
Executa o dashboard avançado com UX sofisticado

Para executar:
python run_modern_dashboard.py

Ou diretamente:
streamlit run modern_dashboard.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = ['streamlit', 'plotly', 'pandas']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - não encontrado")
    
    if missing_packages:
        print(f"\n🔧 Instalando dependências faltantes: {', '.join(missing_packages)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ Dependências instaladas com sucesso!")
    
    return True

def main():
    """Função principal"""
    print("🚀 Iniciando Dashboard Moderno F5 Estratégia")
    print("=" * 50)
    
    # Verificar dependências
    print("🔍 Verificando dependências...")
    check_dependencies()
    
    # Verificar se o arquivo do dashboard existe
    dashboard_file = Path("modern_dashboard.py")
    if not dashboard_file.exists():
        print("❌ Arquivo modern_dashboard.py não encontrado!")
        return
    
    print("\n🎯 Iniciando dashboard...")
    print("📱 Interface disponível em: http://localhost:8501")
    print("🔗 Use Ctrl+C para parar o servidor")
    print("=" * 50)
    
    # Executar Streamlit
    try:
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'modern_dashboard.py',
            '--server.port=8501',
            '--server.headless=false',
            '--browser.serverAddress=localhost'
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard finalizado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")

if __name__ == "__main__":
    main() 