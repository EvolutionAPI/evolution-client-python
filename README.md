# Evolution Client Python

Python client to interact with the evolutionapi.

## Installation

```bash
pip install evolutionapi
```

## Basic Usage

### Initializing the Client

```python
from evolutionapi.client import EvolutionClient

client = EvolutionClient(
    base_url='http://your-server:port',
    api_token='your-api-token'
)
```

### Instance Management

#### List Instances
```python
instances = client.instances.fetch_instances()
```

#### Create New Instance
```python
from evolutionapi.models.instance import InstanceConfig

# Configuração básica
config = InstanceConfig(
    instanceName="minha-instancia",
    integration="WHATSAPP-BAILEYS",
    qrcode=True
)

# Configuração completa
config = InstanceConfig(
    instanceName="minha-instancia",
    integration="WHATSAPP-BAILEYS",
    token="token_da_instancia",
    number="5511999999999",
    qrcode=True,
    rejectCall=True,
    msgCall="Mensagem de chamada rejeitada",
    groupsIgnore=True,
    alwaysOnline=True,
    readMessages=True,
    readStatus=True,
    syncFullHistory=True
)

new_instance = client.instances.create_instance(config)
```

#### Configure Webhook
```python
from evolutionapi.models.instance import WebhookConfig

config = WebhookConfig(
    url="https://seu-servidor.com/webhook",
    byEvents=True,
    base64=True,
    headers={
        "Authorization": "Bearer seu-token"
    },
    events=[
        "messages.upsert",
        "messages.update",
        "messages.delete",
        "groups.upsert",
        "groups.update",
        "groups.delete",
        "group-participants.update",
        "contacts.upsert",
        "contacts.update",
        "contacts.delete",
        "presence.update",
        "chats.upsert",
        "chats.update",
        "chats.delete",
        "call"
    ]
)

response = client.instances.set_webhook(instance_id, config, instance_token)
```

#### Configure Events
```python
from evolutionapi.models.instance import EventsConfig

config = EventsConfig(
    enabled=True,
    events=[
        "messages.upsert",
        "messages.update",
        "messages.delete",
        "groups.upsert",
        "groups.update",
        "groups.delete",
        "group-participants.update",
        "contacts.upsert",
        "contacts.update",
        "contacts.delete",
        "presence.update",
        "chats.upsert",
        "chats.update",
        "chats.delete",
        "call"
    ]
)

response = client.instances.set_events(instance_id, config, instance_token)
```

#### Configure Chatwoot Integration
```python
from evolutionapi.models.instance import ChatwootConfig

config = ChatwootConfig(
    accountId="seu-account-id",
    token="seu-token",
    url="https://seu-chatwoot.com",
    signMsg=True,
    reopenConversation=True,
    conversationPending=False,
    importContacts=True,
    nameInbox="evolution",
    mergeBrazilContacts=True,
    importMessages=True,
    daysLimitImportMessages=3,
    organization="Evolution Bot",
    logo="https://evolution-api.com/files/evolution-api-favicon.png"
)

response = client.instances.set_chatwoot(instance_id, config, instance_token)
```

#### Delete Instance
```python
response = client.instances.delete_instance(instance_id, instance_token)
```

#### Get Instance Info
```python
response = client.instances.get_instance_info(instance_id, instance_token)
```

#### Get Instance QR Code
```python
response = client.instances.get_instance_qrcode(instance_id, instance_token)
```

#### Get Instance Status
```python
response = client.instances.get_instance_status(instance_id, instance_token)
```

#### Logout Instance
```python
response = client.instances.logout_instance(instance_id, instance_token)
```

#### Restart Instance
```python
response = client.instances.restart_instance(instance_id, instance_token)
```

### Instance Operations

#### Connect Instance
```python
state = client.instance_operations.connect(instance_id, instance_token)
```

#### Check Connection State
```python
state = client.instance_operations.get_connection_state(instance_id, instance_token)
```

#### Set Presence
```python
from evolutionapi.models.presence import PresenceConfig, PresenceStatus

# Definir como disponível
config = PresenceConfig(
    presence=PresenceStatus.AVAILABLE
)

# Definir como indisponível
config = PresenceConfig(
    presence=PresenceStatus.UNAVAILABLE
)

response = client.instance_operations.set_presence(instance_id, config, instance_token)
```

