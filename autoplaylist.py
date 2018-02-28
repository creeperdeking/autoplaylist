#!/usr/bin/env python3

import os
import pdb
import random
import sys

import consoleUI
import playlistUtils as utils

#Command arguments
def main():
	if len(sys.argv) < 2:
		consoleUI.consoleUI()
	else:
		if sys.argv[1] == "--help":
			print("Help page for autoplaylist :")
			print("  syntax: autoplaylist [OPTIONS] [file(s)]")
			print("\nOptions:")
			print("  -g, --generate [name] [path1] [path2] [etc...]: generate a new playlist-template from ")
			print("  -p, --play [name] [number of songs]: generate a new playlist from a playlist-template and play it ")
			print()
		elif sys.argv[1] == "-g" or sys.argv[1] == "--generate":
			if len(sys.argv) > 3:
				playlistExtracted = []

				for i in range(3, len(sys.argv)):
					inFile = open(os.path.abspath(sys.argv[i]), 'r')
					fileContent = inFile.readlines()
					playlistExtracted.extend(extractM3U(fileContent))

				savePlaylist(os.path.abspath("./playlists/"+sys.argv[2]+".playlist"), playlistExtracted)
				print("  New playlist successfully created!")
			else:
				print("  Error: not enough arguments. 3 needed at least.")
		elif sys.argv[1] == "-p" or sys.argv[1] == "--play":
			if len(sys.argv) > 3:
				finalPlaylist = utils.generatePlaylist(os.path.abspath("./playlists/"+sys.argv[2]+".playlist"), int(sys.argv[3]))
				utils.saveToM3U(sys.argv[2], finalPlaylist)
				utils.play(os.path.abspath("./generatedPlaylists/"+sys.argv[2]+".m3u"))
			else:
				print("  Error: not enough arguments. 3 needed at least.")



main()
