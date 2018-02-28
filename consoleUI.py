from playlistUtils import *

def consoleUI():
	while True:
		existingPlaylists = []
		playlistInput = str()
		answer = str()

		print("")
		print("Voici les playlists-templates existants:")
		# Listing existing playlists
		files = os.listdir(os.path.abspath("./playlists"))
		for e in files:
			l = e.split('.')
			if l[1] == "playlist":
				existingPlaylists.append(l[0])
		for playlist in existingPlaylists:
			print("   - "+playlist)

		print()
		playlistInput = input("Veuillez saisir le nom de votre playlist : ")
		if playlistInput == "quit" or playlistInput == "exit":
			break

		if not playlistInput in existingPlaylists:
			print("Cette playlist n'existe pas, voulez vous en creer une nouvelle? (y/n)")
			answer = input()

			if answer == 'y':
				print("Veuillez entrer successivement le chemin vers chacune des playlist au format .m3u qui composeront votre nouvelle playlist personnalisee (q pour terminer): ")
				playlistExtracted = []

				while True:
					answer = input()
					if answer != 'q':
						# On teste si le fichier existe
						openSuccess = True
						fileContent = []
						try:
							inFile = open(os.path.abspath(answer), 'r')
							fileContent = inFile.readlines()
							if fileContent[0].strip() != "#EXTM3U":
								openSuccess = False
						except IOError:
							openSuccess = False

						if not openSuccess:
							print("ERREUR: Votre fichier n'existe pas ou n'est pas au format m3u, didiou!")
						else:
							playlistExtracted.extend(extractM3U(fileContent))
							print("Playlist ajoutee!")
					else:
						break

				if len(playlistExtracted) == 0:
					print("Playlist vide!")
				else:
					savePlaylist(os.path.abspath("./playlists/"+playlistInput+".playlist"), playlistExtracted)
					print("Nouvelle playlist créée avec succès!")
			else:
				pass
		else: # We create a new playlist of a given size and then we play it
			songNumber = ""
			while not songNumber.isdigit() or int(songNumber) < 5 or int(songNumber) > 500000:
				songNumber = input("De combien de musiques avez vous besoin dans la playlist générée? : ")
			songNumber = int(songNumber)

			finalPlaylist = generatePlaylist(os.path.abspath("./playlists/"+playlistInput+".playlist"), songNumber)
			saveToM3U(playlistInput, finalPlaylist)
			play(os.path.abspath("./generatedPlaylists/"+playlistInput+".m3u"))

	print("Merci d'avoir utilisé autoplaylist!")
