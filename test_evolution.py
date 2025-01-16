from evolutionapi.client import EvolutionClient
from evolutionapi.models.instance import InstanceConfig
from evolutionapi.models.message import TextMessage, MediaMessage, MediaType


print("Iniciando cliente")

client = EvolutionClient(
    base_url='http://localhost:8081',
    api_token='429683C4C977415CAAFCCE10F7D57E11'
)


instance_token = "60BDC703E413-4710-9473-CA2A763866FE"
instance_id = "94a0aafa-e636-4534-a185-5562bf8f2c22"

response = client.group.fetch_all_groups(instance_id, instance_token, False)

print(response)

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