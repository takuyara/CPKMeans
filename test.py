# Pionniers du TJ, benissiez-moi par votre Esprits Saints!
from constraints import generate_pairs
from CPKMeans import CPKMeans
import numpy as np
import csv
def test_dataset(points, labels, num_clust):
	must_link, cannot_link = generate_pairs(labels, num_clust, percentage = 0.01)
	cpkmeans = CPKMeans(points, num_clust, must_link, cannot_link)
	cpkmeans(ground_truth = labels, num_iteration = 20)

def load_csv(filename):
	csvfile = open(filename, newline = "")
	reader = csv.reader(csvfile)
	points = []
	labels = []
	label_dict = {}
	label_cnt = 0
	for row in reader:
		this_point = row[ : -1]
		this_point = np.array(this_point).astype("float32")
		this_label = row[-1]
		if this_label not in label_dict:
			label_dict[this_label] = label_cnt
			label_cnt += 1
		this_label = label_dict[this_label]
		points.append(this_point)
		labels.append(this_label)
	csvfile.close()
	points = np.array(points)
	return points, labels, label_cnt

def main(filename):
	points, labels, num_clust = load_csv(filename)
	test_dataset(points, labels, num_clust)

main("iris.csv")