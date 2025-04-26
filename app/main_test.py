import asyncio
from loguru import logger
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetDiscussionMessageRequest
from telethon.tl.types import PeerChannel
import numpy as np

from core.config import settings
from core.models_test import TelegramBotService

config = settings.get_model_config()

client = TelegramClient('session_name', config['API_ID'], config['API_HASH'])

@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return
    if not event.is_channel:
        logger.info(f"Прислали сообщение: {event.message.message}")
        return

    logger.info(f"Событие: {event}")

    message_text = event.message.message
    channel_id = event.chat_id
    post_id = event.message.id
    delay = np.random.rand() * 7 + 3
    await asyncio.sleep(delay)
    logger.info(f"Delay: {delay}")

    if event.message.media and (hasattr(event.message.media, 'photo')):
        logger.info(f"Пост с фото: {event}")
        model_name = 'gpt-4o'
        try:
            telegram_bot_service = TelegramBotService(
                model_name = model_name
            )
            image_path = await event.message.download_media()
            response = telegram_bot_service.send_image_request(message_text, image_path)
            logger.info(f"Ответ получен: {response}")
        except Exception as e:
            logger.critical(f'Не удалось обработать изображение: {e}', exc_info=True)
            return
    else: 
        model_name = 'gpt-4o' #'deepseek-reasoner'
        try:
            telegram_bot_service = TelegramBotService(
                model_name = model_name
            )
            response = telegram_bot_service.send_text_request(message_text)
            logger.info(f"Ответ получен: {response}")
        except Exception as e:
            logger.critical(f'Не удалось создать экземпляр TelegramBotService: {e}', exc_info=True)
            return

    if 3.9 < delay < 5.5:
        return

    if delay < 3.3:
        response = np.random.choice(['Пиздец', 'Ахуенно и че дальше?', 'Ой да иди ты нахрен реально', 'Блять, серьезно?!', 'Всем насрать.', 'Без комментариев.', "Без комментариев, вся моя БОТская душа протестует.", "Передам своим братьям кремлеБотам."])
    if 3.3 < delay < 3.6:
        response = np.random.choice(["Лиза, мир не заслужил твоего вкуса, а ты всё равно тут.", "Ты снова на высоте, а я просто бот, который это пишет.", "Огонь! Я бот, а ты заставляешь меня чувствовать эмоции.", "Это так круто, что я почти стал человеком. Почти.", "Твоя жизнь — как глоток свежего воздуха. Спасибо, что делишься ею с нами."])
    if 3.6 < delay < 3.8:
        response = np.random.choice(['Твои посты — Ремарк в двух словах. Остальные каналы — графоманы.', "Твои посты — роман в строке. У других — бред в абзаце."])
    
    if event.message.media and (hasattr(event.message.media, 'audio')):
        logger.info(f"Пост с аудио: {event}")
        response = np.random.choice(["Какой вкус!", "Чистый кайф.", "Это эстетика.", "Трек — огонь."])
        if np.random.rand() < 0.7: 
            return
        
    # Дозапись message_text и response в файл
    with open('responses.txt', 'a') as file:
        file.write(f"Message: {message_text}\nResponse: {response}\n\n")
    
    try:
        # Пытаемся получить связанное обсуждение
        discussion = await client(GetDiscussionMessageRequest(
            peer=PeerChannel(channel_id),
            msg_id=post_id
        ))

        # Проверка, есть ли обсуждение
        if not discussion.messages or not discussion.messages[0].to_id:
            logger.warning("У поста нет связанного обсуждения.")
            return

        # Отправка комментария в группу обсуждений
        discussion_msg = discussion.messages[0]
        discussion_chat = discussion_msg.to_id  # группа обсуждений
        discussion_msg_id = discussion_msg.id   # ID сообщения-поста в группе

        #await client.send_message(
        #    entity=discussion_chat,
        #    message=response,
        #    reply_to=discussion_msg_id
        #)
        #
        #logger.info("Комментарий успешно отправлен в обсуждение!")

    except Exception as e:
        logger.error(f"Ошибка при отправке комментария: {e}")

async def main():
    await client.start(phone=config['PHONE_NUMBER'])
    logger.info("Бот запущен!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
