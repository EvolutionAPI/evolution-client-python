from evolutionapi.client import EvolutionClient
from evolutionapi.models.instance import InstanceConfig
from evolutionapi.models.message import TextMessage, MediaMessage, MediaType
from evolutionapi.models.websocket import WebSocketConfig
import time
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("Iniciando cliente")

client = EvolutionClient(
    base_url='http://localhost:8081',
    api_token='429683C4C977415CAAFCCE10F7D57E11'
)

instance_token = "82D55E57CBBC-48A5-98FB-E99655AE7148"
instance_id = "teste"

# Configurando eventos do WebSocket
websocket_config = WebSocketConfig(
    enabled=True,
    events=[
        "APPLICATION_STARTUP",
        "QRCODE_UPDATED",
        "MESSAGES_SET",
        "MESSAGES_UPSERT",
        "MESSAGES_UPDATE",
        "MESSAGES_DELETE",
        "SEND_MESSAGE",
        "CONTACTS_SET",
        "CONTACTS_UPSERT",
        "CONTACTS_UPDATE",
        "PRESENCE_UPDATE",
        "CHATS_SET",
        "CHATS_UPSERT",
        "CHATS_UPDATE",
        "CHATS_DELETE",
        "GROUPS_UPSERT",
        "GROUP_UPDATE",
        "GROUP_PARTICIPANTS_UPDATE",
        "CONNECTION_UPDATE",
        "LABELS_EDIT",
        "LABELS_ASSOCIATION",
        "CALL",
        "TYPEBOT_START",
        "TYPEBOT_CHANGE_STATUS"
    ]
)

# Configurando WebSocket para a instância
logger.info("Configurando WebSocket...")
response = client.websocket.set_websocket(instance_id, websocket_config, instance_token)
logger.info(f"Configuração WebSocket: {response}")

# Obtendo configuração atual do WebSocket
websocket_info = client.websocket.find_websocket(instance_id, instance_token)
logger.info(f"WebSocket habilitado: {websocket_info.enabled}")
logger.info(f"Eventos configurados: {websocket_info.events}")

# Criando gerenciador WebSocket usando o cliente
logger.info("Criando gerenciador WebSocket...")
websocket_manager = client.create_websocket(
    instance_id=instance_id,
    api_token=instance_token,
    max_retries=5,
    retry_delay=1.0
)
    
def on_message(data):
    """Handler para evento de mensagens"""
    try:
        if 'data' in data:
            message_data = data['data']
            logger.info("=== Mensagem Recebida ===")
            logger.info(f"De: {message_data['key']['remoteJid']}")
            logger.info(f"Tipo: {message_data['messageType']}")
            
            # Extrai o conteúdo baseado no tipo da mensagem
            if 'message' in message_data:
                if 'conversation' in message_data['message']:
                    logger.info(f"Conteúdo: {message_data['message']['conversation']}")
                elif 'extendedTextMessage' in message_data['message']:
                    logger.info(f"Conteúdo: {message_data['message']['extendedTextMessage']['text']}")
                elif 'imageMessage' in message_data['message']:
                    logger.info(f"Conteúdo: [Imagem] {message_data['message']['imageMessage'].get('caption', '')}")
                else:
                    logger.info(f"Conteúdo: {message_data['message']}")
            
            logger.info("=======================")
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)

def on_qrcode(data):
    """Handler para evento de QR Code"""
    logger.info("=== QR Code Atualizado ===")
    logger.info(f"QR Code: {data}")
    logger.info("=======================")

def on_connection(data):
    """Handler para evento de conexão"""
    logger.info("=== Status de Conexão ===")
    logger.info(f"Status: {data}")
    logger.info("=======================")

logger.info("Registrando handlers de eventos...")

# Registrando handlers de eventos
websocket_manager.on('messages.upsert', on_message)
websocket_manager.on('qrcode.updated', on_qrcode)
websocket_manager.on('connection.update', on_connection)

try:
    logger.info("Iniciando conexão WebSocket...")
    # Conectando ao WebSocket
    websocket_manager.connect()
    
    # Mantendo o programa rodando para receber eventos
    logger.info("Aguardando eventos...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logger.info("Encerrando conexão WebSocket...")
finally:
    websocket_manager.disconnect()

# Exemplos de outras operações (comentados)
# response = client.group.fetch_all_groups(instance_id, instance_token, False)
# print(response)

# text_message = TextMessage(
#     number="557499879409",
#     text="Olá, como vai?",
#     delay=1200
# )

# response = client.messages.send_text(instance_id, text_message, instance_token)
# print("Mensagem de texto enviada")
# print(response)

# media_message = MediaMessage(
#     number="557499879409",
#     mediatype="document",
#     mimetype="application/pdf",
#     caption="Olá, como vai?",
#     fileName="arquivo.pdf"
# )

# response = client.messages.send_media(instance_id, media_message, instance_token, "arquivo.pdf")
# print("Mensagem de mídia enviada")
# print(response)