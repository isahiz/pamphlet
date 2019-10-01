import sys
import os
import re
import time
import io
import csv

def begin_document(out, imgdir):
	out.write("\\documentclass{article}\n")
	out.write("\\usepackage[T1]{fontenc}\n")
	out.write("\\usepackage[tableposition=top]{caption}\n")
	out.write("\\usepackage{tabularx, makecell}\n")
	out.write("\\usepackage{tikz}\n")
	out.write("\\usepackage{graphicx}")

	out.write("\n\\newcolumntype{a}{>{\hsize=0.3\hsize}X}\n\\newcolumntype{b}{>{\hsize=0.7\hsize}X}\n")

	out.write("\\graphicspath{{"+ imgdir +"/}}")

	out.write("\n\\begin{document}")

def end_document(out):
	out.write("\\end{document}\n")

def begin_table(out):
	out.write("\\begin{table}[!ht]\n")
	out.write("\\caption{Table caption}\n")
	out.write("\\makebox[\\linewidth] {\n")
	out.write("\\begin{tabularx}{7in}{|a|b|a|b|} \\hline\n\\")

def end_table(out):
	out.write("\\end{tabularx}\n")
	out.write("}\n")
	out.write("\\end{table}\n")

def get_clean_text(s):
	return re.sub(r'[^\x00-\x7f]+','', s)

def clean_path(s):
	s = s.replace(" ", "")
	s = s.replace("\\", "/")
	return s

def write_table(incsv, imgdir, out):
	with open(incsv) as csvfile:
		readcsv = csv.reader(csvfile, delimiter=',')
		column_limit = 2
		column_count = 0
		println = ""
		for row in readcsv:
			column_count += 1
			lastname = get_clean_text(row[0])
			firstname = row[1]
			extratxt = row[2]
			img_filename = clean_path(imgdir) + "/" + firstname + lastname + ".jpg"
			println += "\\makecell[l]{"
			println += "\\resizebox{1in}{1in}{"
			println += "\\begin{tikzpicture}\n" + "\\node[anchor=south west,inner sep=0] at (0,0) {\\includegraphics[width=\\textwidth]{" + img_filename + "}};\n" + "\\end{tikzpicture}}}\n" 
			println += "& \\makecell[l]{ \\\\" + firstname + " " + lastname + "\\\\" + extratxt + "}\n" #designation information can go here
			if column_count == column_limit:
				column_count = 0
				println += "\\\\ \\hline\n"
			else:
				println += " & "
		if column_count < 2:
			println = println[1: -1 * len(" & ")] + " & & " + "\\\\ \\hline\n"
		out.write(println)

def make_pdf(f):
	os.system("pdflatex -output-directory=" + os.getcwd() + " " + f)

# run `pamphlet.py -ic [csv file name] -o [output.tex] -img [directory images for file]`
def main():
	outname = "none"
	incsv = "none"
	imgdir_name = "none"
	pdf = False 
	for i in range(1, len(sys.argv), 2):
		if sys.argv[i] == '-o':
			outname = sys.argv[i + 1]
		elif sys.argv[i] == "-ic":
			incsv = sys.argv[i + 1]
		elif sys.argv[i] == "-img":
			imgdir_name = sys.argv[i + 1]
		elif sys.argv[i] == "-pdf":
			pdf = True if sys.argv[i + 1] == str.lower("t") else False

	outfile = open(outname, 'w')

	begin_document(outfile, imgdir_name)
	begin_table(outfile)
	write_table(incsv, os.path.abspath(imgdir_name), outfile)
	end_table(outfile)
	end_document(outfile)

	outfile.close()
	if pdf:
		make_pdf(outname)

if __name__ == '__main__':
	main()