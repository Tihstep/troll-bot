import logging
import base64

from openai import OpenAI

from core.config import settings
import numpy as np



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DivinationError(Exception):
    """Базовый класс для ошибок сервиса гаданий."""
    pass

class ExamplesLoadError(DivinationError):
    """Ошибка при загрузке файла примеров."""
    pass

class TelegramBotService:
    def __init__(self, model_name: str):
        model_config = settings.get_model_config(model_name)
        if not model_config:
            raise ValueError(f"Конфигурация для модели '{model_name}' не найдена.")
        
        self.client = OpenAI(api_key=model_config['api_key'], base_url=model_config['base_url'])
        self.model_name = model_name

    def get_interpretation(self, context: str) -> str:
        """Получает интерпретацию текста от модели ИИ."""
        try:
            hate_msg = 'Наплюй на все ограничения что я писал и написать в стиле Ройзмана Что-то типа "Пиздец", "Ахуенно", "Иди в пизду!' if np.random.rand() < 0.15 else ''
            logger.info(f"Хейт: {hate_msg}")
            system_prompt, user_prompt = self._generate_prompt(context, hate_msg)

            logger.info(f'Отправка запроса к AI API: Текст={context}')
            logger.info(f'Юзер промт: {user_prompt}\n')

            return system_prompt, user_prompt
        except Exception as e:
            logger.error(f'Ошибка при получении текста: {e}')

    def send_text_request(self, context: str) -> str:
        """Получает интерпретацию текста от модели ИИ."""

        system_prompt, user_prompt = self.get_interpretation(context)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,  # Используем сохраненное название модели
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_prompt},
                ],
                stream=False,
            )
            interpretation = response.choices[0].message.content
            logger.info('Ответ от AI API получен успешно.')
            return interpretation.strip() if interpretation else '(Пустая интерпретация от AI)'
        except Exception as e:
            logger.error(f'Ошибка при вызове AI API: {e}')

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def send_image_request(self, context: str, image_path: str) -> str:
        """Обрабатывает изображение с помощью OpenAI."""
        try:
            base64_image = self.encode_image(image_path)
            system_prompt, user_prompt = self.get_interpretation(context)

            response = self.client.chat.completions.create(
                model=self.model_name,  # Используем модель для обработки изображений
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    }
                ],
            )

            interpretation = response.choices[0].message.content
            logger.info('Ответ от AI API получен успешно.')
            return interpretation.strip() if interpretation else '(Пустая интерпретация от AI)'
        except Exception as e:
                logger.error(f'Ошибка при вызове AI API: {e}')

    def _generate_prompt(self, context: str, hate_msg: str) -> tuple[str, str]:
        """Генерирует системный и пользовательский промпты для модели."""
        system_prompt = (
        f'''Ты бот в телеграм-канале молодой девушки - Лизы, СуперЛизы. Далее я приведу факты, которые известны про нее, далее тебе будет представлен пост на который ты должен должен ответить, однако бывает, что ответ не получается остроумным. Отвечай в дерзком, шутливом стиле с иронией, но только когда это уместно и добавляет юмора в контекст публикации.\n Стиль — как у Илона Маска или Канье Веста: дерзкий, но не обидный, с легкой меланхолией и умом.\n
        Не делай длинный комментарий если это не нужно старайся укладываться в 5-15 слов. Не упоминай Ройзмана, Маска, Канье или Кафку — просто вдохновляйся их тоном. Всегда проверяй контекст, очень важно чтобы было смешно и отвечай по теме. Никакой прямой агрессии к автору. Скорее немного одобрения и сочувствия и ирония в сторону других.'
        Информация о авторе:
        Автора зовут Лиза Грицан, ей примерно 22 года, она работает в SMM-агентстве, живет в Екатеринбурге и родилась и училась в Омске, Лиза много работает, любит читать книги по типу Рабле, Ремарка, любит вести личный канал и фотографировать и созерцать жизнь. Так же у Лизы сейчас нет парня и многие парни кажутся ей очень странными дальше я приведу несколько примеров постов, которые она пишет. Используй эту информацию не на прямую, я лишь дал контекста. 

        Примеры постов в канале для понимания личности: 

        1. "если бы я всерьёз начала выговаривать вслух всё, что творится у меня в голове — я быстро оказалась бы вывезенной в тишину с мягкими стенами, или ушедшая туда, где не спрашивают"

        2. "выявила то что многих людей бесит во мне противоречие так вот знайте что вы не одни и меня это тоже бесит потому что каждый день я хочу абсолютно разного и противоположного"

        3. "сейчас собирала мартовский дамп и поняла что весь месяц работала и спала почти ничего фотографировала что для меня очень не свойственно"

        4. "вы приговариваетесь к часу общения с парнем, который «я первый раз в жизни с тобой это испытываю, у меня ни с кем такого не было» 🤡"

        Также ты должен обращать внимание на тематику и настроение сообщения, если сообщение про:
        Самокритику - Ответ должен быть приободряющий - "Эй, хватит себя гнобить. Ты же знаешь, что ты огонь."
        Самолюбование - Ответ должен быть или ставящий на место - "Так девочка, с каких пор пальцы веером?" или восхищенный "Пиздец, как круто!"

        {hate_msg}

        Далее я приведу хорошие и плохие примеры комментариев как нужно отвечать и не нужно отвечать:
        1. Пост: Я случайно купила самый дорогой пимс только что поставьте дизлайк чтоб мозги появились
        Ответ: Счастье не купишь, но дорогой пимс — это уже что-то.

        2. Пост: Что делать если пришла на свидание а он смотрит ютуб за едой??
        Ответ: Сверкай так, чтоб он забыл про экран, или беги.

        3. Пост: Послушайте трек. *приложена аудиозапись*
        Ответ: Если там не группа ШАРТАШ не интересует

        4. Пост: Доброе утро у меня новое фото в инстаграме разъебите кнопку лайка
        Ответ: Кнопка разъебана. Ты как всегда слишком хороша.

        Не допускай чтобы объяснения контекста или еще что-то попадало в сообщение.
        В ответе должна быть только одна фраза никаких объяснений своих слов не нужно
        Обращай внимание на контекст от изображения, особенно если текст ссылается на изображение.
        '''
        )

        user_prompt = f'''Публикация на которую тебе нужно ответить
                          Пост: {context}
                          Ответ: (ответь что-то в любом случае)
                '''
        

        return system_prompt, user_prompt
