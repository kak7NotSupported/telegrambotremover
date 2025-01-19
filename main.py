from datetime import datetime
from time import sleep

from telethon import TelegramClient
from telethon.tl.types import Channel, ChannelAdminLogEvent, User

# Укажите ваши данные API
api_id = 123456
api_hash = 'aabbccddeeffgg1122334455'
channel_username = -1001892464745  # Например, '@example_channel'

delete_after_date = datetime(2025, 1, 16)  # Дата, после которой добавленные пользователи будут удалены


async def remove_recent_users():
    async with TelegramClient('anon', api_id, api_hash) as client:
        client: TelegramClient
        # Получение объекта канала

        channel = await client.get_entity(channel_username)

        # Получение списка участников
        async for user in client.iter_participants(channel):
            # Проверяем дату добавления пользователя
            if user.date and user.date > delete_after_date:
                try:
                    # await client.kick_participant(channel, user.id)
                    print(f"Удалён пользователь: {user.id} ({user.username})")
                except Exception as e:
                    print(f"Не удалось удалить пользователя {user.id}: {e}")


client = TelegramClient('anon', api_id, api_hash)


async def main():
    me = await client.get_me()

    username = me.username

    channel: Channel = await client.get_entity(channel_username)
    print(channel)
    count = 0

    members = await client.get_participants(channel)
    print(len(members))

    async for event in client.iter_admin_log(
            channel,
            join=True,  # Указываем, что интересуют только события входа
            limit=999  # Устанавливаем лимит событий
    ):
        if event.user:  # Проверяем, есть ли информация о пользователе
            event: ChannelAdminLogEvent
            user: User = event.user
            if user not in members:
                print(f"skipped {user.username}")
                continue
            await client.edit_permissions(channel, user.id, view_messages=False)
                # see in documentation how to kick

            print(f"{user.first_name} @{user.username} {event.date.strftime('%d/%m/%Y')}")
            count += 1

    print(count)


with client:
    client.loop.run_until_complete(main())
