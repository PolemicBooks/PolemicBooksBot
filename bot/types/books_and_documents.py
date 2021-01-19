from typing import Union, List, Any
from itertools import zip_longest
import random

from asyncpg.connection import Connection

from .utils import remove_accents


class Book:
	"""Objeto representando informações sobre um livro."""
	def __init__(self, book: dict) -> None:
		
		if book["title"]:
			book["title"] = Title(book["title"])
		
		if book["category"]:
			book["category"] = Category(book["category"])
		
		if book["type"]:
			book["type"] = Type(book["type"])
		
		if book["author"]:
			book["author"] = Author(book["author"])
		
		if book["narrator"]:
			book["narrator"] = Narrator(book["narrator"])
		
		if book["publisher"]:
			book["publisher"] = Publisher(book["publisher"])
		
		if book["duration"]:
			book["duration"] = Duration(book["duration"])
		
		book["size"] = Size(book["size"])
		book["date"] = Date(book["date"])
		
		if book["photo"]:
			book["photo"]["date"] = Date(book["photo"]["date"])
			book["photo"]["file_size"] = Size(book["photo"]["file_size"])
			book["photo"]["resolution"] = Resolution(book["photo"]["resolution"])
			
			book["photo"] = Cover(book["photo"])
		
		documents = []
		
		for document in book["documents"]:
			document["date"] = Date(document["date"])
			document["file_size"] = Size(document["file_size"])
			
			document = Document(document)
			documents.append(document)
		
		book["documents"] = documents
		
		self.__dict__.update(book)


class Narrator:
	"""Objeto representando informações sobre o narrador de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Type:
	"""Objeto representando informações sobre o tipo de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Publisher:
	"""Objeto representando informações sobre a editora de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)

class Author:
	"""Objeto representando informações sobre o autor de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Category:
	"""Objeto representando informações sobre a categoria de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Title:
	"""Objeto representando informações sobre o título de um livro."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Duration:
	"""Objeto representando a duração total de um audiobook."""
	def __init__(self, duration: dict) -> None:
		self.__dict__.update(duration)


class Size:
	"""Objeto representando o tamanho de um documento ou imagem."""
	def __init__(self, size: dict) -> None:
		self.__dict__.update(size)


class Cover:
	"""Objeto representando informações sobre o cover de um livro."""
	def __init__(self, cover: dict) -> None:
		self.__dict__.update(cover)


class Date:
	"""Objeto representando a data de adição de um livro."""
	def __init__(self, date: dict) -> None:
		self.__dict__.update(date)


class Resolution:
	"""Objeto representando as resoluções de uma imagem."""
	def __init__(self, resolution: dict) -> None:
		self.__dict__.update(resolution)


class Document:
	"""Objeto representando informações sobre um documento."""
	def __init__(self, document: dict) -> None:
		self.__dict__.update(document)


