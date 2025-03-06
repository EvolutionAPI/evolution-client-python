from evolutionapi.client import EvolutionClient
from evolutionapi.models.instance import InstanceConfig
from evolutionapi.models.message import TextMessage, MediaMessage, MediaType
from evolutionapi.services.websocket import WebSocketManager
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

# Inicializando o WebSocket
websocket_manager = WebSocketManager(
    base_url='http://localhost:8081',
    instance_id=instance_id,
    api_token=instance_token
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

logger.info("Registrando handlers de eventos...")

# Registrando handlers de eventos
websocket_manager.on('messages.upsert', on_message)

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

# print("Buscando instâncias")
# instances = client.instances.fetch_instances()

# print("Instâncias encontradas")
# print(instances)

# print("Criando instância")
# config = InstanceConfig(
#     instanceName="instance-python3",
#     integration="WHATSAPP-BAILEYS",
#     qrcode=True,
# )

# new_instance = client.instances.create_instance(config)

# print("Instância criada")
# print(new_instance)

# instance_token = new_instance['hash']
# instance_id = new_instance['instance']['instanceName']

# print("Recuperando estado de conexão")
# connection_state = client.instance_operations.get_connection_state(instance_id, instance_token)

# print("Estado de conexão")
# print(connection_state)

# print("Conectando instância")
# connection_state = client.instance_operations.connect(instance_id, instance_token)

# print("Estado de conexão")
# print(connection_state)

# print("Reiniciando instância")
# restart_instance = client.instance_operations.restart(instance_id, instance_token)

# print("Instância reiniciada")
# print(restart_instance)

# print("Desconectando instância")
# logout_instance = client.instance_operations.logout(instance_id, instance_token)

# print("Instância desconectada")
# print(logout_instance)

# print("Deletando instância")
# delete_instance = client.instance_operations.delete(instance_id, instance_token)

# print("Instância deletada")
# print(delete_instance)

# group_id = "120363026465248932@g.us"

# # Buscando as 3 últimas mensagens do grupo
# mensagens = client.chat.get_messages(
#     instance_id=instance_id,
#     remote_jid=group_id,
#     instance_token=instance_token,
#     timestamp_start="2025-01-16T00:00:00Z",
#     timestamp_end="2025-01-16T23:59:59Z",
#     page=1,
#     offset=10
# )

# print("Mensagens encontradas:")
# print(mensagens)