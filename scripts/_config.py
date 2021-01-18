import os
from pathlib import Path

CWD = Path(os.getcwd())

BOOKS_DIRECTORY = os.path.join(str(CWD.parent), "files/books")

PYROGRAM_OPTIONS = {
	"session_name": "bot",
	"api_id": None,
	"api_hash": None,
	"bot_token": None,
	"workdir": os.path.join(str(CWD)), "files/pyrogram"),
	"no_updates": True,
}