### Sending Messages

#### Text Message
```python
from evolutionapi.models.message import TextMessage, QuotedMessage

# Mensagem simples
message = TextMessage(
    number="5511999999999",
    text="Olá, como você está?",
    delay=1000  # delay opcional em ms
)

# Mensagem com menções
message = TextMessage(
    number="5511999999999",
    text="@everyone Olá a todos!",
    mentionsEveryOne=True,
    mentioned=["5511999999999", "5511888888888"]
)

# Mensagem com link preview
message = TextMessage(
    number="5511999999999",
    text="Confira este link: https://exemplo.com",
    linkPreview=True
)

# Mensagem com citação
quoted = QuotedMessage(
    key={
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": False,
        "participant": "5511999999999@s.whatsapp.net",
        "id": "123456789",
        "owner": "5511999999999@s.whatsapp.net"
    }
)

message = TextMessage(
    number="5511999999999",
    text="Esta é uma resposta",
    quoted=quoted
)

response = client.messages.send_text(instance_id, message, instance_token)
```

#### Media Message
```python
from evolutionapi.models.message import MediaMessage, MediaType, QuotedMessage

# Mensagem com imagem
message = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.IMAGE.value,
    mimetype="image/jpeg",
    caption="Minha imagem",
    media="base64_da_imagem_ou_url",
    fileName="imagem.jpg",
    delay=1000  # delay opcional
)

# Mensagem com vídeo
message = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.VIDEO.value,
    mimetype="video/mp4",
    caption="Meu vídeo",
    media="base64_do_video_ou_url",
    fileName="video.mp4"
)

# Mensagem com documento
message = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.DOCUMENT.value,
    mimetype="application/pdf",
    caption="Meu documento",
    media="base64_do_documento_ou_url",
    fileName="documento.pdf"
)

# Mensagem com menções
message = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.IMAGE.value,
    mimetype="image/jpeg",
    caption="@everyone Olhem esta imagem!",
    media="base64_da_imagem",
    mentionsEveryOne=True,
    mentioned=["5511999999999", "5511888888888"]
)

response = client.messages.send_media(instance_id, message, instance_token)
```

#### Status Message
```python
from evolutionapi.models.message import StatusMessage, StatusType, FontType

# Status de texto
message = StatusMessage(
    type=StatusType.TEXT,
    content="Meu status de texto",
    caption="Legenda opcional",
    backgroundColor="#FF0000",
    font=FontType.BEBASNEUE_REGULAR,
    allContacts=True
)

# Status de imagem
message = StatusMessage(
    type=StatusType.IMAGE,
    content="base64_da_imagem",
    caption="Minha imagem de status"
)

# Status de vídeo
message = StatusMessage(
    type=StatusType.VIDEO,
    content="base64_do_video",
    caption="Meu vídeo de status"
)

# Status de áudio
message = StatusMessage(
    type=StatusType.AUDIO,
    content="base64_do_audio",
    caption="Meu áudio de status"
)

response = client.messages.send_status(instance_id, message, instance_token)
```

#### Location Message
```python
from evolutionapi.models.message import LocationMessage

message = LocationMessage(
    number="5511999999999",
    name="Localização",
    address="Endereço completo",
    latitude=-23.550520,
    longitude=-46.633308,
    delay=1000  # delay opcional
)

response = client.messages.send_location(instance_id, message, instance_token)
```

#### Contact Message
```python
from evolutionapi.models.message import ContactMessage, Contact

contact = Contact(
    fullName="Nome Completo",
    wuid="5511999999999",
    phoneNumber="5511999999999",
    organization="Empresa",
    email="email@exemplo.com",
    url="https://exemplo.com"
)

message = ContactMessage(
    number="5511999999999",
    contact=[contact]
)

response = client.messages.send_contact(instance_id, message, instance_token)
```

