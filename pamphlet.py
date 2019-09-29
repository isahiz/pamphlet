#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import re
import time
import io

def main():
	outname = "none"
	inxls = "none"
	imgdr = "none"
	for i in range(1, len(sys.argv), 2):
		if sys.argv[i] == '-o':
			outname = sys.argv[i + 1]
		elif sys.argv[i] == "-ix":
			inxls = sys.argv[i + 1]
		elif sys.argv[i] == "-img":
			imgdr = sys.argv[i + 1]

	infile = open(inxls, 'r')
	outfile = open(outname, 'w')


if __name__ == '__main__':
	main()