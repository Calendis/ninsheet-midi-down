# Utility to download MIDIs from ninsheetmusic.org
# Bert Myroon
# 31 April, 2019
import requests
import os

# This is where the MIDIs are stored
# You can access them by appening a number after "mid/"
url = "https://www.ninsheetmusic.org/download/mid/"

# Set this higher than the actual amount of MIDIs to get them all
number_of_midis = 6000

# The maximum number of allowed consecutive failures before the script will no
# longer check for more MIDIs.
max_consecutive_failures = 4

# Set to true if you want to skip files that already exist locally
ignore_files = False

def main():
	consecutive_failures = 0
	for i in range(number_of_midis):
		
		filename = "midis/NSM_"+str(i)+".mid"
		download_url = url+str(i)
			
		if ignore_files or not os.path.isfile(filename):
			r = requests.get(download_url)
			if r.status_code != 200 or r.headers["Content-Type"] != "audio/mid":
				consecutive_failures += 1
				print(download_url, " returned an error or is not a MIDI file. Skipping.")
			else:
				consecutive_failures = 0

				print(filename, "does not exist. Writing...")
				new_midi_file = open(filename, "wb")
				new_midi_file.write(bytes(r.content))
				new_midi_file.close()
		else:
			print(filename, "already exists.")
			consecutive_failures = 0

		if consecutive_failures > max_consecutive_failures:
			print(consecutive_failures, "consecutive failures. Aborting.")
			return

main()