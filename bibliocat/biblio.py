NOT_USED = 0
READING = 1
TRANSPORTING = 2


class Library:
	def __init__(self, idl, distances=None):
		if distances is None:
			distances = []
		self.id = idl
		self.books = []
		self.distances = distances

	def id_copy(self):
		my_lib = Library(self.id, self.distances)
		my_lib.books = [bk.id for bk in self.books]
		return my_lib

	def send_book(self, book, library, by_book_id=False):
		if book.library == self:
			if by_book_id:
				for i, elem in self.books:
					if elem.id == book:
						book = self.books.pop(i)
						break
			else:
				for i, elem in self.books:
					if elem.id == book.id:
						self.books.pop(i)
						break
			book.time = self.distances[library.id]
			book.status = TRANSPORTING
			book.destination = library
			return 0
		else:
			return -1

	def lend_book(self, book, reader, by_book_id=False):
		if book.library == self and reader.library_id == self.id:
			if by_book_id:
				for i, elem in self.books:
					if elem.id == book:
						book = self.books.pop(i)
						break
			else:
				for i, elem in self.books:
					if elem.id == book.id:
						self.books.pop(i)
						break
			reader.start_book(book)
			book.destination = self
			return 0
		else:
			return -1


class Book:
	def __init__(self, idb, value):
		self.id = idb
		self.value = value
		self.status = NOT_USED
		self.time = 0
		self.destination = None
		self.reader = None
		self.library = None

	def id_copy(self):
		my_book = Book(self.id, self.value)
		my_book.status = self.status
		my_book.time = self.time
		if self.destination is None:
			my_book.destination = None
		else:
			my_book.destination = self.destination.id
		if self.reader is None:
			my_book.reader = None
		else:
			my_book.reader = self.reader.id
		if self.library is None:
			my_book.library = None
		else:
			my_book.library = self.library.id
		return my_book

	def end_day(self):
		if self.time != 0:
			self.time -= 1
		if self.time == 0:
			if self.status == READING:
				self.status = NOT_USED
				self.destination.books.append(self)
				self.library = self.destination
				self.destination = None
				self.reader.end_book(self)
				return self.value
			else:
				self.status = NOT_USED
				self.destination.books.append(self)
				self.library = self.destination
				self.destination = None
				return 0

	def get_library(self, libraries):
		for lib in libraries:
			if self.id in [bk.id for bk in lib.books]:
				self.library = lib
				return lib
		return None


class Reader:
	def __init__(self, idr, idl):
		self.id = idr
		self.library_id = idl
		self.books = [None, None, None]
		self.book_times = {}

	def id_copy(self):
		my_reader = Reader(self.id, self.library_id)
		my_reader.book_times = self.book_times
		my_reader.books = []
		for book in self.books:
			if book is None:
				my_reader.books.append(None)
			else:
				my_reader.books.append(book.id)
		return my_reader

	def start_book(self, book):
		if self.can_start_book():
			for i, bk in enumerate(self.books):
				if bk is None:
					if book.status == NOT_USED:
						book.reader = self
						book.time = self.book_times[book.id]
						book.status = READING
						self.books[i] = book
						return 0
		return -1

	def end_book(self, book):
		for i, bk in enumerate(self.books):
			if bk is not None:
				if bk.id == book.id:
					self.books[i] = None
					return 0
		return -1

	def can_start_book(self):
		for bk in self.books:
			if bk is None:
				return True
		return False
