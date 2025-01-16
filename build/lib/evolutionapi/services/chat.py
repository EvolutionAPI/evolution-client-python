from typing import Union, BinaryIO, Optional
from ..models.chat import *

class ChatService:
    def __init__(self, client):
        self.client = client

    def check_is_whatsapp_numbers(self, instance_id: str, data: CheckIsWhatsappNumber, instance_token: str):
        return self.client.post(
            f'chat/checkIsWhatsappNumber/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )
    
    def mark_message_as_read(self, instance_id: str, messages: List[ReadMessage], instance_token: str):
        return self.client.post(
            f'chat/markMessageAsRead/{instance_id}',
            data={"readMessages": [m.__dict__ for m in messages]},
            instance_token=instance_token
        )

    def archive_chat(self, instance_id: str, data: ArchiveChat, instance_token: str):
        return self.client.post(
            f'chat/archiveChat/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def mark_chat_unread(self, instance_id: str, data: UnreadChat, instance_token: str):
        return self.client.post(
            f'chat/markChatUnread/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def delete_message_for_everyone(self, instance_id: str, data: MessageKey, instance_token: str):
        return self.client.delete(
            f'chat/deleteMessageForEveryone/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def fetch_profile_picture_url(self, instance_id: str, data: ProfilePicture, instance_token: str):
        return self.client.post(
            f'chat/fetchProfilePictureUrl/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def get_base64_from_media_message(self, instance_id: str, data: MediaMessage, instance_token: str):
        return self.client.post(
            f'chat/getBase64FromMediaMessage/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def update_message(self, instance_id: str, data: UpdateMessage, instance_token: str):
        return self.client.post(
            f'chat/updateMessage/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def send_presence(self, instance_id: str, data: Presence, instance_token: str):
        return self.client.post(
            f'chat/sendPresence/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )
    
    def get_messages(
        self, 
        instance_id: str, 
        remote_jid: str, 
        instance_token: str, 
        message_id: Optional[str] = None,
        whatsapp_message_id: Optional[str] = None,
        from_me: Optional[bool] = None,
        message_type: Optional[str] = None,
        source: Optional[str] = None,
        timestamp_start: Optional[str] = None,
        timestamp_end: Optional[str] = None,
        page: int = 1, 
        offset: int = 50
    ):
        '''
        Obtém mensagens de um chat com filtros opcionais
        
        Args:
            timestamp_start: Data inicial no formato ISO (ex: "2025-01-16T00:00:00Z")
            timestamp_end: Data final no formato ISO (ex: "2025-01-16T23:59:59Z")
        '''
        where = {"key": {"remoteJid": remote_jid}}
        
        if message_id:
            where["id"] = message_id
        if whatsapp_message_id:
            where["key"]["id"] = whatsapp_message_id
        if from_me is not None:
            where["key"]["fromMe"] = from_me
        if message_type:
            where["messageType"] = message_type
        if source:
            where["source"] = source
        if timestamp_start or timestamp_end:
            where["messageTimestamp"] = {}
            if timestamp_start:
                where["messageTimestamp"]["gte"] = timestamp_start
            if timestamp_end:
                where["messageTimestamp"]["lte"] = timestamp_end
            
        payload = {
            "where": where,
            "page": page,
            "offset": offset,
        }
        
        return self.client.post(
            f'chat/findMessages/{instance_id}', 
            data=payload,
            instance_token=instance_token,
        )
