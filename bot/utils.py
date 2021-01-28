from typing import List
import unicodedata
import os

from pyrogram.types import InputMediaDocument

from .types.books_and_documents import Book


# Esta função é usada para gerar o texto ou legenda de um livro.
def create_caption(book: Book) -> str:
	
	caption = ""
	
	if book.title:
		caption += f"**{book.title.original}**\n\n"
	if book.type:
		caption += f"**Tipo**: __{book.type.original}__\n"
	if book.category:
		caption += f"**Categoria**: __{book.category.original}__\n"
	if book.duration:
		caption += f"**Duração**: __{book.duration.human}__\n"
	if book.size:
		caption += f"**Tamanho**: __{book.size.human}__\n"
	if book.author:
		caption += f"**Autor**: __{book.author.original}__\n"
	if book.narrator:
		caption += f"**Narrador**: __{book.narrator.original}__\n"
	if book.publisher:
		caption += f"**Editora**: __{book.publisher.original}__\n"
	
	return caption


# Este método é usado para criar um grupo de documentos a serem enviados.
def create_media_group(book: Book) -> List[InputMediaDocument]:
	
	group = []
	
	caption = f"**{book.type.original}**: {book.title.original}"
	
	for document in book.documents:
		group.append(InputMediaDocument(document.file_id, caption=caption))
	
	return group


