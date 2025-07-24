"""
Configurações da Aplicação YouTube Optimization System - F5 Estratégia
"""

import os
from dotenv import load_dotenv
from typing import Dict, List, Optional

load_dotenv()

class YouTubeConfig:
    """Configurações para APIs do YouTube"""
    
    # Credenciais da API
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
    
    # Arquivo de credenciais OAuth (baixado do Google Cloud Console)
    CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE', 'client_secret.json')
    
    # Escopo de permissões
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/yt-analytics.readonly',
        'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
    ]
    
    # Canal da F5 Estratégia
    CHANNEL_ID = os.getenv('F5_CHANNEL_ID')
    CHANNEL_NAME = "F5 Estratégia"
    
    # Configurações de API
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    ANALYTICS_SERVICE_NAME = "youtubeAnalytics"
    ANALYTICS_VERSION = "v2"
    
    # Configurações de quota (YouTube API tem limites)
    DAILY_QUOTA_LIMIT = 10000  # Unidades por dia
    REQUESTS_PER_MINUTE = 100   # Requests por minuto

class F5Config:
    """Configurações específicas da F5 Estratégia"""
    
    # Metodologia CHAVI
    CHAVI_PILLARS = {
        'C': 'Campanha',
        'H': 'Humanização', 
        'A': 'Anúncios',
        'V': 'Vendas',
        'I': 'Inteligência'
    }
    
    # Personas de Cliente
    PERSONAS = {
        'estrategico': {
            'name': 'Empresário Estratégico',
            'age_range': '35-55',
            'revenue': 'R$ 300k+/mês',
            'focus': ['métricas detalhadas', 'inovação tecnológica', 'crescimento sustentável']
        },
        'crescimento': {
            'name': 'Empresário em Crescimento',
            'age_range': '30-45',
            'revenue': 'R$ 50-300k/mês',
            'focus': ['cases comprovação', 'soluções práticas', 'estruturar funil']
        },
        'smart': {
            'name': 'Empresário Smart',
            'age_range': '25-40',
            'revenue': 'até R$ 50k/mês',
            'focus': ['resultados rápidos', 'geração caixa', 'leads reais']
        }
    }
    
    # Arquétipos da Marca
    BRAND_ARCHETYPES = {
        'primary': 'Sábio',
        'secondary': 'Herói',
        'tone': ['confiável', 'analítico', 'determinado', 'focado resultados']
    }
    
    # Palavras-chave principais
    CORE_KEYWORDS = [
        'marketing digital',
        'tráfego pago',
        'meta ads',
        'google ads', 
        'growth marketing',
        'vendas online',
        'crm',
        'funil de vendas',
        'lead generation'
    ]

class AIConfig:
    """Configurações para integração com IA - Usando Gemini (Google AI)"""
    
    # Google Gemini API (Principal)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = 'gemini-2.5-pro'  # Gemini 2.5 Pro - Modelo mais avançado
    
    # Fallback para Claude (opcional)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'
    
    # Fallback para OpenAI (opcional)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4-turbo-preview'
    
    # Google Cloud AI (para análises complementares)
    GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
    VERTEX_AI_MODEL = 'gemini-pro'
    
    # Configurações de geração
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
    # Prompts padrão para Gemini
    CONTENT_OPTIMIZATION_PROMPT = """
    Analise o seguinte conteúdo de YouTube considerando:
    1. SEO para YouTube
    2. Metodologia CHAVI da F5 Estratégia
    3. Persona alvo: {persona}
    4. Palavras-chave: {keywords}
    
    Forneça sugestões específicas e acionáveis para otimização.
    
    Contexto da F5 Estratégia:
    - Agência de marketing digital
    - Metodologia CHAVI (Campanha, Humanização, Anúncios, Vendas, Inteligência)
    - Foco em resultados e dados
    - Tom: Sábio + Herói (confiável, analítico, determinado)
    """

class DatabaseConfig:
    """Configurações do banco de dados"""
    
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///f5_youtube_optimizer.db')
    ENABLE_ECHO = os.getenv('DATABASE_ECHO', 'False').lower() == 'true'

class AppConfig:
    """Configurações gerais da aplicação"""
    
    # Ambiente
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Coleta de dados
    DATA_COLLECTION_INTERVAL = int(os.getenv('DATA_COLLECTION_INTERVAL', '3600'))  # 1 hora
    MAX_VIDEOS_PER_REQUEST = int(os.getenv('MAX_VIDEOS_PER_REQUEST', '50'))
    
    # Rate limiting para respeitar quotas do YouTube
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', '100'))  # requests por minuto
    
    # Diretórios
    DATA_DIR = os.path.join(os.getcwd(), 'data')
    REPORTS_DIR = os.path.join(os.getcwd(), 'reports')
    LOGS_DIR = os.path.join(os.getcwd(), 'logs')
    CREDENTIALS_DIR = os.path.join(os.getcwd(), 'credentials')
    
    @classmethod
    def ensure_directories(cls):
        """Cria os diretórios necessários se não existirem"""
        for dir_path in [cls.DATA_DIR, cls.REPORTS_DIR, cls.LOGS_DIR, cls.CREDENTIALS_DIR]:
            os.makedirs(dir_path, exist_ok=True)

# Configurações de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': os.path.join(AppConfig.LOGS_DIR, 'f5_youtube_optimizer.log'),
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['default', 'file'],
    },
}

# Validação de configurações
def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    required_vars = [
        'YOUTUBE_API_KEY',
        'F5_CHANNEL_ID'
    ]
    
    # Verificar se pelo menos uma API de IA está configurada
    ai_configured = bool(os.getenv('GEMINI_API_KEY')) or bool(os.getenv('ANTHROPIC_API_KEY')) or bool(os.getenv('OPENAI_API_KEY'))
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing_vars)}")
    
    if not ai_configured:
        raise ValueError("Configure pelo menos uma API de IA (GEMINI_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY)")
    
    # Verificar se arquivo de credenciais OAuth existe
    client_secrets_file = YouTubeConfig.CLIENT_SECRETS_FILE
    if not os.path.exists(client_secrets_file):
        raise ValueError(f"Arquivo de credenciais não encontrado: {client_secrets_file}")
    
    return True

def get_setup_instructions():
    """Retorna instruções de setup para as APIs"""
    return """
    🔧 INSTRUÇÕES DE SETUP - APIs DO YOUTUBE:
    
    1. GOOGLE CLOUD CONSOLE:
       - Acesse: https://console.cloud.google.com/
       - Crie projeto: 'F5-YouTube-Analytics-System'
       - Habilite APIs: YouTube Data API v3, YouTube Analytics API, YouTube Reporting API
    
    2. CREDENCIAIS OAUTH:
       - Configure tela de consentimento OAuth
       - Crie credenciais OAuth 2.0 (aplicativo desktop)
       - Baixe como 'client_secret.json'
    
    3. API KEY:
       - Crie chave de API
       - Restrinja para YouTube APIs
    
    4. ARQUIVO .env:
       YOUTUBE_API_KEY=sua_api_key_aqui
       F5_CHANNEL_ID=id_do_canal_f5_aqui
       GEMINI_API_KEY=sua_gemini_key_aqui
       GOOGLE_CLOUD_PROJECT=seu_projeto_gcp_aqui
    
    5. ARQUIVO DE CREDENCIAIS:
       - Coloque 'client_secret.json' na raiz do projeto
    
    📚 Documentação: https://developers.google.com/youtube/analytics?hl=pt-br
    """ 