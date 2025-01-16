from typing import Optional
from ..models.group import *

class GroupService:
    def __init__(self, client):
        self.client = client

    def create_group(self, instance_id: str, data: CreateGroup, instance_token: str):
        return self.client.post(
            f'group/create/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def update_group_picture(self, instance_id: str, group_jid: str, data: GroupPicture, instance_token: str):
        return self.client.post(
            f'group/updateGroupPicture/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def update_group_subject(self, instance_id: str, group_jid: str, data: GroupSubject, instance_token: str):
        return self.client.post(
            f'group/updateGroupSubject/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def update_group_description(self, instance_id: str, group_jid: str, data: GroupDescription, instance_token: str):
        return self.client.post(
            f'group/updateGroupDescription/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def get_invite_code(self, instance_id: str, group_jid: str, instance_token: str):
        return self.client.get(
            f'group/inviteCode/{instance_id}?groupJid={group_jid}',
            instance_token=instance_token
        )

    def revoke_invite_code(self, instance_id: str, group_jid: str, instance_token: str):
        return self.client.post(
            f'group/revokeInviteCode/{instance_id}?groupJid={group_jid}',
            instance_token=instance_token
        )

    def send_invite(self, instance_id: str, data: GroupInvite, instance_token: str):
        return self.client.post(
            f'group/sendInvite/{instance_id}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def get_invite_info(self, instance_id: str, invite_code: str, instance_token: str):
        return self.client.get(
            f'group/inviteInfo/{instance_id}?inviteCode={invite_code}',
            instance_token=instance_token
        )

    def get_group_info(self, instance_id: str, group_jid: str, instance_token: str):
        return self.client.get(
            f'group/findGroupInfos/{instance_id}?groupJid={group_jid}',
            instance_token=instance_token
        )

    def fetch_all_groups(self, instance_id: str, instance_token: str, get_participants: bool = False):
        url = f'group/fetchAllGroups/{instance_id}?getParticipants={str(get_participants).lower()}'
        return self.client.get(
            url,
            instance_token=instance_token
        )

    def get_participants(self, instance_id: str, group_jid: str, instance_token: str):
        return self.client.get(
            f'group/participants/{instance_id}?groupJid={group_jid}',
            instance_token=instance_token
        )

    def update_participant(self, instance_id: str, group_jid: str, data: UpdateParticipant, instance_token: str):
        return self.client.post(
            f'group/updateParticipant/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def update_setting(self, instance_id: str, group_jid: str, data: UpdateSetting, instance_token: str):
        return self.client.post(
            f'group/updateSetting/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def toggle_ephemeral(self, instance_id: str, group_jid: str, data: ToggleEphemeral, instance_token: str):
        return self.client.post(
            f'group/toggleEphemeral/{instance_id}?groupJid={group_jid}',
            data=data.__dict__,
            instance_token=instance_token
        )

    def leave_group(self, instance_id: str, group_jid: str, instance_token: str):
        return self.client.delete(
            f'group/leaveGroup/{instance_id}?groupJid={group_jid}',
            instance_token=instance_token
        )