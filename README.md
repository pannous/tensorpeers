# tensorpeers
P2P peer-to-peer training of deep learning tensorflow models

In the Golden age of deep learning, baidu and others have shown that training time scales almost linearly with the number of GPUs.
This gives large corporations an advantage over startups in the run for the best A.I. systems ... until now.

Tensorpeers will empower the community to combine their efforts and GPU time into quickly converging wonderful models.

The architecture has to be slightly different to existing 'parameter server' schemes, because of relatively slow Internet connections. However our optimistic guess is that this won't hinder the success of this project: as long as we find any  merging scheme, which successfully combines the *gained knowledge* of two separate runs, we should be fine.

To speed things up, we base this project on python-libtorrent.

Not to be confused with [exxact p2p deep-learning](https://exxactcorp.com/deep-learning-p2p.php)
