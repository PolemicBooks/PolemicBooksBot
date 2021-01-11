import os

BASE_DIR = os.path.dirname(os.getcwd())

BOOKS_DIRECTORY = os.path.join(BASE_DIR, "files/books")

PYROGRAM_OPTIONS = {
	"session_name": "bot",
	"api_id": "",
	"api_hash": "",
	"bot_token": "",
	"workdir": os.path.join(BASE_DIR, "files/pyrogram"),
	"parse_mode": "markdown",
}

