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

	def send_book(self, book, library, by_book_id=False):
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

	def lend_book(self, book, reader, by_book_id=False):
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


class Book:
	def __init__(self, idb, value):
		self.id = idb
		self.value = value
		self.status = NOT_USED
		self.time = 0
		self.destination = None
		self.reader = None

	def end_day(self):
		if self.time != 0:
			self.time -= 1
		if self.time == 0:
			if self.status == READING:
				self.status = NOT_USED
				self.destination.books.append(self)
				self.destination = None
				self.reader.end_book(self)
				return self.value
			else:
				self.status = NOT_USED
				self.destination.books.append(self)
				self.destination = None
				return 0


class Reader:
	def __init__(self, idr, idl):
		self.id = idr
		self.library_id = idl
		self.books = [None, None, None]
		self.book_times = {}

	def start_book(self, book):
		for i, bk in enumerate(self.books):
			if bk is None:
				book.reader = self
				book.time = self.book_times[book.id]
				book.status = READING
				self.books[i] = book

	def end_book(self, book):
		for i, bk in enumerate(self.books):
			if bk is not None:
				if bk.id == book.id:
					self.books[i] = None
