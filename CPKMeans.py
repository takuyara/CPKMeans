# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
import numpy as np

class DisjointSet:
	def __init__(self, num_points):
		self.fa = []
		for __ in range(num_points):
			self.fa.append(-1)
	def get(self, x):
		rt = x
		while self.fa[rt] != -1:
			rt = self.fa[rt]
		while x != rt:
			x1 = self.fa[x]
			self.fa[x] = rt
			x = x1
		return rt
	def merge(self, x, y):
		self.fa[self.get(x)] = self.get(y)
	def get_sizes(self):
		sz = {}
		for i in range(len(self.fa)):
			j = self.get(i)
			if j not in sz:
				sz[j] = []
			sz[j].append(i)
		res = []
		for idx, sz in sz.items():
			res.append((idx, sz))
		res.sort(key = lambda x: len(x[1]), reverse = True)
		return res

class CPKMeans:
	"""
		points: Numpy array of points.
		num_clust: desired number of clusters in CPKmeans.
		must_link: [(i, j)] means i and j must be linked.
		cannot_link: [(i, j)] means i and j cannot be linked.
		W: penalty of violating constraints.
	"""
	def __init__(self, points, num_clust, must_link, cannot_link, W = 1e8):
		# Initilization
		self.points = points
		self.num_clust = num_clust
		self.dset = DisjointSet(len(num_points))
		for i, j in must_link:
			self.dset.merge(i, j)
		self.cannot_link = {}
		for i, j in cannot_link:
			i = self.dset.get(i)
			j = self.dset.get(j)
			self.cannot_link[ts(i, j)] = True

		# Init sets
		sizes = self.dset.get_sizes()
		num_sets = len(sizes)
		for i, (__, curclust) in enumerate(sizes):
			if len(curclust) == 1:
				num_sets = i
				break
		self.clust = []
		self.centre = []
		if num_sets >= num_clust:
			for __, curclust in sizes[ : num_clust]:
				self.insert_clust(curclust)
			for __, curclust in sizes[num_clust : ]:
				for i in curclust:
					self.assign_clust(i)
		else:
			clust_ids = []
			waiting_list = []
			for idx, curclust in sizes[ : num_sets]:
				self.insert_clust(curclust)
				clust_ids.append(idx)
			rest_cnt = num_clust - num_sets
			for idx, curclust in sizes[num_sets : ]:
				all_cannot = True
				for jdx in clust_ids:
					if ts(idx, jdx) not in self.cannot_link:
						all_cannot = False
						break
				if all_cannot and rest_cnt > 0:
					self.insert_clust(curclust)
					rest_cnt -= 1
				else:
					waiting_list.extend(curclust)
			global_mean = np.mean(self.points, axis = 0)
			for __ in range(rest_cnt):
				perturbation = np.random.randn(self.points[0].shape)
				curpt = global_mean + perturbation
				self.clust.append([])
				self.centre.append(curpt)
			for i in waiting_list:
				self.assign_clust(i)

	def should_link(self, i, j):
		return 1. if self.dset.get(i) == self.dset.get(j) else 0.

	def shouldnot_link(self, i, j):
		return 1. if ts(self.dset.get(i), self.dset.get(j)) in self.cannot_link else 0.

	def compute_centre(self, clust_ids):
		clust = self.points[clust_ids]
		return np.mean(clust, axis = 0)

	def insert_clust(self, clust_ids):
		self.clust.append(clust_ids)
		self.centre.append(self.compute_centre(clust_ids))

	def compute_nearest_clust(self, idx):
		pass

	def assign_clust(self, i):
		j = self.compute_nearest_clust(i)
		self.clust[j].append(i)

	def __call__(iteration_times = 100):
		for __ in range(iteration_times):
			for i in range(len(self.points)):
				self.assign_clust(i)
			for i, clust in enumerate(self.clust):
				self.centre[i] = compute_centre(clust)

def ts(x, y):
	return (x, y) if x < y else (y, x)
