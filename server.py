#!/usr/bin/python
import tensorflow as tf

cluster_spec = {'ps': ['localhost:2222'], 'worker': ['localhost:2223', 'localhost:2224']}

import socket
from flask import Flask


try:
	from urllib2 import urlopen
	from urllib import urlretrieve, quote
except ImportError:
	from urllib.request import urlopen, urlretrieve, quote  # py3 HELL

app = Flask(__name__)

@app.route('/')
def index():
	return 'TensorPeers distributed training server!\n'


@app.route('/register')
def register():
	return 'TensorPeers training client registered!\n'


@app.route('/list')
def list_clients():
	return 'TensorPeers training client list:\n'+ client_list()


@app.route('/start')
def start():
	print("waiting for clients")
	cluster = tf.train.ClusterSpec(cluster_spec)
	server = tf.train.Server(cluster, job_name="ps")
	server.join()
	return "waiting for clients"

def client_list():
	return "\n".join(myip)


def download(url):  # to memory
	return urlopen(url).read()

host = socket.gethostname()
print("host", host)
myip = download('http://pannous.net/ip.php').strip()
print("myip", myip)
# local_ip=socket.gethostbyname(host)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=2221)

