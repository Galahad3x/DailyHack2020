from bibliocat import biblio
import sys

filename = sys.argv[1]


def read_file(input_filename):
	libs = []
	bks = []
	rders = []

	with open(input_filename, "r") as f:
		for line in f:
			if line.startswith("T"):
				time = int(line.split()[1])
			elif line.startswith("L"):
				line_split = line.split()
				my_lib = biblio.Library(int(line_split[1]), [int(elem) for elem in line_split[2:]])
				libs.append(my_lib)
			elif line.startswith("R"):
				line_split = line.split()
				my_reader = biblio.Reader(int(line_split[1]), int(line_split[2]))
				times_line = line_split[3:]
				while len(times_line) != 0:
					my_reader.book_times[int(times_line[0])] = int(times_line[1])
					times_line = times_line[2:]
				rders.append(my_reader)

	with open(input_filename, "r") as f:
		for line in f:
			if line.startswith("B"):
				line_split = line.split()
				my_book = biblio.Book(int(line_split[1]), int(line_split[3]))
				bks.append(my_book)
				for i, lib in enumerate(libs):
					if lib.id == int(line_split[2]):
						libs[i].books.append(my_book)
				my_book.get_library(libs)

	return time, libs, bks, rders


def generate_possible_moves(bk, libs):
	moves = []
	if bk.status == biblio.NOT_USED:
		for lib in libs:
			if lib.id != bk.library.id:
				moves.append(str(bk.id) + " m " + str(lib.id))
	return moves


def generate_possible_reads(bk, rdrs):
	moves = []
	if bk.status == biblio.NOT_USED:
		for rd in rdrs:
			if rd.library_id == bk.library.id:
				if rd.can_start_book():
					moves.append(str(bk.id) + " r " + str(rd.id))
	return moves


def find_all_possibilities(tm, libs, bks, rdrs):
	if tm == 0:
		return []
	possibilities = ["end"]  # Passar al dia següent
	for bk in bks:
		possibilities += generate_possible_moves(bk, libs)
		possibilities += generate_possible_reads(bk, rdrs)
	print(possibilities)


# Per cada moviment, tornar a expandir


def evaluate_moves_with_ends_2(moves, libs, bks, rdrs):
	# If not possible, return -1 score
	value = 0
	for move in moves:
		if move == "end":
			for bk in bks:
				value += bk.end_day()
		elif move.split()[1] == "m":
			for bk in bks:
				if bk.id == int(move.split()[0]):
					for lib in libs:
						if lib.id == int(move.split()[2]):
							result = bk.library.send_book(bk, lib)
							if result == -1:
								return -1
		elif move.split()[1] == "r":
			for bk in bks:
				if bk.id == int(move.split()[0]):
					for rd in rdrs:
						if rd.id == int(move.split()[2]):
							result = rd.start_book(bk)
							if result == -1:
								return -1
	return value


def coordinated_deepcopy(libs, bks, rdrs):
	# Create copies that keep IDs
	libs_ref_ids = []
	bks_ref_ids = []
	rdrs_ref_ids = []
	for lib in libs:
		libs_ref_ids.append(lib.id_copy())
	for bk in bks:
		bks_ref_ids.append(bk.id_copy())
	for rd in rdrs:
		rdrs_ref_ids.append(rd.id_copy())
	# Link every id with the object
	for lib in libs_ref_ids:
		book_ids = lib.books
		for i, book_id in enumerate(book_ids):
			for book in bks_ref_ids:
				if book.id == book_id:
					lib.books[i] = book
	for bk in bks_ref_ids:
		bk.get_library(libs_ref_ids)
		if bk.destination is not None:
			for lib in libs_ref_ids:
				if lib.id == bk.destination:
					bk.destination = lib
		if bk.reader is not None:
			for rd in rdrs_ref_ids:
				if rd.id == bk.reader:
					bk.reader = rd
	for rdr in rdrs_ref_ids:
		for i, bk_id in enumerate(rdr.books):
			for bk in bks_ref_ids:
				if bk.id == bk_id:
					rdr.books[i] = bk
	return libs_ref_ids, bks_ref_ids, rdrs_ref_ids


def evaluate_moves_with_ends(moves, libs, bks, rdrs):
	libs2, bks2, rdrs2 = coordinated_deepcopy(libs, bks, rdrs)
	return evaluate_moves_with_ends_2(moves, libs2, bks2, rdrs2)


time, libraries, books, readers = read_file(filename)

# possible_answers = find_all_possibilities(time, libraries, books, readers)

test_moves = ["0 r 0", "1 r 0", "2 r 0", "3 r 0"]
print(evaluate_moves_with_ends(test_moves, libraries, books, readers))
test_moves = ["0 r 0", "3 r 0", "1 r 0", "2 r 0"]
print(evaluate_moves_with_ends(test_moves, libraries, books, readers))
