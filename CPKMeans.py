# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
import numpy as np
from disjoint import DisjointSet
from sklearn.metrics.cluster import normalized_mutual_info_score as NMI
import warnings
warnings.filterwarnings(action = "ignore", category = FutureWarning)

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
		self.penalty = W
		self.dset = DisjointSet(points.shape[0])
		num_points = points.shape[0]

		for i, j in must_link:
			self.dset.merge(i, j)
		self.clust_idx = [None for __ in range(num_points)]

		# Init sets
		sizes = self.dset.get_sizes()
		self.cannot_link = [{} for __ in range(num_points)]
		for i, j in cannot_link:
			i = self.dset.get(i)
			j = self.dset.get(j)
			self.cannot_link[i][j] = True
			self.cannot_link[j][i] = True

		self.neighbour_size = [0 for __ in range(num_points)]
		for idx, curclust in sizes:
			self.neighbour_size[idx] = len(curclust)

		num_sets = len(sizes)
		for i, (__, curclust) in enumerate(sizes):
			if len(curclust) == 1:
				num_sets = i
				break

		self.clust = []
		self.centre = []

		if num_sets >= num_clust:
			for idx, curclust in sizes[ : num_clust]:
				self.insert_clust(idx, curclust)
			for __, curclust in sizes[num_clust : ]:
				for i in curclust:
					self.assign_clust(i)
		else:
			clust_ids = []
			waiting_list = []
			for idx, curclust in sizes[ : num_sets]:
				self.insert_clust(idx, curclust)
				clust_ids.append(idx)
			rest_cnt = num_clust - num_sets
			for idx, curclust in sizes[num_sets : ]:
				all_cannot = True
				for jdx in clust_ids:
					if ts(idx, jdx) not in self.cannot_link:
						all_cannot = False
						break
				if all_cannot and rest_cnt > 0:
					self.insert_clust(idx, curclust)
					rest_cnt -= 1
				else:
					waiting_list.extend(curclust)
			global_mean = np.mean(self.points, axis = 0)
			for __ in range(rest_cnt):
				perturbation = np.random.randn(self.points[0].shape)
				curpt = global_mean + perturbation
				self.clust.append({})
				self.centre.append(curpt)
	
			for i in waiting_list:
				self.assign_clust(i)

	def compute_centre(self, clust_ids):
		clust = self.points[clust_ids]
		return np.mean(clust, axis = 0)

	def insert_clust(self, idx, clust_ids):
		self.clust.append({idx : len(clust_ids)})
		self.centre.append(self.compute_centre(clust_ids))

	def compute_nearest_clust(self, x):
		xrt = self.dset.get(x)
		must_link_size = self.neighbour_size[xrt]
		min_dist = 1e100
		for i, clust in enumerate(self.clust):
			curd = np.linalg.norm(self.points[x] - self.centre[i])
			curd += self.penalty * (must_link_size - clust.get(xrt, 0))
			for idx, size in clust.items():
				if idx in self.cannot_link[xrt]:
					curd += self.penalty * size
			if curd < min_dist:
				min_dist = curd
				res_clust = i
		return res_clust

	def assign_clust(self, i):
		j = self.compute_nearest_clust(i)
		rt = self.dset.get(i)
		if rt not in self.clust[j]:
			self.clust[j][rt] = 0
		self.clust[j][rt] += 1

	def __call__(self, ground_truth = None, num_iteration = 100):
		for T in range(num_iteration):
			for i in range(self.points.shape[0]):
				self.clust_idx[i] = self.compute_nearest_clust(i)
			self.clust = [{} for i in range(self.num_clust)]
			tmp_clust = {}
			for i in range(self.points.shape[0]):
				j = self.dset.get(i)
				rt = self.clust_idx[i]
				if j not in self.clust[rt]:
					self.clust[rt][j] = 0
				self.clust[rt][j] += 1
				if rt not in tmp_clust:
					tmp_clust[rt] = []
				tmp_clust[rt].append(i)
			for i, clust_ids in enumerate(tmp_clust):
				self.centre[i] = self.compute_centre(clust_ids)
			if ground_truth is not None:
				this_nmi = NMI(self.clust_idx, ground_truth)
				print("Iteration: {}, NMI = {}".format(T, this_nmi))
		return self.clust_idx