#### Reaction Message
```python
from evolutionapi.models.message import ReactionMessage

message = ReactionMessage(
    key={
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": False,
        "participant": "5511999999999@s.whatsapp.net",
        "id": "123456789",
        "owner": "5511999999999@s.whatsapp.net"
    },
    reaction="👍"
)

response = client.messages.send_reaction(instance_id, message, instance_token)
```

#### Poll Message
```python
from evolutionapi.models.message import PollMessage

message = PollMessage(
    number="5511999999999",
    name="Minha Enquete",
    selectableCount=1,  # número de opções que podem ser selecionadas
    values=["Opção 1", "Opção 2", "Opção 3"],
    delay=1000  # delay opcional
)

response = client.messages.send_poll(instance_id, message, instance_token)
```

#### Button Message
```python
from evolutionapi.models.message import ButtonMessage, Button

# Botão de resposta simples
buttons = [
    Button(
        type="reply",
        displayText="Opção 1",
        id="1"
    ),
    Button(
        type="reply",
        displayText="Opção 2",
        id="2"
    )
]

# Botão com URL
buttons = [
    Button(
        type="url",
        displayText="Visitar Site",
        url="https://exemplo.com"
    )
]

# Botão com número de telefone
buttons = [
    Button(
        type="phoneNumber",
        displayText="Ligar",
        phoneNumber="5511999999999"
    )
]

# Botão com código de cópia
buttons = [
    Button(
        type="copyCode",
        displayText="Copiar Código",
        copyCode="ABC123"
    )
]

message = ButtonMessage(
    number="5511999999999",
    title="Título",
    description="Descrição",
    footer="Rodapé",
    buttons=buttons,
    delay=1000  # delay opcional
)

response = client.messages.send_buttons(instance_id, message, instance_token)
```

#### List Message
```python
from evolutionapi.models.message import ListMessage, ListSection, ListRow

rows = [
    ListRow(
        title="Item 1",
        description="Descrição do item 1",
        rowId="1"
    ),
    ListRow(
        title="Item 2",
        description="Descrição do item 2",
        rowId="2"
    )
]

section = ListSection(
    title="Seção 1",
    rows=rows
)

message = ListMessage(
    number="5511999999999",
    title="Título da Lista",
    description="Descrição da lista",
    buttonText="Clique aqui",
    footerText="Rodapé",
    sections=[section],
    delay=1000  # delay opcional
)

response = client.messages.send_list(instance_id, message, instance_token)
```

### Group Management

#### Create Group
```python
from evolutionapi.models.group import CreateGroup

config = CreateGroup(
    subject="Nome do Grupo",
    participants=["5511999999999", "5511888888888"],
    description="Descrição do grupo"
)

response = client.group.create_group(instance_id, config, instance_token)
```

#### Update Group Picture
```python
from evolutionapi.models.group import GroupPicture

config = GroupPicture(
    image="base64_da_imagem"
)

response = client.group.update_group_picture(instance_id, "group_jid", config, instance_token)
```

#### Update Group Subject
```python
from evolutionapi.models.group import GroupSubject

config = GroupSubject(
    subject="Novo Nome do Grupo"
)

response = client.group.update_group_subject(instance_id, "group_jid", config, instance_token)
```

#### Update Group Description
```python
from evolutionapi.models.group import GroupDescription

config = GroupDescription(
    description="Nova descrição do grupo"
)

response = client.group.update_group_description(instance_id, "group_jid", config, instance_token)
```

#### Send Group Invite
```python
from evolutionapi.models.group import GroupInvite

config = GroupInvite(
    groupJid="group_jid",
    description="Convite para o grupo",
    numbers=["5511999999999", "5511888888888"]
)

response = client.group.send_group_invite(instance_id, config, instance_token)
```

#### Manage Participants
```python
from evolutionapi.models.group import UpdateParticipant

# Adicionar participantes
config = UpdateParticipant(
    action="add",
    participants=["5511999999999", "5511888888888"]
)

# Remover participantes
config = UpdateParticipant(
    action="remove",
    participants=["5511999999999"]
)

# Promover a administrador
config = UpdateParticipant(
    action="promote",
    participants=["5511999999999"]
)

# Rebaixar de administrador
config = UpdateParticipant(
    action="demote",
    participants=["5511999999999"]
)

response = client.group.update_participant(instance_id, "group_jid", config, instance_token)
```

