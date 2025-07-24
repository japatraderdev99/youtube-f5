"""
YouTube API Manager - Sistema de integração com APIs nativas do YouTube
Desenvolvido para F5 Estratégia
"""

import logging
import pickle
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import YouTubeConfig, AppConfig, F5Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeAPIManager:
    """Gerenciador principal para as APIs do YouTube"""
    
    def __init__(self):
        self.config = YouTubeConfig()
        self.app_config = AppConfig()
        
        # Serviços da API
        self.youtube_service = None
        self.analytics_service = None
        
        # Credenciais
        self.credentials = None
        
        # Cache de dados
        self.cache = {}
        
        self._setup_services()
    
    def _setup_services(self):
        """Configura os serviços das APIs do YouTube"""
        try:
            self.credentials = self._get_authenticated_credentials()
            
            # YouTube Data API v3
            self.youtube_service = build(
                self.config.API_SERVICE_NAME,
                self.config.API_VERSION,
                credentials=self.credentials
            )
            
            # YouTube Analytics API v2
            self.analytics_service = build(
                self.config.ANALYTICS_SERVICE_NAME,
                self.config.ANALYTICS_VERSION,
                credentials=self.credentials
            )
            
            logger.info("Serviços das APIs do YouTube configurados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao configurar serviços da API: {e}")
            raise
    
    def _get_authenticated_credentials(self) -> Credentials:
        """Obtém credenciais autenticadas para as APIs"""
        credentials = None
        token_file = "token.pickle"
        
        # Carrega credenciais existentes se disponíveis
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
        
        # Se não há credenciais válidas, inicia o fluxo de autenticação
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                # Usar arquivo client_secret.json diretamente
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.config.CLIENT_SECRETS_FILE,
                    self.config.SCOPES
                )
                credentials = flow.run_local_server(port=0)
            
            # Salva as credenciais para próxima execução
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
        
        return credentials

class YouTubeAnalyticsCollector:
    """Coletor de dados do YouTube Analytics API"""
    
    def __init__(self, api_manager: YouTubeAPIManager):
        self.api_manager = api_manager
        self.analytics_service = api_manager.analytics_service
        self.channel_id = YouTubeConfig.CHANNEL_ID
    
    def get_channel_performance(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Coleta métricas de performance do canal
        
        Args:
            start_date (str): Data de início (YYYY-MM-DD)
            end_date (str): Data de fim (YYYY-MM-DD)
        
        Returns:
            Dict com métricas de performance
        """
        try:
            # Métricas principais do canal
            response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost',
                dimensions='day'
            ).execute()
            
            return self._process_analytics_response(response)
            
        except HttpError as e:
            logger.error(f"Erro ao coletar performance do canal: {e}")
            return {}
    
    def get_traffic_sources(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Coleta dados de fontes de tráfego - DADOS MAIS VALIOSOS PARA SEO
        
        Args:
            start_date (str): Data de início
            end_date (str): Data de fim
        
        Returns:
            Dict com dados de fontes de tráfego
        """
        try:
            # Fontes de tráfego geral
            traffic_response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='insightTrafficSourceType',
                sort='-views'
            ).execute()
            
            # Detalhes de busca - DADOS ÚNICOS E VALIOSOS
            search_response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='insightTrafficSourceDetail',
                filters='insightTrafficSourceType==YT_SEARCH',
                sort='-views',
                maxResults=100
            ).execute()
            
            return {
                'traffic_sources': self._process_analytics_response(traffic_response),
                'search_terms': self._process_analytics_response(search_response)
            }
            
        except HttpError as e:
            logger.error(f"Erro ao coletar fontes de tráfego: {e}")
            return {}
    
    def get_audience_demographics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Coleta dados demográficos da audiência
        
        Args:
            start_date (str): Data de início
            end_date (str): Data de fim
        
        Returns:
            Dict com dados demográficos
        """
        try:
            # Dados por idade e gênero
            demographics_response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='viewerPercentage',
                dimensions='ageGroup,gender',
                sort='-viewerPercentage'
            ).execute()
            
            # Dados por localização
            geography_response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='views,estimatedMinutesWatched',
                dimensions='country',
                sort='-views',
                maxResults=20
            ).execute()
            
            return {
                'demographics': self._process_analytics_response(demographics_response),
                'geography': self._process_analytics_response(geography_response)
            }
            
        except HttpError as e:
            logger.error(f"Erro ao coletar dados demográficos: {e}")
            return {}
    
    def get_video_performance(self, video_ids: List[str], start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Coleta métricas de performance de vídeos específicos
        
        Args:
            video_ids (List[str]): Lista de IDs dos vídeos
            start_date (str): Data de início
            end_date (str): Data de fim
        
        Returns:
            Dict com métricas dos vídeos
        """
        try:
            video_filter = ','.join([f'video=={vid}' for vid in video_ids])
            
            response = self.analytics_service.reports().query(
                ids=f"channel=={self.channel_id}",
                startDate=start_date,
                endDate=end_date,
                metrics='views,likes,dislikes,comments,shares,estimatedMinutesWatched,averageViewDuration',
                dimensions='video',
                filters=video_filter,
                sort='-views'
            ).execute()
            
            return self._process_analytics_response(response)
            
        except HttpError as e:
            logger.error(f"Erro ao coletar performance dos vídeos: {e}")
            return {}
    
    def _process_analytics_response(self, response: Dict) -> Dict[str, Any]:
        """Processa resposta da API Analytics em formato mais utilizável"""
        if not response.get('rows'):
            return {'data': [], 'headers': []}
        
        headers = [col['name'] for col in response.get('columnHeaders', [])]
        data = []
        
        for row in response['rows']:
            row_dict = dict(zip(headers, row))
            data.append(row_dict)
        
        return {
            'data': data,
            'headers': headers,
            'total_rows': len(data)
        }

