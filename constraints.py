# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
import numpy as np
def generate_pairs(labels, num_clust, percentage, seed = None):
	rng = np.random.default_rng(seed)
	clust = [[] for __ in range(num_clust)]
	for i, lb in enumerate(labels):
		clust[lb].append(i)
	all_list = range(len(labels))
	must_link = []
	cannot_link = []
	for i, cur in enumerate(clust):
		must_cnt = int(percentage * len(cur) * len(cur))
		for __ in range(must_cnt):
			this_pair = tuple(rng.choice(cur, size = 2, replace = False))
			must_link.append(this_pair)
		cannot_cnt = int(percentage * len(cur) * (len(labels) - len(cur)))
		for __ in range(cannot_cnt):
			other = None
			while other is None or labels[other] == i:
				other = rng.choice(all_list)
			this_pair = (rng.choice(cur), other)
			cannot_link.append(this_pair)
	return must_link, cannot_link
