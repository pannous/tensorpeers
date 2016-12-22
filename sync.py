from __future__ import print_function
from __future__ import print_function
import sys
import time
import libtorrent as lt

def upload(path, checkpoint_name):
	# Create torrent
	fs = lt.file_storage()
	lt.add_files(fs, path+"/"+ checkpoint_name)
	t = lt.create_torrent(fs)
	t.add_tracker("udp://tracker.openbittorrent.com:80/announce", 0)
	t.set_creator('libtorrent %s' % lt.version)
	t.set_comment("checkpoint: "+checkpoint_name)
	lt.set_piece_hashes(t, ".")
	torrent = t.generate()
	torrent_file = checkpoint_name + ".torrent"
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


def sync():
	upload()

