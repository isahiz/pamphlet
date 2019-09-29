import sys
import os
import re
import time
import io
import csv

def begin_document(out):
	out.write("\\documentclass{article}\n")
	out.write("\\usepackage[T1]{fontenc}\n")
	out.write("\\usepackage[tableposition=top]{caption}\n")
	out.write("\\usepackage{tabularx}\n")
	out.write("\\usepackage{tikz}\n")

	out.write("\n\\newcolumntype{a}{>{\hsize=0.3\hsize}X}\n\\newcolumntype{b}{>{\hsize=0.7\hsize}X}\n")

	out.write("\n\\begin{document}")

def end_document(out):
	out.write("\\end{document}\n")

def begin_table(out):
	out.write("\\begin{table}[!ht]\n")
	out.write("\\caption{Table caption}\n")
	out.write("\\makebox[\\linewidth] {\n")
	out.write("\\begin{tabularx}{7in}{|a|b|a|b|} \\hline\n")

def end_table(out):
	out.write("\\end{tabularx}\n")
	out.write("}\n")
	out.write("\\end{table}\n")

def write_table(incsv, imgdir, out):
	with open(incsv) as csvfile:
		readcsv = csv.reader(csvfile, delimiter=',')
		column_limit = 2
		column_count = 1
		for row in readcsv:
			lastname = row[0]
			firstname = row[1]
			extratxt = row[2]
			img_filename = imgdir + "/" + lastname + "_" + firstname + ".jpg"
			out.write("\\begin{tikzpicture}\n")
			out.write("\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics[width=\\textwidth]{" + img_filename + "}};\n")
			out.write("\\end{tikzpicture}\n")
			out.write(" & ")
			out.write(firstname + " " + lastname + "\n")
			if column_count == 2:
				out.write("\\\\ \\hline\n")
				column_count = 1
			else:
				out.write(" & ")
				column_count += 1

		if column_count == 1:
			out.write("\\\\ \\hline\n")

def main():
	outname = "none"
	incsv = "none"
	imgdir_name = "none"
	for i in range(1, len(sys.argv), 2):
		if sys.argv[i] == '-o':
			outname = sys.argv[i + 1]
		elif sys.argv[i] == "-ic":
			incsv = sys.argv[i + 1]
		elif sys.argv[i] == "-img":
			imgdir_name = sys.argv[i + 1]

	outfile = open(outname, 'w')

	begin_document(outfile)
	begin_table(outfile)
	write_table(incsv, imgdir_name, outfile)
	end_table(outfile)
	end_document(outfile)

if __name__ == '__main__':
	main()