class YouTubeDataCollector:
    """Coletor de dados públicos via YouTube Data API v3"""
    
    def __init__(self, api_manager: YouTubeAPIManager):
        self.api_manager = api_manager
        self.youtube_service = api_manager.youtube_service
        self.channel_id = YouTubeConfig.CHANNEL_ID
    
    def get_channel_videos(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Obtém lista de vídeos do canal da F5
        
        Args:
            max_results (int): Número máximo de vídeos a retornar
        
        Returns:
            Lista de dicionários com dados dos vídeos
        """
        try:
            # Primeiro, obter o upload playlist ID
            channel_response = self.youtube_service.channels().list(
                part='contentDetails',
                id=self.channel_id
            ).execute()
            
            upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Obter vídeos da playlist de uploads
            videos = []
            next_page_token = None
            
            while len(videos) < max_results:
                playlist_response = self.youtube_service.playlistItems().list(
                    part='snippet',
                    playlistId=upload_playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                ).execute()
                
                for item in playlist_response['items']:
                    video_data = {
                        'video_id': item['snippet']['resourceId']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail_url': item['snippet']['thumbnails']['default']['url']
                    }
                    videos.append(video_data)
                
                next_page_token = playlist_response.get('nextPageToken')
                if not next_page_token:
                    break
            
            return videos
            
        except HttpError as e:
            logger.error(f"Erro ao obter vídeos do canal: {e}")
            return []
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Obtém detalhes completos de vídeos específicos
        
        Args:
            video_ids (List[str]): Lista de IDs dos vídeos
        
        Returns:
            Lista com detalhes dos vídeos
        """
        try:
            # A API permite até 50 IDs por request
            all_videos = []
            
            for i in range(0, len(video_ids), 50):
                batch_ids = video_ids[i:i+50]
                
                response = self.youtube_service.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=','.join(batch_ids)
                ).execute()
                
                for item in response['items']:
                    video_data = {
                        'video_id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'tags': item['snippet'].get('tags', []),
                        'published_at': item['snippet']['publishedAt'],
                        'duration': item['contentDetails']['duration'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'comment_count': int(item['statistics'].get('commentCount', 0)),
                        'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                    }
                    all_videos.append(video_data)
            
            return all_videos
            
        except HttpError as e:
            logger.error(f"Erro ao obter detalhes dos vídeos: {e}")
            return []
    
    def search_competitor_videos(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """
        Busca vídeos de concorrentes por palavra-chave
        
        Args:
            query (str): Termo de busca
            max_results (int): Número máximo de resultados
        
        Returns:
            Lista de vídeos encontrados
        """
        try:
            search_response = self.youtube_service.search().list(
                q=query,
                part='snippet',
                maxResults=max_results,
                order='relevance',
                type='video',
                publishedAfter=(datetime.now() - timedelta(days=90)).isoformat() + 'Z'  # Últimos 90 dias
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_title': item['snippet']['channelTitle'],
                    'channel_id': item['snippet']['channelId'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url']
                }
                videos.append(video_data)
            
            return videos
            
        except HttpError as e:
            logger.error(f"Erro ao buscar vídeos concorrentes: {e}")
            return []
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Obtém comentários de um vídeo específico
        
        Args:
            video_id (str): ID do vídeo
            max_results (int): Número máximo de comentários
        
        Returns:
            Lista de comentários
        """
        try:
            comments = []
            next_page_token = None
            
            while len(comments) < max_results:
                response = self.youtube_service.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=min(100, max_results - len(comments)),
                    order='relevance',
                    pageToken=next_page_token
                ).execute()
                
                for item in response['items']:
                    comment_data = {
                        'comment_id': item['id'],
                        'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        'like_count': item['snippet']['topLevelComment']['snippet']['likeCount'],
                        'published_at': item['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                    comments.append(comment_data)
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
            
            return comments
            
        except HttpError as e:
            logger.error(f"Erro ao obter comentários do vídeo {video_id}: {e}")
            return []

# Função principal para inicializar o sistema
def initialize_youtube_system():
    """Inicializa o sistema completo de APIs do YouTube"""
    try:
        # Criar diretórios necessários
        AppConfig.ensure_directories()
        
        # Inicializar gerenciador de APIs
        api_manager = YouTubeAPIManager()
        
        # Inicializar coletores
        analytics_collector = YouTubeAnalyticsCollector(api_manager)
        data_collector = YouTubeDataCollector(api_manager)
        
        logger.info("Sistema YouTube API inicializado com sucesso")
        
        return {
            'api_manager': api_manager,
            'analytics_collector': analytics_collector,
            'data_collector': data_collector
        }
        
    except Exception as e:
        logger.error(f"Erro ao inicializar sistema YouTube API: {e}")
        raise

if __name__ == "__main__":
    # Teste básico do sistema
    system = initialize_youtube_system()
    logger.info("Sistema inicializado e pronto para uso!") 