from imports import *

import utils
import traceback
import sys
import random

def clustering(tri_list):
	pass

def parse_poly_conter(poly):
	x, y = 0, 0
	for e in poly:
		x += e[0]
		y += e[1]
	return [x/len(poly),y/len(poly)]

def weighted_clustering(polygons, part_num):
	clusters = {}
	init_centers = KMeans(n_clusters=part_num, algorithm='auto').fit(poly_centrals).clutser_centers_
	for cent in init_centers:
		clusters[cent] = []
	while len(polygons)!= 0:
		pass

def poly_cluster(polygons, part_num):
	poly_centrals = []
	polys = {}
	for poly in polygons:
		key = parse_poly_conter(poly)
		poly_centrals.append(key)
		polys[tuple(key)] = poly

	# clutser_centers = KMeans(n_clusters=part_num, algorithm='auto').fit(poly_centrals)
	clutser_centers = AgglomerativeClustering(n_clusters=part_num, linkage='complete', affinity='euclidean').fit(poly_centrals)
	

	poly_cent_labels = clutser_centers.labels_

	features = []
	for i in range(part_num):
		features.append([])
	for i in range(len(poly_cent_labels)):
		features[poly_cent_labels[i]].append(polys[tuple(poly_centrals[i])])

	edges = []
	for polygons in features:
		edges.append(parse_edges(polygons))
	return edges

def parse_edges(polygons):
	edges = []
	for polygon in polygons:
		for idx in range(len(polygon)-1):
			edges.append(tuple((tuple(polygon[idx]),tuple(polygon[idx+1]))))
		edges.append(tuple((tuple(polygon[-1]),tuple(polygon[0]))))
	edge_set = set()
	waste_set = set()
	for edge in edges:
		if edge not in edge_set and tuple((edge[1],edge[0])) not in edge_set:
			edge_set.add(edge)
		else:
			waste_set.add(edge)
			waste_set.add(tuple((edge[1],edge[0])))
	edges = list(edge_set - waste_set)
	edges = [[list(x[0]),list(x[1])] for x in edges]

	edges = parse_vertices(edges)
	edges.append(edges[0])
	return edges

def parse_vertices(edges):
	vertices_list = []
	while len(edges)!=0:
		vertices = edges[0]
		edges.remove(edges[0])
		prev_v = vertices[1]
		prev_l = 999
		while len(edges) != prev_l:
			prev_l = len(edges)
			for e in edges:
				if e[0]==prev_v:
					prev_v = e[1]
					vertices.append(e[1])
					edges.remove(e)
					break
				if e[1]==prev_v:
					prev_v = e[0]
					vertices.append(e[0])
					edges.remove(e)
					break
		vertices_list.append(vertices)
	lens = [len(x) for x in vertices_list]
	res = vertices_list[lens.index(max(lens))]
	return res
