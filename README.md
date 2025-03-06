# Evolution Client Python

Client Python para interagir com a API evolutionapi.

## Instalação

```bash
pip install evolutionapi
```

## Uso Básico

### Inicializando o Cliente

```python
from evolutionapi.client import EvolutionClient

client = EvolutionClient(
    base_url='http://seu-servidor:porta',
    api_token='seu-token-api'
)
```

### Gerenciamento de Instâncias

#### Listar Instâncias
```python
instances = client.instances.fetch_instances()
```

#### Criar Nova Instância
```python
from evolutionapi.models.instance import InstanceConfig

config = InstanceConfig(
    instanceName="minha-instancia",
    integration="WHATSAPP-BAILEYS",
    qrcode=True
)

nova_instancia = client.instances.create_instance(config)
```

### Operações com Instâncias

#### Conectar Instância
```python
estado = client.instance_operations.connect(instance_id, instance_token)
```

#### Verificar Estado da Conexão
```python
estado = client.instance_operations.get_connection_state(instance_id, instance_token)
```

#### Definir Presença
```python
from evolutionapi.models.presence import PresenceStatus

client.instance_operations.set_presence(
    instance_id,
    PresenceStatus.AVAILABLE,
    instance_token
)
```

### Enviando Mensagens

#### Mensagem de Texto
```python
from evolutionapi.models.message import TextMessage

mensagem = TextMessage(
    number="5511999999999",
    text="Olá, como vai?",
    delay=1000  # delay opcional em ms
)

response = client.messages.send_text(instance_id, mensagem, instance_token)
```

#### Mensagem de Mídia
```python
from evolutionapi.models.message import MediaMessage, MediaType

mensagem = MediaMessage(
    number="5511999999999",
    mediatype=MediaType.IMAGE.value,
    mimetype="image/jpeg",
    caption="Minha imagem",
    media="base64_da_imagem_ou_url",
    fileName="imagem.jpg"
)

response = client.messages.send_media(instance_id, mensagem, instance_token)
```

#### Mensagem com Botões
```python
from evolutionapi.models.message import ButtonMessage, Button

botoes = [
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

mensagem = ButtonMessage(
    number="5511999999999",
    title="Título",
    description="Descrição",
    footer="Rodapé",
    buttons=botoes
)

response = client.messages.send_buttons(instance_id, mensagem, instance_token)
```

#### Mensagem com Lista
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

mensagem = ListMessage(
    number="5511999999999",
    title="Título da Lista",
    description="Descrição da lista",
    buttonText="Clique aqui",
    footerText="Rodapé",
    sections=[section]
)

response = client.messages.send_list(instance_id, mensagem, instance_token)
```

### Gerenciamento de Grupos

#### Criar Grupo
```python
from evolutionapi.models.group import CreateGroup

config = CreateGroup(
    subject="Nome do Grupo",
    participants=["5511999999999", "5511888888888"],
    description="Descrição do grupo"
)

response = client.group.create_group(instance_id, config, instance_token)
```

#### Atualizar Foto do Grupo
```python
from evolutionapi.models.group import GroupPicture

config = GroupPicture(
    image="base64_da_imagem"
)

response = client.group.update_group_picture(instance_id, "grupo_jid", config, instance_token)
```

#### Gerenciar Participantes
```python
from evolutionapi.models.group import UpdateParticipant

config = UpdateParticipant(
    action="add",  # ou "remove", "promote", "demote"
    participants=["5511999999999"]
)

response = client.group.update_participant(instance_id, "grupo_jid", config, instance_token)
```

### Gerenciamento de Perfil

#### Atualizar Nome do Perfil
```python
from evolutionapi.models.profile import ProfileName

config = ProfileName(
    name="Novo Nome"
)

response = client.profile.update_profile_name(instance_id, config, instance_token)
```

#### Atualizar Status
```python
from evolutionapi.models.profile import ProfileStatus