#### Update Group Settings
```python
from evolutionapi.models.group import UpdateSetting

# Ativar modo anúncio
config = UpdateSetting(
    action="announcement"
)

# Desativar modo anúncio
config = UpdateSetting(
    action="not_announcement"
)

# Bloquear grupo
config = UpdateSetting(
    action="locked"
)

# Desbloquear grupo
config = UpdateSetting(
    action="unlocked"
)

response = client.group.update_setting(instance_id, "group_jid", config, instance_token)
```

#### Toggle Ephemeral Messages
```python
from evolutionapi.models.group import ToggleEphemeral

config = ToggleEphemeral(
    expiration=86400  # 24 horas em segundos
)

response = client.group.toggle_ephemeral(instance_id, "group_jid", config, instance_token)
```

### Profile Management

#### Fetch Profile
```python
from evolutionapi.models.profile import FetchProfile

config = FetchProfile(
    number="5511999999999"
)

response = client.profile.fetch_profile(instance_id, config, instance_token)
```

#### Update Profile Name
```python
from evolutionapi.models.profile import ProfileName

config = ProfileName(
    name="Novo Nome"
)

response = client.profile.update_profile_name(instance_id, config, instance_token)
```

#### Update Status
```python
from evolutionapi.models.profile import ProfileStatus

config = ProfileStatus(
    status="Novo status"
)

response = client.profile.update_profile_status(instance_id, config, instance_token)
```

#### Update Profile Picture
```python
from evolutionapi.models.profile import ProfilePicture

config = ProfilePicture(
    picture="base64_da_imagem"
)

response = client.profile.update_profile_picture(instance_id, config, instance_token)
```

#### Configure Privacy Settings
```python
from evolutionapi.models.profile import PrivacySettings

config = PrivacySettings(
    readreceipts="all",           # "all" ou "none"
    profile="contacts",           # "all", "contacts", "contact_blacklist" ou "none"
    status="contacts",            # "all", "contacts", "contact_blacklist" ou "none"
    online="all",                 # "all" ou "match_last_seen"
    last="contacts",              # "all", "contacts", "contact_blacklist" ou "none"
    groupadd="contacts"           # "all", "contacts" ou "contact_blacklist"
)

response = client.profile.update_privacy_settings(instance_id, config, instance_token)
```

### Chat Operations

#### Check WhatsApp Numbers
```python
from evolutionapi.models.chat import CheckIsWhatsappNumber

config = CheckIsWhatsappNumber(
    numbers=["5511999999999", "5511888888888"]
)

response = client.chat.check_is_whatsapp_numbers(instance_id, config, instance_token)
```

#### Mark Message as Read
```python
from evolutionapi.models.chat import ReadMessage

message = ReadMessage(
    remote_jid="5511999999999@s.whatsapp.net",
    from_me=False,
    id="message_id"
)

response = client.chat.mark_message_as_read(instance_id, [message], instance_token)
```

#### Archive Chat
```python
from evolutionapi.models.chat import ArchiveChat

config = ArchiveChat(
    last_message={
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "message_id",
            "participant": "5511999999999@s.whatsapp.net"
        },
        "message": {
            "conversation": "Última mensagem"
        }
    },
    chat="5511999999999@s.whatsapp.net",
    archive=True  # True para arquivar, False para desarquivar
)

response = client.chat.archive_chat(instance_id, config, instance_token)
```

#### Mark Chat as Unread
```python
from evolutionapi.models.chat import UnreadChat

config = UnreadChat(
    last_message={
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "message_id",
            "participant": "5511999999999@s.whatsapp.net"
        },
        "message": {
            "conversation": "Última mensagem"
        }
    },
    chat="5511999999999@s.whatsapp.net"
)

response = client.chat.unread_chat(instance_id, config, instance_token)
```

#### Get Chat Profile Picture
```python
from evolutionapi.models.chat import ProfilePicture

config = ProfilePicture(
    number="5511999999999"
)

response = client.chat.get_chat_profile_picture(instance_id, config, instance_token)
```

