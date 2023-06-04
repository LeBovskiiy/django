import os
from dotenv import load_dotenv
from telethon import TelegramClient
         
load_dotenv()                         

admin_contact = os.getenv('ADMIN_CONTACTS').split(',')

client = TelegramClient('anon', api_id=os.getenv('API_ID'), api_hash=os.getenv('API_HASH'))

async def main(message):
    async with client:
        me = await client.get_me()
        username = me.username
        print(username)
        print(me.phone)

        message = await client.send_message(
            int(admin_contact[0]), message
        )