config = ProfileStatus(
    status="Novo status"
)

response = client.profile.update_profile_status(instance_id, config, instance_token)
```

#### Configurar Privacidade
```python
from evolutionapi.models.profile import PrivacySettings

config = PrivacySettings(
    readreceipts="all",
    profile="contacts",
    status="contacts",
    online="all",
    last="contacts",
    groupadd="contacts"
)

response = client.profile.update_privacy_settings(instance_id, config, instance_token)
```

### Operações de Chat

#### Verificar Números WhatsApp
```python
from evolutionapi.models.chat import CheckIsWhatsappNumber

config = CheckIsWhatsappNumber(
    numbers=["5511999999999", "5511888888888"]
)

response = client.chat.check_is_whatsapp_numbers(instance_id, config, instance_token)
```

#### Marcar Mensagem como Lida
```python
from evolutionapi.models.chat import ReadMessage

mensagem = ReadMessage(
    remote_jid="5511999999999@s.whatsapp.net",
    from_me=False,
    id="mensagem_id"
)

response = client.chat.mark_message_as_read(instance_id, [mensagem], instance_token)
```

### Chamadas

#### Simular Chamada
```python
from evolutionapi.models.call import FakeCall

config = FakeCall(
    number="5511999999999",
    isVideo=False,
    callDuration=30
)

response = client.calls.fake_call(instance_id, config, instance_token)
```

### Labels

#### Gerenciar Labels
```python
from evolutionapi.models.label import HandleLabel

config = HandleLabel(
    number="5511999999999",
    label_id="label_id",
    action="add"  # ou "remove"
)

response = client.label.handle_label(instance_id, config, instance_token)
```

## WebSocket

O cliente Evolution API suporta conexão via WebSocket para receber eventos em tempo real. Aqui está um guia de como usar:

### Configuração Básica

```python
from evolutionapi.services.websocket import WebSocketManager
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Configuração do WebSocket
websocket = WebSocketManager(
    base_url="http://localhost:8081",  # URL da sua Evolution API
    instance_id="teste",               # ID da sua instância
    api_token="seu-token-aqui"         # Token de autenticação
)
```

### Registrando Handlers de Eventos

Você pode registrar handlers para diferentes tipos de eventos:

```python
def handle_message(data):
    print(f"Nova mensagem recebida: {data}")

def handle_qrcode(data):
    print(f"QR Code atualizado: {data}")

# Registrando handlers
websocket.on("messages.upsert", handle_message)
websocket.on("qrcode.updated", handle_qrcode)
```

### Eventos Disponíveis

Os eventos disponíveis são:

#### Eventos de Instância
- `application.startup`: Disparado quando a aplicação inicia
- `instance.create`: Disparado quando uma nova instância é criada
- `instance.delete`: Disparado quando uma instância é deletada
- `remove.instance`: Disparado quando uma instância é removida
- `logout.instance`: Disparado quando uma instância faz logout

#### Eventos de Conexão e QR Code
- `qrcode.updated`: Disparado quando o QR Code é atualizado
- `connection.update`: Disparado quando o status da conexão muda
- `status.instance`: Disparado quando o status da instância muda
- `creds.update`: Disparado quando as credenciais são atualizadas

#### Eventos de Mensagens
- `messages.set`: Disparado quando mensagens são definidas
- `messages.upsert`: Disparado quando novas mensagens são recebidas
- `messages.edited`: Disparado quando mensagens são editadas
- `messages.update`: Disparado quando mensagens são atualizadas
- `messages.delete`: Disparado quando mensagens são deletadas
- `send.message`: Disparado quando uma mensagem é enviada
- `messaging-history.set`: Disparado quando o histórico de mensagens é definido

#### Eventos de Contatos
- `contacts.set`: Disparado quando contatos são definidos
- `contacts.upsert`: Disparado quando novos contatos são adicionados
- `contacts.update`: Disparado quando contatos são atualizados

#### Eventos de Chats
- `chats.set`: Disparado quando chats são definidos
- `chats.update`: Disparado quando chats são atualizados
- `chats.upsert`: Disparado quando novos chats são adicionados
- `chats.delete`: Disparado quando chats são deletados

#### Eventos de Grupos
- `groups.upsert`: Disparado quando grupos são criados/atualizados
- `groups.update`: Disparado quando grupos são atualizados
- `group-participants.update`: Disparado quando participantes de um grupo são atualizados

#### Eventos de Presença
- `presence.update`: Disparado quando o status de presença é atualizado

#### Eventos de Chamadas
- `call`: Disparado quando há uma chamada

#### Eventos de Typebot
- `typebot.start`: Disparado quando um typebot inicia
- `typebot.change-status`: Disparado quando o status do typebot muda

#### Eventos de Labels
- `labels.edit`: Disparado quando labels são editados
- `labels.association`: Disparado quando labels são associados/desassociados

### Exemplo de Uso com Eventos Específicos

```python
def handle_messages(data):
    logger.info(f"Nova mensagem: {data}")

