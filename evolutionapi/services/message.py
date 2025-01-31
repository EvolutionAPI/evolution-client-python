from typing import Union, BinaryIO
from ..models.message import *
from requests_toolbelt import MultipartEncoder
import mimetypes
import requests

class MessageService:
    def __init__(self, client):
        self.client = client

    def send_text(self, instance_id: str, message: TextMessage, instance_token: str):
        # Preparar os dados como JSON
        data = {}
        
        # Add all additional kwargs to data dictionary
        data.update(message.__dict__)
        
        # Usar o método post do cliente que já trata JSON corretamente
        return self.client.post(
            f'message/sendText/{instance_id}',
            data=data,
            instance_token=instance_token
        )

    def send_media(self, instance_id: str, message: MediaMessage, instance_token: str, file: Union[BinaryIO, str] = None):
        # Preparar os dados do formulário
        fields = {
            'number': (None, message.number, 'text/plain'),
            'mediatype': (None, message.mediatype, 'text/plain'),
            'mimetype': (None, message.mimetype, 'text/plain'),
            'caption': (None, message.caption, 'text/plain'),
            'fileName': (None, message.fileName, 'text/plain'),
        }
        
        # Adicionar delay apenas se existir
        if hasattr(message, 'delay') and message.delay is not None:
            fields['delay'] = (None, str(message.delay), 'text/plain; type=number')
        
        # Adicionar o arquivo se fornecido
        if file:
            if isinstance(file, str):
                mime_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'
                fields['file'] = ('file', open(file, 'rb'), mime_type)
            else:
                fields['file'] = ('file', file, 'application/octet-stream')
        
        # Criar o multipart encoder
        multipart = MultipartEncoder(fields=fields)
        
        # Preparar os headers
        headers = self.client._get_headers(instance_token)
        headers['Content-Type'] = multipart.content_type
        
        # Fazer a requisição diretamente
        url = f'{self.client.base_url}/message/sendMedia/{instance_id}'
        response = requests.post(
            url,
            headers=headers,
            data=multipart
        )
        
        return response.json()

    def send_ptv(self, instance_id: str, message: dict, instance_token: str, file: Union[BinaryIO, str] = None):
        fields = {}
        
        # Adiciona todos os campos do message como text/plain
        for key, value in message.items():
            if key == 'delay' and value is not None:
                fields[key] = (None, str(value), 'text/plain; type=number')
            else:
                fields[key] = (None, str(value), 'text/plain')
        
        if file:
            if isinstance(file, str):
                mime_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'
                fields['file'] = ('file', open(file, 'rb'), mime_type)
            else:
                fields['file'] = ('file', file, 'application/octet-stream')
        
        multipart = MultipartEncoder(fields=fields)
        headers = self.client._get_headers(instance_token)
        headers['Content-Type'] = multipart.content_type
        
        url = f'{self.client.base_url}/message/sendPtv/{instance_id}'
        response = requests.post(url, headers=headers, data=multipart)
        return response.json()

    def send_whatsapp_audio(self, instance_id: str, message: dict, instance_token: str, file: Union[BinaryIO, str] = None):
        fields = {}
        
        # Adiciona todos os campos do message como text/plain
        for key, value in message.items():
            if key == 'delay' and value is not None:
                fields[key] = (None, str(value), 'text/plain; type=number')
            else:
                fields[key] = (None, str(value), 'text/plain')
        
        if file:
            if isinstance(file, str):
                mime_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'
                fields['file'] = ('file', open(file, 'rb'), mime_type)
            else:
                fields['file'] = ('file', file, 'application/octet-stream')
        
        multipart = MultipartEncoder(fields=fields)
        headers = self.client._get_headers(instance_token)
        headers['Content-Type'] = multipart.content_type
        
        url = f'{self.client.base_url}/message/sendWhatsAppAudio/{instance_id}'
        response = requests.post(url, headers=headers, data=multipart)
        return response.json()

    def send_status(self, instance_id: str, message: StatusMessage, instance_token: str):
        return self.client.post(
            f'message/sendStatus/{instance_id}',
            data=message.__dict__,
            instance_token=instance_token
        )

    def send_sticker(self, instance_id: str, message: dict, instance_token: str, file: Union[BinaryIO, str] = None):
        fields = {}
        
        # Adiciona todos os campos do message como text/plain
        for key, value in message.items():
            if key == 'delay' and value is not None:
                fields[key] = (None, str(value), 'text/plain; type=number')
            else:
                fields[key] = (None, str(value), 'text/plain')
        
        if file:
            if isinstance(file, str):
                mime_type = mimetypes.guess_type(file)[0] or 'application/octet-stream'
                fields['file'] = ('file', open(file, 'rb'), mime_type)
            else:
                fields['file'] = ('file', file, 'application/octet-stream')
        
        multipart = MultipartEncoder(fields=fields)
        headers = self.client._get_headers(instance_token)
        headers['Content-Type'] = multipart.content_type
        
        url = f'{self.client.base_url}/message/sendSticker/{instance_id}'
        response = requests.post(url, headers=headers, data=multipart)
        return response.json()

    def send_location(self, instance_id: str, message: LocationMessage, instance_token: str):
        data = message.__dict__.copy()
        if 'delay' in data and data['delay'] is not None:
            data['delay'] = int(data['delay'])
        
        return self.client.post(
            f'message/sendLocation/{instance_id}',
            data=data,
            instance_token=instance_token
        )

    def send_contact(self, instance_id: str, message: ContactMessage, instance_token: str):
        return self.client.post(
            f'message/sendContact/{instance_id}',
            data=message.__dict__,
            instance_token=instance_token
        )

    def send_reaction(self, instance_id: str, message: ReactionMessage, instance_token: str):
        return self.client.post(
            f'message/sendReaction/{instance_id}',
            data=message.__dict__,
            instance_token=instance_token
        )

    def send_poll(self, instance_id: str, message: PollMessage, instance_token: str):
        data = message.__dict__.copy()
        if 'delay' in data and data['delay'] is not None:
            data['delay'] = int(data['delay'])
        
        return self.client.post(
            f'message/sendPoll/{instance_id}',
            data=data,
            instance_token=instance_token
        )

    def send_list(self, instance_id: str, message: ListMessage, instance_token: str):
        data = message.__dict__.copy()
        if 'delay' in data and data['delay'] is not None:
            data['delay'] = int(data['delay'])
        
        return self.client.post(
            f'message/sendList/{instance_id}',
            data=data,
            instance_token=instance_token
        )

    def send_buttons(self, instance_id: str, message: ButtonMessage, instance_token: str):
        data = message.__dict__.copy()
        if 'delay' in data and data['delay'] is not None:
            data['delay'] = int(data['delay'])
        
        return self.client.post(
            f'message/sendButtons/{instance_id}',
            data=data,
            instance_token=instance_token
        )