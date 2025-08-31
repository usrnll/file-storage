# File Storage Service

Простой HTTP-сервис для хранения файлов с авторизацией.

## 

Сервис предоставляет следующие возможности:

- **Upload** — загрузка файлов авторизованным пользователем, хранение на диске по хэшу, запись в SQLite.
- **Download** — скачивание файлов по хэшу.
- **Delete** — удаление файлов авторизованным пользователем.
- **Health** — проверка состояния сервиса.

Авторизация пользователей реализована через **Basic Auth**. Регистрация не предусмотрена.

---

## Технологии

- Python 3.9
- Flask
- SQLite
- Хэширование: SHA256 

---

## Установка

1. Клонируйте репозиторий:

```bash
git clone https://github.com/usrnll/file-storage
cd file-storage
```
2. Создайте виртуальное окружение и активируйте:

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```
3. Установите зависимости:

```bash
pip install -r requirements.txt
```
## Запуск

```bash
python app.py
```
## Эндпоинты


### 1. Upload

```bash
POST /upload
```
- **Headers**: Basic Auth `(username:password)`
- **Body**: form-data `file=@имя_файла`
- **Response** — JSON с хэшем файла, размером, MIME и владельцем

**Примеры curl**

Файл внутри каталога проекта:
```bash
curl -u alice:password -F "file=@test.txt" http://127.0.0.1:8000/upload
```

### 2. Download

```bash
GET /download/<hash>
```

- Любой пользователь может скачать файл по его хэшу.

- Файл будет возвращён с именем хэша, но можно сохранить под любым именем.

**Примеры curl**

```bash
# Скачать с именем от сервера
curl -O -J http://127.0.0.1:8000/download/<file_hash>

# Скачать под своим именем
curl -o myfile.txt http://127.0.0.1:8000/download/<file_hash>
```

### 3. Delete

```bash
DELETE /delete/<hash>
```
- **Headers**: Basic Auth `(username:password)`
- Удаляет файл, если он принадлежит авторизованному пользователю.
- Если файл не найден или не принадлежит пользователю — возвращается 404.

**Примеры curl**

Файл внутри каталога проекта:
```bash
curl -u alice:password -X DELETE http://127.0.0.1:8000/delete/<file_hash>
```

### 4. Health

```bash
GET /health
```
- Проверка состояния сервиса.

**Примеры curl**

```bash
curl http://127.0.0.1:8000/health
```

## Примечания

- Файлы сохраняются в STORE_DIR в структуре по первым двум символам хэша:

```bash
store/ab/abcdef12345...
```
