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

#### Obter Mensagens do Chat
```python
response = client.chat.get_messages(
    instance_id,
    remote_jid="5511999999999@s.whatsapp.net",
    instance_token=instance_token,
    page=1,  # página opcional (padrão: 1)
    offset=50  # limite de mensagens por página opcional (padrão: 50)
)
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