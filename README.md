# Divination Generator Microservice

Микросервис на FastAPI для генерации интерпретаций рунических раскладов с использованием ИИ.

## Установка

1.  Клонируйте репозиторий:
    ```bash
    git clone <your-repo-url>
    cd divination-generator
    ```
2.  Установите зависимости с помощью Poetry:
    ```bash
    poetry install
    ```
3.  Создайте файл `.env` из `.env.example` и укажите ваш API ключ:
    ```bash
    cp .env.example .env
    # Отредактируйте .env, указав ваш ключ
    ```

## Запуск

```bash
poetry run uvicorn app.main:app --reload
```

Сервис будет доступен по адресу `http://127.0.0.1:8000`. Документация API (Swagger UI) находится по адресу `http://127.0.0.1:8000/docs`.

## API

### POST /api/v1/divination/encode

**Запрос:**

```json
{
  "runes": ["Иса", "Лагуз", "Вуньо", "Йеро", "Ингуз", "Хагалаз"],
  "theme": "Карьера"
}
```

**Ответ:**

```json
{
  "interpretation": "Сгенерированное описание расклада..."
}
```
```

**5. `app/data/RuneExample.json`:**

Скопируйте содержимое файла `RuneExample.json`, который вы предоставили, в `app/data/RuneExample.json`. Я вижу только часть файла, скопируйте его полностью. Если он большой, можете пока ограничиться теми примерами, что видны.

**6. Python файлы:**

Пока оставьте все файлы `.py` пустыми (`__init__.py`, `main.py`, `schemas.py`, `endpoints/divination.py`, `config.py`, `models.py`). Мы наполним их на следующих шагах.

Пожалуйста, выполните эти шаги, и дайте мне знать, когда будете готовы продолжить с написанием кода FastAPI и логики ИИ.