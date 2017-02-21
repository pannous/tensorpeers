import tensorflow as tf
cluster = tf.train.ClusterSpec({'ps': ['localhost:2222'],
	'worker': ['localhost:2223', 'localhost:2224']
})

TASK_INDEX = -1#  -1=server 0=master-worker or n>=1:worker >
if TASK_INDEX==-1:
	print("waiting for clients")
	server = tf.train.Server(cluster, job_name="ps")
	server.join()

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('MNIST_data', one_hot=True)

server = tf.train.Server(cluster, job_name="worker", task_index=TASK_INDEX)#,shared=True)

with tf.device(tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % TASK_INDEX, cluster=cluster)):
	x = tf.placeholder(tf.float32, shape=[None, 784])
	y_ = tf.placeholder(tf.float32, shape=[None, 10])
	W = tf.Variable(tf.zeros([784, 10]))
	b = tf.Variable(tf.zeros([10]))
	y = tf.matmul(x, W) + b
	logits = tf.nn.softmax_cross_entropy_with_logits(logits=y,labels= y_)
	cross_entropy = tf.reduce_mean(logits)
	global_step = tf.Variable(0)

	train_op = tf.train.AdagradOptimizer(0.01).minimize(
		cross_entropy, global_step=global_step)
	summary_op = tf.summary.merge_all()
	init_op = tf.global_variables_initializer()

sv = tf.train.Supervisor(is_chief=(TASK_INDEX == 0),
                         init_op=init_op,
                         summary_op=summary_op,
                         global_step=global_step)

with sv.managed_session(server.target) as sess:
	step = 0
	batch_sz = 50
	iters = 55000 / batch_sz
	while not sv.should_stop() and step < iters:
		bx = mnist.train.images[step * batch_sz:(step + 1) * batch_sz]
		by = mnist.train.labels[step * batch_sz:(step + 1) * batch_sz]
		feed_dict={x: bx, y_: by}
		_, step = sess.run([train_op, global_step], feed_dict)

# Ask for all the services to stop.
sv.stop()
init_feed_dict={}
sess.run(init_op, feed_dict=init_feed_dict)
