# purpose of 'master tracker servers':

# keeps the *best* checkpoint up to date
# serves the current model checkpoint state to peers
# download the progress of other peers
# validate their claimed accuracy
# reject checkpoints which are too far behind
# merge the progress of good peer checkpoints into the *current best master* model
# repeat ...
# coordinate with possible other master tracker servers (later)
import tensorpeers.sync
import pytt.tracker

def merge(model_name, path):
	#todo
	tensorpeers.sync.upload(model_name, path, "current")

def tracker():
	# Keep track of all models, peers and checkpoints
	pytt.tracker.start_tracker()