def handle_contacts(data):
    logger.info(f"Contatos atualizados: {data}")

def handle_groups(data):
    logger.info(f"Grupos atualizados: {data}")

def handle_presence(data):
    logger.info(f"Status de presença: {data}")

# Registrando handlers para diferentes eventos
websocket.on("messages.upsert", handle_messages)
websocket.on("contacts.upsert", handle_contacts)
websocket.on("groups.upsert", handle_groups)
websocket.on("presence.update", handle_presence)
```

### Exemplo Completo

```python
from evolutionapi.services.websocket import WebSocketManager
import logging
import time

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def handle_message(data):
    logger.info(f"Nova mensagem recebida: {data}")

def handle_qrcode(data):
    logger.info(f"QR Code atualizado: {data}")

def handle_connection(data):
    logger.info(f"Status da conexão: {data}")

def main():
    # Inicializa o WebSocket
    websocket = WebSocketManager(
        base_url="http://localhost:8081",
        instance_id="teste",
        api_token="seu-token-aqui"
    )

    # Registra os handlers
    websocket.on("messages.upsert", handle_message)
    websocket.on("qrcode.updated", handle_qrcode)
    websocket.on("connection.update", handle_connection)

    try:
        # Conecta ao WebSocket
        websocket.connect()
        logger.info("Conectado ao WebSocket. Aguardando eventos...")

        # Mantém o programa rodando
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Encerrando conexão...")
        websocket.disconnect()
    except Exception as e:
        logger.error(f"Erro: {e}")
        websocket.disconnect()

if __name__ == "__main__":
    main()

### Recursos Adicionais

#### Reconexão Automática

O WebSocket Manager possui reconexão automática com backoff exponencial:

```python
websocket = WebSocketManager(
    base_url="http://localhost:8081",
    instance_id="teste",
    api_token="seu-token-aqui",
    max_retries=5,        # Número máximo de tentativas de reconexão
    retry_delay=1.0       # Delay inicial entre tentativas em segundos
)
```

#### Logging

O WebSocket Manager utiliza o sistema de logging do Python. Você pode ajustar o nível de log conforme necessário:

```python
# Para ver mais detalhes
logging.getLogger("evolutionapi.services.websocket").setLevel(logging.DEBUG)
```

### Tratamento de Erros

O WebSocket Manager possui tratamento de erros robusto:

- Reconexão automática em caso de desconexão
- Logs detalhados de erros
- Tratamento de eventos inválidos
- Validação de dados recebidos

### Dicas de Uso

1. Sempre use try/except ao conectar ao WebSocket
2. Implemente handlers para todos os eventos que você precisa monitorar
3. Use logging para debug e monitoramento
4. Considere implementar um mecanismo de heartbeat se necessário
5. Mantenha o token de API seguro e não o exponha em logs