class Library:
	"""Objeto representando informações sobre vários livros."""
	def __init__(self, categories: dict, authors: dict, narrators: dict, publishers: dict, types: dict) -> None:
		self.books = []
		self.categories = categories
		self.authors = authors
		self.narrators = narrators
		self.publishers = publishers
		self.types = types
		
		# Ordenar todos os itens das listas em ordem alfabética.
		self.categories.sort()
		self.authors.sort()
		self.narrators.sort()
		self.publishers.sort()
		self.types.sort()
	
	
	# Este método é usado para obter uma lista de todas as categorias disponíveis.
	def get_categories(self):
		return self.create_pagination(list(enumerate(self.categories)), fillvalue=(None, None))
	
	
	# Este método é usado para obter uma lista de todas os autores disponíveis.
	def get_authors(self):
		return self.create_pagination(list(enumerate(self.authors)), fillvalue=(None, None))
	
	
	# Este método é usado para obter uma lista de todas os narradores disponíveis.
	def get_narrators(self):
		return self.create_pagination(list(enumerate(self.narrators)), fillvalue=(None, None))
	
	
	# Este método é usado para obter uma lista de todas as editoras disponíveis.
	def get_publishers(self):
		return self.create_pagination(list(enumerate(self.publishers)), fillvalue=(None, None))
	
	
	# Este método é usado para obter uma lista de todas os tipos disponíveis.
	def get_types(self):
		return self.create_pagination(list(enumerate(self.types)), fillvalue=(None, None))
	
	
	# Este método é usado para obter um livro aleatório da lista.
	def get_random(self) -> Book:
		book = random.choice(self.books)
		
		# Livros semi capa não são escolhidos
		while not book.photo:
			book = random.choice(self.books)
		
		return book
	
	
	# Este método é usado para adicionar livros a lista.
	def append(self, book: Book) -> None:
		self.books.append(book)
	
	
	# Este método é usado para obter um livro específico da lista.
	# Os livros são distinguidos usando o ID númerico da mensagem
	# correspondente enviada no canal Telegram.
	def get(self, message_id: int) -> Union[None, Book]:
		
		for book in self.books:
			if book.id == message_id:
				return book
	
	
	# Este método é usado para obter livros de um determinado tipo, autor, editora e entre outros.
	def get_books(self, category: str = int, author: str = int, narrator: str = int, publisher: str = int, book_type: str = int) -> List[Book]:
		
		results = []
		
		if isinstance(category, int):
			category_name = self.categories[category]
			for book in self.books:
				if book.category and book.category.original == category_name:
					results.append(book)
			return self.create_pagination(results)
		
		if isinstance(author, int):
			author_name = self.authors[author]
			for book in self.books:
				if book.author and book.author.original == author_name:
					results.append(book)
			return self.create_pagination(results)
		
		if isinstance(narrator, int):
			narrator_name = self.narrators[narrator]
			for book in self.books:
				if book.narrator and book.narrator.original == narrator_name:
					results.append(book)
			return self.create_pagination(results)
		
		if isinstance(publisher, int):
			publisher_name = self.publishers[publisher]
			for book in self.books:
				if book.publisher and book.publisher.original == publisher_name:
					results.append(book)
			return self.create_pagination(results)
		
		if isinstance(book_type, int):
			type_name = self.types[book_type]
			for book in self.books:
				if book.type and book.type.original == type_name:
					results.append(book)
			return self.create_pagination(results)
	
	
	# Este método é usado para pesquisar por livros.
	def search(self, query: str) -> Union[None, List[Union[Book, None]]]:
		search_results = []
		
		# Aqui convertemos todos os caracteres para minúsculo e removemos os acentos.
		query = remove_accents(query.lower())
		
		# Aqui separamos cada palavra com mais de 2 caracteres em uma lista.
		splited_query = [
			word for word in query.split() if len(word) > 2
		]
		
		for book in self.books:
			if book.title:
				if query in book.title.ascii_lower:
					search_results.append(book)
				elif all(word in book.title.ascii_lower for word in splited_query):
					search_results.append(book)
			
			if book.type:
				if query in book.type.ascii_lower:
					search_results.append(book)
				elif all(word in book.type.ascii_lower for word in splited_query):
					search_results.append(book)
			
			if book.category:
				if query in book.category.ascii_lower:
					search_results.append(book)
				elif all(word in book.category.ascii_lower for word in splited_query):
					search_results.append(book)
			
			if book.author:
				if query in book.author.ascii_lower:
					search_results.append(book)
				elif all(word in book.author.ascii_lower for word in splited_query):
					search_results.append(book)
			
			if book.narrator:
				if query in book.narrator.ascii_lower:
					search_results.append(book)
				elif all(word in book.narrator.ascii_lower for word in splited_query):
					search_results.append(book)
			
			if book.publisher:
				if query in book.publisher.ascii_lower:
					search_results.append(book)
				elif all(word in book.publisher.ascii_lower for word in splited_query):
					search_results.append(book)
		
		if search_results:
			return self.create_pagination(search_results)
	
	
	# Este método é usado para criar uma lista contendo tuples de até 10 livros.
	def create_pagination(self, items: list, fillvalue: Any = None) -> List[Union[Book, None]]:
		return list(zip_longest(*[iter(items)] * 10, fillvalue=fillvalue))


