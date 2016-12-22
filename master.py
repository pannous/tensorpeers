# purpose of 'master tracker servers':

# keeps the *best* model up to date
# serves the current model to peers
# download the progress of other peers
# validate their claimed accuracy
# reject checkpoints which are too far behind
# merge the progress of good peer checkpoints into the *current best master* model
# repeat ...
# coordinate with possible other master tracker servers (later)
