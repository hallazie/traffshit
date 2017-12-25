import math

from imports import *

def seg_line(lst):
	# lst.append(lst[0])
	ret = []
	for i in range(len(lst)-1):
		ret.append([lst[i],lst[i+1]])
	return ret

def length(c1,c2):
	return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

def euc_dis(p1,p2):
	return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

# def upsample(nodes,gap):
# 	prev_len = 0
# 	cnt = 0
# 	while prev_len != len(nodes):
# 		if cnt%20==0:
# 			print 'removed %s nodes'%cnt
# 		prev_len = len(nodes)
# 		remove_flag = False
# 		remove_cnt = 0
# 		for node in nodes:
# 			if remove_flag:
# 				break
# 			for neighbor in nodes:
# 				if node != neighbor and euc_dis(node, neighbor)<gap:
# 					remove_cnt += 1
# 					if remove_cnt == 2:
# 						nodes.remove(node)
# 						cnt += 1
# 						remove_flag = True
# 						break
# 	return nodes

def upsample(nodes,gap):
	removed = True
	cnt_total = 0
	for node in nodes:
		cnt = 0
		# if cnt_total!=0 and cnt_total%500==0:
		# 	print 'removed %s nodes'%cnt_total
		for neighbor in nodes:
			if node!=neighbor and euc_dis(node, neighbor)<gap:
				nodes.remove(neighbor)
				removed = True
				cnt_total += 1
	return nodes

def downsample(nodes, gap):
	res = [nodes[0]]
	# print str(nodes[0])+' '+str(nodes[1])+' '+str(nodes[-2])+' '+str(nodes[-1])
	for i in range(1,len(nodes)):
		head = nodes[i-1]
		tail = nodes[i]

		downsample_nodes = []
		num = int(euc_dis(head,tail)/gap)
		# print num
		if num > 0:
			x_step = (tail[0]-head[0])/float(num)
			y_step = (tail[1]-head[1])/float(num)
		for j in range(1,num):
			downsample_nodes.append([head[0]+j*x_step, head[1]+j*y_step])
		res.extend(downsample_nodes)
		res.append(tail)
	# print str(res[0])+' '+str(res[1])+' '+str(res[-2])+' '+str(res[-1])
	return res

def tri_height(lst):
	c1,c2,c3 = lst[0],lst[1],lst[2]
	c12,c23,c31 = [(c1[0]+c2[0])/2., (c1[1]+c2[1])/2.], [(c2[0]+c3[0])/2., (c2[1]+c3[1])/2.], [(c3[0]+c1[0])/2., (c3[1]+c1[1])/2.]
	h1 = [(c1[0]+c23[0])/2.,(c1[1]+c23[1])/2.]
	h2 = [(c2[0]+c31[0])/2.,(c2[1]+c31[1])/2.]
	h3 = [(c3[0]+c12[0])/2.,(c3[1]+c12[1])/2.]
	hline = [h1,h2,h3]
	hleng = [length(c1,c23),length(c2,c31),length(c3,c12)]
	return hline[hleng.index(max(hleng))]

def parse_edges(polygons):
	# polygons = remove_trival_polygons(polygons)
	edges = []
	for polygon in polygons:
		edges.append(tuple((tuple(polygon[0]),tuple(polygon[1]))))
		edges.append(tuple((tuple(polygon[1]),tuple(polygon[2]))))
		edges.append(tuple((tuple(polygon[2]),tuple(polygon[0]))))
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

# def remove_trival_lines(edges):
# 	codes = [Path.MOVETO]+[Path.LINETO]*(len(edges)-2)+[Path.CLOSEPOLY]
# 	epath = Path(edges,codes)
# 	for i in range(len(edges)-1):
# 		cent = [(edges[i][0]+edges[i+1][0])/2.,(edges[i][1]+edges[i+1][1])/2.]
# 		if 

def remove_trival_polygons(polygons):
	pgroups = [[polygons[0]]]
	lgroups = [[
				[polygons[0][0],polygons[0][1]],
				[polygons[0][1],polygons[0][0]],
				[polygons[0][1],polygons[0][2]],
				[polygons[0][2],polygons[0][1]],
				[polygons[0][2],polygons[0][0]],
				[polygons[0][0],polygons[0][2]]]]
	polygons.remove(polygons[0])
	for polygon in polygons:
		flg = False
		lines = [
			[polygon[0],polygon[1]],
			[polygon[1],polygon[0]],
			[polygon[1],polygon[2]],
			[polygon[2],polygon[1]],
			[polygon[2],polygon[0]],
			[polygon[0],polygon[2]]]
		for i in range(len(lgroups)):
			if [polygon[0],polygon[1]] in lgroups[i] or [polygon[1],polygon[0]] in lgroups[i] or [polygon[1],polygon[2]] in lgroups[i] or [polygon[2],polygon[1]] in lgroups[i] or [polygon[2],polygon[0]] in lgroups[i] or [polygon[0],polygon[2]] in lgroups[i]:
				pgroups[i].append(polygon)
				lgroups[i].extend(lines)
				flg = True
				break
		if not flg:
			pgroups.append([polygon])
			lgroups.append([lines])
	lens = [len(x) for x in pgroups]
	print lens
	maxlen = max(lens)
	res = pgroups[lens.index(maxlen)]
	# print res
	return res

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

def parse_vertices_concat(polygons):
	pass

def get_dot_in_order(edge_list):
	node_list = [edge_list[0][1], edge_list[0][0]]
	node_list_len = len(edge_list)
	edge_list.remove(edge_list[0])
	curr_head = node_list[1]
	while len(edge_list) != 0:
		min_dis = 10000.
		for i in range(len(edge_list)):
			if edge_list[i][0] == curr_head:
				node_list.append(edge_list[i][1]) 
				curr_head = edge_list[i][1]
				edge_list.remove(edge_list[i])
				break
			elif edge_list[i][1] == curr_head:
				node_list.append(edge_list[i][0]) 
				curr_head = edge_list[i][0]
				edge_list.remove(edge_list[i])
				break
			curr_ids0 = euc_dis(curr_head,edge_list[i][0])
			curr_ids1 = euc_dis(curr_head,edge_list[i][1])
			if curr_ids0 < min_dis:
				min_dis = curr_ids0
				curr_min_head = edge_list[i][0]
				curr_remove_idx = i
				flag = 1
			if curr_ids1 < min_dis:
				min_dis = curr_ids1
				curr_min_head = edge_list[i][1]
				curr_remove_idx = i
				flag = 0
			if i == len(edge_list)-1:
				node_list.append(curr_min_head)
				curr_head = edge_list[curr_remove_idx][flag]
				edge_list.remove(edge_list[curr_remove_idx])
	return node_list

if __name__ == '__main__':
	# print tri_height([[0,0],[2,0],[1,100]])
	edges = [[[0,0],[1,0]],[[2,0],[1,0]],[[1,1],[2,2]],[[0,0],[1,1]],[[2,2],[2,1]],[[2,0],[2,1]]]
	print parse_vertices(edges)
	# nodes = [[0,0],[1,1],[1,2],[2,2],[3,3],[4,4],[4,2],[4,0],[2,0]]
	# print upsample(nodes,1.2)