import requests
from requests_toolbelt import MultipartEncoder
from .exceptions import EvolutionAuthenticationError, EvolutionNotFoundError, EvolutionAPIError
from .services.instance import InstanceService
from .services.instance_operations import InstanceOperationsService
from .services.message import MessageService
from .services.call import CallService
from .services.chat import ChatService
from .services.label import LabelService
from .services.profile import ProfileService
from .services.group import GroupService
from .services.websocket import WebSocketService, WebSocketManager

class EvolutionClient:
    """
    Cliente para interagir com a API Evolution.

    Args:
        base_url (str): A URL base do servidor da API Evolution.
        api_token (str): O token de autenticação para acessar a API.
    """

    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.instances = InstanceService(self)
        self.instance_operations = InstanceOperationsService(self)
        self.messages = MessageService(self)
        self.calls = CallService(self)
        self.chat = ChatService(self)
        self.label = LabelService(self)
        self.profile = ProfileService(self)
        self.group = GroupService(self)
        self.websocket = WebSocketService(self)
        
    def _get_headers(self, instance_token: str = None):
        return {
            'apikey': instance_token or self.api_token,
            'Content-Type': 'application/json'
        }

    def _get_full_url(self, endpoint):
        return f'{self.base_url}/{endpoint}'

    def _handle_response(self, response):
        if response.status_code == 401:
            raise EvolutionAuthenticationError('Falha na autenticação.')
        elif response.status_code == 404:
            raise EvolutionNotFoundError('Recurso não encontrado.')
        elif response.ok:
            try:
                return response.json()
            except ValueError:
                return response.content
        else:
            error_detail = ''
            try:
                error_detail = f' - {response.json()}'
            except:
                error_detail = f' - {response.text}'
            raise EvolutionAPIError(f'Erro na requisição: {response.status_code}{error_detail}')

    def get(self, endpoint: str, instance_token: str = None):
        """Faz uma requisição GET."""
        url = self._get_full_url(endpoint)
        response = requests.get(url, headers=self._get_headers(instance_token))
        return self._handle_response(response)

    def post(self, endpoint: str, data: dict = None, instance_token: str = None, files: dict = None):
        url = f'{self.base_url}/{endpoint}'
        headers = self._get_headers(instance_token)
        
        if files:
            # Remove o Content-Type do header quando enviando arquivos
            if 'Content-Type' in headers:
                del headers['Content-Type']
            
            # Prepara os campos do multipart
            fields = {}
            
            # Adiciona os campos do data
            for key, value in data.items():
                fields[key] = str(value) if not isinstance(value, (int, float)) else (None, str(value), 'text/plain')
            
            # Adiciona o arquivo
            file_tuple = files['file']
            fields['file'] = (file_tuple[0], file_tuple[1], file_tuple[2])
            
            # Cria o multipart encoder
            multipart = MultipartEncoder(fields=fields)
            headers['Content-Type'] = multipart.content_type
            
            response = requests.post(
                url, 
                headers=headers,
                data=multipart
            )
        else:
            response = requests.post(
                url, 
                headers=headers, 
                json=data
            )
        
        return response.json()

    def put(self, endpoint, data=None):
        """Faz uma requisição PUT."""
        url = self._get_full_url(endpoint)
        response = requests.put(url, headers=self.headers, json=data)
        return self._handle_response(response)

    def delete(self, endpoint: str, instance_token: str = None):
        """Faz uma requisição DELETE."""
        url = self._get_full_url(endpoint)
        response = requests.delete(url, headers=self._get_headers(instance_token))
        return self._handle_response(response)

    def create_websocket(self, instance_id: str, api_token: str, max_retries: int = 5, retry_delay: float = 1.0) -> WebSocketManager:
        """
        Create a WebSocket manager for the specified instance.
        
        Args:
            instance_id (str): The instance ID
            api_token (str): The API token
            max_retries (int): Maximum number of reconnection attempts
            retry_delay (float): Initial delay between attempts in seconds
            
        Returns:
            WebSocketManager: The WebSocket manager instance
        """
        return WebSocketManager(
            base_url=self.base_url,
            instance_id=instance_id,
            api_token=api_token,
            max_retries=max_retries,
            retry_delay=retry_delay
        )
