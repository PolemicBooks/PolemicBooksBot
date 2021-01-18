import os

CWD = os.getcwd()

BOOKS_DIR = os.path.join(CWD, "files/books")
USERS_DIR = os.path.join(CWD, "files/users")
STRINGS_DIR = os.path.join(CWD, "files/strings")
PGPASS_DIR = os.path.join(CWD, "files/pgpass")

BOOKS_FILE = os.path.join(BOOKS_DIR, "books.json")
CATEGORIES_FILE = os.path.join(BOOKS_DIR, "categories.json")
AUTHORS_FILE = os.path.join(BOOKS_DIR, "authors.json")
NARRATORS_FILE = os.path.join(BOOKS_DIR, "narrators.json")
PUBLISHERS_FILE = os.path.join(BOOKS_DIR, "publishers.json")
TYPES_FILE = os.path.join(BOOKS_DIR, "types.json")

STRINGS_FILE = os.path.join(STRINGS_DIR, "strings.json")

# Configuração para o uso do pyrogram.
PYROGRAM_OPTIONS = {
	"session_name": "bot",
	"api_id": None,
	"api_hash": None,
	"bot_token": None,
	"workdir": os.path.join(CWD, "files/pyrogram"),
	"parse_mode": "markdown",
}

# Configuração para o uso do asyncpg.
ASYNCPG_OPTIONS = {
	"host": "127.0.0.1",
	"port": 5432,
	"user": None,
	"database": None,
	"password": None,
	"passfile": os.path.join(PGPASS_DIR, "pgpass"),
}
