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
import tensorflow as tf

current_score=0.0
tolerance=0.9

def merge(model_name, path):
	print("accepting checkpoint with current best net")
	#todo

def tracker():
	print ("Keep track of all models, peers and checkpoints")
	pytt.tracker.start_tracker()
	pytt.tracker.get_peer_list()
	pytt.tracker.listen(new_peer_checkpoint_available)


def evaluate(graph, checkpoint):
	print(" confirm the announced test accuracy (todo)")
	return current_score

def new_peer_checkpoint_available(model_name,torrent):
	checkpoint=tensorpeers.sync.download(model_name, torrent)
	graph=tf.import_graph_def(model_name)
	score=evaluate(graph, checkpoint)
	if score<current_score*tolerance:
		print ("Rejecting this peers contribution because of low accuracy.")
		print(" sorry for wasting bandwidth, we keep the checkpoint: maybe there is still something to learn from it.")
	else:
		print ("accepting this peers contribution thanks to high accuracy.")
		merge(model_name,checkpoint)
		tensorpeers.sync.upload(model_name, checkpoint, "current") #How to switch seamlessly?


if __name__ == '__main__':
	tracker()