#### Download Media Message
```python
from evolutionapi.models.chat import MediaMessage

config = MediaMessage(
    message={
        "key": {
            "remoteJid": "5511999999999@s.whatsapp.net",
            "fromMe": False,
            "id": "message_id",
            "participant": "5511999999999@s.whatsapp.net"
        },
        "message": {
            "imageMessage": {
                "jpegThumbnail": "base64_da_imagem"
            }
        }
    },
    convert_to_mp4=True  # opcional, para converter vídeos para MP4
)

response = client.chat.download_media_message(instance_id, config, instance_token)
```

#### Update Message
```python
from evolutionapi.models.chat import UpdateMessage

config = UpdateMessage(
    number="5511999999999",
    key={
        "remoteJid": "5511999999999@s.whatsapp.net",
        "fromMe": False,
        "id": "message_id",
        "participant": "5511999999999@s.whatsapp.net"
    },
    text="Mensagem atualizada"
)

response = client.chat.update_message(instance_id, config, instance_token)
```

#### Set Presence
```python
from evolutionapi.models.chat import Presence

config = Presence(
    number="5511999999999",
    delay=1000,  # delay em ms
    presence="composing"  # "composing", "recording", "paused"
)

response = client.chat.set_presence(instance_id, config, instance_token)
```

### Calls

#### Simulate Call
```python
from evolutionapi.models.call import FakeCall

# Chamada de voz
config = FakeCall(
    number="5511999999999",
    isVideo=False,
    callDuration=30  # duração em segundos
)

# Chamada de vídeo
config = FakeCall(
    number="5511999999999",
    isVideo=True,
    callDuration=30  # duração em segundos
)

response = client.calls.fake_call(instance_id, config, instance_token)
```

### Labels

#### Manage Labels
```python
from evolutionapi.models.label import HandleLabel

# Adicionar etiqueta
config = HandleLabel(
    number="5511999999999",
    label_id="label_id",
    action="add"
)

# Remover etiqueta
config = HandleLabel(
    number="5511999999999",
    label_id="label_id",
    action="remove"
)

response = client.label.handle_label(instance_id, config, instance_token)
```

## WebSocket

The Evolution API client supports WebSocket connection to receive real-time events. Here's a guide on how to use it:

### Prerequisites

Before using WebSocket, you need to:

1. Enable WebSocket in your Evolution API by setting the environment variable:
```bash
WEBSOCKET_ENABLED=true
```

2. Configure WebSocket events for your instance using the WebSocket service:
```python
from evolutionapi.models.websocket import WebSocketConfig

# Configure WebSocket events
config = WebSocketConfig(
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

# Set WebSocket configuration
response = client.websocket.set_websocket(instance_id, config, instance_token)

# Get current WebSocket configuration
websocket_info = client.websocket.find_websocket(instance_id, instance_token)
print(f"WebSocket enabled: {websocket_info.enabled}")
print(f"Configured events: {websocket_info.events}")
```

### Basic Configuration

There are two ways to create a WebSocket manager:

1. Using the client's helper method:
```python
# Create WebSocket manager using the client
websocket = client.create_websocket(
    instance_id="test",
    max_retries=5,        # Maximum number of reconnection attempts
    retry_delay=1.0       # Initial delay between attempts in seconds
)
```

2. Creating the manager directly:
```python
from evolutionapi.services.websocket import WebSocketManager
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create WebSocket manager directly
websocket = WebSocketManager(
    base_url="http://localhost:8081",  # Your Evolution API URL
    instance_id="test",                # Your instance ID
    api_token="your-api-token"         # Your API token
)
```

### Registering Event Handlers

You can register handlers for different types of events:

```python
def handle_message(data):
    print(f"New message received: {data}")

def handle_qrcode(data):
    print(f"QR Code updated: {data}")

# Registering handlers
websocket.on("messages.upsert", handle_message)
websocket.on("qrcode.updated", handle_qrcode)
```

### Available Events

The available events are:

#### Instance Events
- `application.startup`: Triggered when the application starts
- `instance.create`: Triggered when a new instance is created
- `instance.delete`: Triggered when an instance is deleted
- `remove.instance`: Triggered when an instance is removed
- `logout.instance`: Triggered when an instance logs out

