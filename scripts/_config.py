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

CHAT_ID = -1001436494509

FALLBACK_CHAT = -1001341909754
COVER_MESSAGE_ID = 2
