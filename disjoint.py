# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
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
		x = self.get(x)
		y = self.get(y)
		if x != y:
			self.fa[x] = y
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
