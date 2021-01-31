import json
import time
import os

from pyrogram import Client
from unidecode import unidecode

from _config import *
from _core import *
from _utils import *

books = []

message_id = 0

book = {}

client = Client(**PYROGRAM_OPTIONS)
client.start()

FALLBACK_COVER = {
	"file_id": client.get_messages(FALLBACK_CHAT, COVER_MESSAGE_ID).photo.file_id
}

while message_id < 145000:
	
	message_id += 1
	
	# Essas mensagens não são publicações de livros
	if message_id in (2, 10596, 10597, 13337, 131117, 134378, 134379):
		continue
	
	message = client.get_messages(CHAT_ID, message_id)
	
	if message.empty or message.service:
		continue
	
	if message.photo and message.caption:
		if book:
			books.append(book)
		
		book_title = message.caption.split(sep="\n")[0]
		
		author, publisher, book_type, category, narrator, duration, year, chapters = (
			get_author(message.caption.markdown),
			get_publisher(message.caption.markdown),
			get_book_type(message.caption.markdown),
			get_category(message.caption.markdown),
			get_narrator(message.caption.markdown),
			get_duration(message.caption.markdown),
			get_year(message.caption.markdown),
			get_chapters(message.caption.markdown),
		)
		
		book = {
			"message": message.message_id,
			"title": book_title,
			"type": book_type,
			"category": category,
			"duration": None if book_type != "Audiobook" else human_duration_to_seconds(message.caption.markdown),
			"size": 0,
			"author": author,
			"narrator": narrator,
			"publisher": publisher,
			"year": year,
			"chapters": chapters,
			"photo": {
				"file_id": message.photo.file_id
			},
			"documents": [],
		}
		
		continue
		
	if message.text:
		if book:
			books.append(book)
		
		book_title = message.text.split(sep="\n")[0]
		
		author, publisher, book_type, category, narrator, duration, year, chapters = (
			get_author(message.text.markdown),
			get_publisher(message.text.markdown),
			get_book_type(message.text.markdown),
			get_category(message.text.markdown),
			get_narrator(message.text.markdown),
			get_duration(message.text.markdown),
			get_year(message.text.markdown),
			get_chapters(message.text.markdown),
		)
		
		book = {
			"message": message.message_id,
			"title": book_title,
			"type": book_type,
			"category": category,
			"duration": None if book_type != "Audiobook" else human_duration_to_seconds(message.text.markdown),
			"size": 0,
			"author": author,
			"narrator": narrator,
			"publisher": publisher,
			"year": year,
			"chapters": chapters,
			"photo": FALLBACK_COVER,
			"documents": []
		}
		
		continue
	
	if message.document:
		document = {
			"file_id": message.document.file_id
		}
		
		book["size"] += message.document.file_size
		
		book["documents"].append(document)
	
	print(json.dumps(book, indent=4))

books.append(book)

categories, types, authors, narrators, publishers, years = (
	[], [], [], [], []
)

for book in books:
	category, book_type, author, narrator, publisher, year = (
		None if book["category"] is None else book["category"],
		None if book["type"] is None else book["type"],
		None if book["author"] is None else book["author"],
		None if book["narrator"] is None else book["narrator"],
		None if book["publisher"] is None else book["publisher"],
		None if book["year"] is None else book["year"]
	)
	
	if category and category not in categories:
		categories.append(category)
	
	if book_type and book_type not in types:
		types.append(book_type)
	
	if author and author not in authors:
		authors.append(author)
	
	if narrator and narrator not in narrators:
		narrators.append(narrator)

	if publisher and publisher not in publishers:
		publishers.append(publisher)
	
	if year and year not in years:
		years.append(year)

with open(file=os.path.join(BOOKS_DIRECTORY, "categories.json"), mode="w") as file:
	file.write(json.dumps(categories))

with open(file=os.path.join(BOOKS_DIRECTORY, "types.json"), mode="w") as file:
	file.write(json.dumps(types))

with open(file=os.path.join(BOOKS_DIRECTORY, "authors.json"), mode="w") as file:
	file.write(json.dumps(authors))

with open(file=os.path.join(BOOKS_DIRECTORY, "narrators.json"), mode="w") as file:
	file.write(json.dumps(narrators))

with open(file=os.path.join(BOOKS_DIRECTORY, "publishers.json"), mode="w") as file:
	file.write(json.dumps(publishers))

with open(file=os.path.join(BOOKS_DIRECTORY, "years.json"), mode="w") as file:
	file.write(json.dumps(years))

with open(file=os.path.join(BOOKS_DIRECTORY, "books.json"), mode="w") as file:
	file.write(json.dumps(books))