#### Connection and QR Code Events
- `qrcode.updated`: Triggered when the QR Code is updated
- `connection.update`: Triggered when connection status changes
- `status.instance`: Triggered when instance status changes
- `creds.update`: Triggered when credentials are updated

#### Message Events
- `messages.set`: Triggered when messages are set
- `messages.upsert`: Triggered when new messages are received
- `messages.edited`: Triggered when messages are edited
- `messages.update`: Triggered when messages are updated
- `messages.delete`: Triggered when messages are deleted
- `send.message`: Triggered when a message is sent
- `messaging-history.set`: Triggered when messaging history is set

#### Contact Events
- `contacts.set`: Triggered when contacts are set
- `contacts.upsert`: Triggered when new contacts are added
- `contacts.update`: Triggered when contacts are updated

#### Chat Events
- `chats.set`: Triggered when chats are set
- `chats.update`: Triggered when chats are updated
- `chats.upsert`: Triggered when new chats are added
- `chats.delete`: Triggered when chats are deleted

#### Group Events
- `groups.upsert`: Triggered when groups are created/updated
- `groups.update`: Triggered when groups are updated
- `group-participants.update`: Triggered when group participants are updated

#### Presence Events
- `presence.update`: Triggered when presence status is updated

#### Call Events
- `call`: Triggered when there's a call

#### Typebot Events
- `typebot.start`: Triggered when a typebot starts
- `typebot.change-status`: Triggered when typebot status changes

#### Label Events
- `labels.edit`: Triggered when labels are edited
- `labels.association`: Triggered when labels are associated/disassociated

### Example with Specific Events

```python
def handle_messages(data):
    logger.info(f"New message: {data}")

def handle_contacts(data):
    logger.info(f"Contacts updated: {data}")

def handle_groups(data):
    logger.info(f"Groups updated: {data}")

def handle_presence(data):
    logger.info(f"Presence status: {data}")

# Registering handlers for different events
websocket.on("messages.upsert", handle_messages)
websocket.on("contacts.upsert", handle_contacts)
websocket.on("groups.upsert", handle_groups)
websocket.on("presence.update", handle_presence)
```

### Complete Example

```python
from evolutionapi.services.websocket import WebSocketManager
import logging
import time

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_message(data):
    logger.info(f"New message received: {data}")

def handle_qrcode(data):
    logger.info(f"QR Code updated: {data}")

def handle_connection(data):
    logger.info(f"Connection status: {data}")

def main():
    # Initialize WebSocket
    websocket = WebSocketManager(
        base_url="http://localhost:8081",
        instance_id="test",
        api_token="your-api-token"
    )

    # Register handlers
    websocket.on("messages.upsert", handle_message)
    websocket.on("qrcode.updated", handle_qrcode)
    websocket.on("connection.update", handle_connection)

    try:
        # Connect to WebSocket
        websocket.connect()
        logger.info("Connected to WebSocket. Waiting for events...")

        # Keep the program running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Closing connection...")
        websocket.disconnect()
    except Exception as e:
        logger.error(f"Error: {e}")
        websocket.disconnect()

if __name__ == "__main__":
    main()
```

### Additional Features

#### Automatic Reconnection

The WebSocket Manager has automatic reconnection with exponential backoff:

```python
websocket = WebSocketManager(
    base_url="http://localhost:8081",
    instance_id="test",
    api_token="your-api-token",
    max_retries=5,        # Maximum number of reconnection attempts
    retry_delay=1.0       # Initial delay between attempts in seconds
)
```

#### Logging

The WebSocket Manager uses Python's logging system. You can adjust the log level as needed:

```python
# For more details
logging.getLogger("evolutionapi.services.websocket").setLevel(logging.DEBUG)
```

### Error Handling

The WebSocket Manager has robust error handling:

- Automatic reconnection on disconnection
- Detailed error logs
- Invalid event handling
- Data validation

### Usage Tips

1. Always use try/except when connecting to WebSocket
2. Implement handlers for all events you need to monitor
3. Use logging for debugging and monitoring
4. Consider implementing a heartbeat mechanism if needed
5. Keep your API token secure and don't expose it in logs