class UserLibrary:
	"""Um objeto representando uma listas contendo livros de um usuário."""
	def __init__(self, index: int, conn: Connection, user_id: int, read: list, reading: list, dropped: list, favorites: list) -> None:
		self.index = index
		self.conn = conn
		self.user_id = user_id
		self.read = read
		self.reading = reading
		self.dropped = dropped
		self.favorites= favorites
	
	
	# Este método é usado para obter uma lista de livros específica do usuário.
	def get_list(self, category: Union[str, int]) -> Union[List[int], None]:
		
		if category in (1, "read"):
			return self.read if self.read else None
		
		if category in (2, "reading"):
			return self.reading if self.reading else None
		
		if category in (3, "dropped"):
			return self.dropped if self.dropped else None
		
		if category in (4, "favorites"):
			return self.favorites if self.favorites else None
	
	
	# Este método é usado para verificar se o usuário possui um determinado
	# livro em uma de suas listas.
	def has(self, book: Book, category: Union[str, int] = None) -> bool:
		if category is None:
			return (
				book.id in self.read or
				book.id in self.reading or
				book.id in self.dropped or
				book.id in self.favorites
			)
		
		if category in (1, "read"):
			return (book.id in self.read)
		
		if category in (2, "reading"):
			return (book.id in self.reading)
		
		if category in (3, "dropped"):
			return (book.id in self.dropped)
		
		if category in (4, "favorites"):
			return (book.id in self.favorites)
	
	
	# Este método é usado para adicionar um livro a uma das listas
	# do usuário.
	def add(self, book: Book, category: Union[str, int]) -> None:
		if self.has(book, category):
			return
		
		if category in (1, "read"):
			self.read.append(book.id)
		elif category in (2, "reading"):
			self.reading.append(book.id)
		elif category in (3, "dropped"):
			self.dropped.append(book.id)
		elif category in (4, "favorites"):
			self.favorites.append(book.id)
	
	
	# Este método é usado para remover um livro de uma das listas
	# do usuário.
	def remove(self, book: Book, category: Union[str, int] = None) -> None:
		if not self.has(book, category):
			return
			
		if category is None:
			if book.id in self.read:
				self.read.remove(book.id)
			elif book.id in self.reading:
				self.reading.remove(book.id)
			elif book.id in self.dropped:
				self.dropped.remove(book.id)
			return
		
		if category in (1, "read"):
			if book.id in self.read:
				self.read.remove(book.id)
		elif category in (2, "reading"):
			if book.id in self.reading:
				self.reading.remove(book.id)
		elif category in (3, "dropped"):
			if book.id in self.dropped:
				self.dropped.remove(book.id)
		elif category in (4, "favorites"):
			if book.id in self.favorites:
				self.favorites.remove(book.id)
	
	
	# Este método é usado para atualizar a row do usuário.
	# Deve ser chamado sempre que uma das listas sofrer modificações.
	async def refresh(self) -> None:
		command = """
			UPDATE users
			SET read = $1,
					reading = $2,
					dropped = $3,
					favorites = $4
			WHERE user_id = $5
		"""
		
		async with self.conn.transaction() as transaction:
			await self.conn.execute(
				command,
				self.read,
				self.reading,
				self.dropped,
				self.favorites,
				self.user_id
			)
	
	
	# Este método é usado para deletar a row do usuário.
	async def delete(self) -> None:
		command = """
			DELETE FROM users
			WHERE user_id = $1
		"""
		
		async with self.conn.transaction() as transaction:
			await self.conn.execute(command, self.user_id)
	
		