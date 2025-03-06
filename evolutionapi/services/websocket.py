import socketio
from typing import Callable, Dict, Any
import logging
import ssl
import time
from typing import Optional

class WebSocketManager:
    def __init__(self, base_url: str, instance_id: str, api_token: str, max_retries: int = 5, retry_delay: float = 1.0):
        """
        Inicializa o gerenciador de WebSocket
        
        Args:
            base_url (str): URL base da API
            instance_id (str): ID da instância
            api_token (str): Token de autenticação da API
            max_retries (int): Número máximo de tentativas de reconexão
            retry_delay (float): Delay inicial entre tentativas em segundos
        """
        self.base_url = base_url.rstrip('/')
        self.instance_id = instance_id
        self.api_token = api_token
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retry_count = 0
        self.should_reconnect = True
        
        # Configuração do Socket.IO
        self.sio = socketio.Client(
            ssl_verify=False,  # Para desenvolvimento local
            logger=False,
            engineio_logger=False,
            request_timeout=30
        )
        
        # Configura o logger da classe para INFO
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Dicionário para armazenar os handlers registrados
        self._handlers = {}
        
        # Configuração dos handlers de eventos
        self.sio.on('connect', self._on_connect)
        self.sio.on('disconnect', self._on_disconnect)
        self.sio.on('error', self._on_error)
        
        # Registra o handler global no namespace específico da instância
        self.sio.on('*', self._handle_event, namespace=f'/{self.instance_id}')
    
    def _on_connect(self):
        """Handler para evento de conexão"""
        self.logger.info("Socket.IO conectado")
        self.retry_count = 0  # Reseta o contador de retry após conexão bem-sucedida
    
    def _on_disconnect(self):
        """Handler para evento de desconexão"""
        self.logger.warning(f"Socket.IO desconectado. Tentativa {self.retry_count + 1}/{self.max_retries}")
        if self.should_reconnect and self.retry_count < self.max_retries:
            self._attempt_reconnect()
        else:
            self.logger.error("Número máximo de tentativas de reconexão atingido")
    
    def _on_error(self, error):
        """Handler para eventos de erro"""
        self.logger.error(f"Erro no Socket.IO: {str(error)}", exc_info=True)
    
    def _attempt_reconnect(self):
        """Tenta reconectar com backoff exponencial"""
        try:
            delay = self.retry_delay * (2 ** self.retry_count)  # Backoff exponencial
            self.logger.info(f"Tentando reconectar em {delay:.2f} segundos...")
            time.sleep(delay)
            self.connect()
            self.retry_count += 1
        except Exception as e:
            self.logger.error(f"Erro durante tentativa de reconexão: {str(e)}", exc_info=True)
            if self.retry_count < self.max_retries:
                self._attempt_reconnect()
            else:
                self.logger.error("Todas as tentativas de reconexão falharam")
    
    def _handle_event(self, event, *args):
        """Handler global para todos os eventos"""
        # Só processa eventos que foram registrados
        if event in self._handlers:
            self.logger.debug(f"Evento recebido no namespace /{self.instance_id}: {event}")
            self.logger.debug(f"Dados do evento: {args}")
            
            try:
                # Extrai os dados do evento
                raw_data = args[0] if args else {}
                
                # Garante que estamos passando o objeto correto para o callback
                if isinstance(raw_data, dict):
                    self.logger.debug(f"Chamando handler para {event} com dados: {raw_data}")
                    self._handlers[event](raw_data)
                else:
                    self.logger.error(f"Dados inválidos recebidos para evento {event}: {raw_data}")
            except Exception as e:
                self.logger.error(f"Erro ao processar evento {event}: {str(e)}", exc_info=True)
    
    def connect(self):
        """Conecta ao servidor Socket.IO"""
        try:
            # Conecta apenas ao namespace da instância com o header de autenticação
            self.sio.connect(
                f"{self.base_url}?apikey={self.api_token}",
                transports=['websocket'],
                namespaces=[f'/{self.instance_id}'],
                wait_timeout=30
            )
            
            # Entra na sala específica da instância
            self.sio.emit('subscribe', {'instance': self.instance_id}, namespace=f'/{self.instance_id}')
            
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao Socket.IO: {str(e)}", exc_info=True)
            raise
    
    def disconnect(self):
        """Desconecta do servidor Socket.IO"""
        self.should_reconnect = False  # Impede tentativas de reconexão
        if self.sio.connected:
            self.sio.disconnect()
    
    def on(self, event: str, callback: Callable):
        """
        Registra um callback para um evento específico
        
        Args:
            event (str): Nome do evento
            callback (Callable): Função a ser chamada quando o evento ocorrer
        """
        self._handlers[event] = callback