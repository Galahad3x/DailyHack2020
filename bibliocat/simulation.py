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

	return time, libs, bks, rders


time, libraries, books, readers = read_file(filename)

print(libraries)
