from __future__ import print_function
from __future__ import print_function
import sys

import time
try:
	import libtorrent as lt
except:
	print (""" You need to install the libtorrent dependency: One of
	apt-get install python-libtorrent
	apt-get install python3-libtorrent
	brew install libtorrent-rasterbar --with-python"

	pip install python-libtorrent DOESN'T WORK! use one of the above!
	building boost dependency might take a while
""")

	exit(0)
	# alternatives to libtorrent:
	# https://github.com/Blender3D/torrent not a functional replacement yet (but pure python)
	# https://github.com/damoxc/spritzle ?

def upload(model_name, path, checkpoint_nr):
	# Create torrent
	fs = lt.file_storage()
	lt.add_files(fs, path +"/" + checkpoint_nr)
	t = lt.create_torrent(fs)
	t.add_tracker("udp://tracker.openbittorrent.com:80/announce", 0)
	# t.add_tracker("udp://tracker.pannous.com:80/announce", 0) # see pytt
	t.set_creator('libtorrent %s' % lt.version)
	t.set_comment("checkpoint: " + checkpoint_nr)
	lt.set_piece_hashes(t, ".")
	torrent = t.generate()
	torrent_file = model_name+"_" + checkpoint_nr + ".torrent"
	f = open(torrent_file, "wb")
	f.write(lt.bencode(torrent))
	f.close()

	# Seed torrent
	ses = lt.session()
	ses.listen_on(6881, 6891)
	h = ses.add_torrent({'ti': lt.torrent_info(torrent_file), 'save_path': '.', 'seed_mode': True})
	print("Total size: " + str(h.status().total_wanted))
	print("Name: " + h.name())
	while True:
		s = h.status()
		state_str = ['queued', 'checking', 'downloading metadata', \
		             'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

		msg = '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
		print(msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
		sys.stdout.flush()

		time.sleep(1)


def download(model_name, checkpoint="current"):
	ses = lt.session()
	ses.listen_on(6881, 6891)

	e = lt.bdecode(open(model_name+"_"+checkpoint+".torrent", 'rb').read())
	info = lt.torrent_info(e)

	params = {'save_path': '.', 'storage_mode': lt.storage_mode_t.storage_mode_sparse, 'ti': info}
	h = ses.add_torrent(params)

	s = h.status()
	while (not s.is_seeding):
		s = h.status()
		state_str = ['queued', 'checking', 'downloading metadata', \
		             'downloading', 'finished', 'seeding', 'allocating']
		msg = '%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s'
		print(msg % (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))

		time.sleep(1)


def sync():
	upload()

