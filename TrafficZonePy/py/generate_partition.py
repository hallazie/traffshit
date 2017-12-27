# coding:utf-8

from imports import *

import utils
import traceback
import sys
import random

root_path = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
boundary_path = os.path.join(root_path,'data','source','administrative','boundary')
road_path = os.path.join(root_path,'data','source','administrative','road')
river_path = os.path.join(root_path,'data','source','administrative','river')
rail_path = os.path.join(root_path,'data','source','administrative','rail')

ADMIN_DICT = {
	1:'1_hongxinzhen',
	2:'2_heshanzhen',
	3:'3_sanjiangxiang',
	4:'4_qionglaishi',
	5:'5_pengshanxian',
	6:'6_xinjinxian',
	7:'7_shuangliuqu',
	8:'8_dayixian',
	9:'9_chongzhoushi',
	10:'10_shuimozhen',
	11:'11_wenjiangqu',
	12:'12_wuhouqu',
	13:'13_qingyangqu',
	14:'14_jinniuqu',
	15:'15_pixian',
	16:'16_ziyangshi',
	17:'17_jianyangshi',
	18:'18_jinjiangqu',
	19:'19_chenghuaqu',
	20:'20_longquanyiqu',
	21:'21_xinduqu',
	22:'22_qingbaijiangqu',
	23:'23_jintangxian',
	24:'24_wolongzhen',
	25:'25_gengdaxiang',
	26:'26_caopoxiang',
	27:'27_lixian'
}

ADMIN_IDX = [4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23]

GAP = 0.0004

def parse_inner_coords(regcode,road,river,rail):
	res = set()
	if road:
		geo = geojson.load(codecs.open(os.path.join(road_path, ADMIN_DICT[regcode]+'.geojson'),'r','latin-1'))
		for e in geo['features']:
			line = e['geometry']['coordinates']
			for c in line:
				res.add(tuple(c))
	if river:
		geo = geojson.load(codecs.open(os.path.join(river_path, ADMIN_DICT[regcode]+'.geojson'),'r','latin-1'))
		for e in geo['features']:
			line = e['geometry']['coordinates']
			for c in line:
				res.add(tuple(c))
	if rail:
		geo = geojson.load(codecs.open(os.path.join(rail_path, ADMIN_DICT[regcode]+'.geojson'),'r','latin-1'))
		for e in geo['features']:
			line = e['geometry']['coordinates']
			for c in line:
				res.add(tuple(c))
	return [list(x) for x in list(res)]

def partition_call(region_code, partition, road, railway, river, cluster_flag):
	regcode = region_code

	boundary_path = os.path.join(root_path,'data','source','administrative','boundary')

	geo_boundary = geojson.load(codecs.open(os.path.join(boundary_path, ADMIN_DICT[regcode]+'.geojson'),'r','latin-1'))
	boundary = geo_boundary['features'][0]['geometry']['coordinates'][0]
	inner = parse_inner_coords(regcode, road=road, river=river, rail=railway)

	# print 'before inner upsampling: %s, %s'%(len(inner), ADMIN_DICT[region_code])
	inner = utils.upsample(inner, 0.0025)
	# print 'after inner upsampling: %s, %s'%(len(inner), ADMIN_DICT[region_code])

	boundary_pair = []
	for i in range(len(boundary)-1):
		boundary_pair.append([boundary[i],boundary[i+1]])

	coord = boundary + inner

	if len(coord)>15000:
		print 'too large...'
		return
	coord_mat = np.array(coord)

	codes = [Path.MOVETO]+[Path.LINETO]*(len(boundary)-2)+[Path.CLOSEPOLY]
	boundary_path = Path(boundary, codes)	

	tri_origin = Delaunay(coord_mat)
	tri_point = tri_origin.points
	tri_simps = tri_origin.simplices
	tri_dict = {}
	tri_centrals = []
	tri = {}
	for i,k in enumerate(tri_simps):
		f1 = boundary_path.contains_point(tuple((tri_point[k[0]]+tri_point[k[1]])/2.))
		if [list(coord[k[0]]),list(coord[k[1]])] in boundary_pair or [list(coord[k[1]]),list(coord[k[0]])] in boundary_pair:
			f1 = True
		f2 = boundary_path.contains_point(tuple((tri_point[k[1]]+tri_point[k[2]])/2.))
		if [list(coord[k[1]]),list(coord[k[2]])] in boundary_pair or [list(coord[k[2]]),list(coord[k[1]])] in boundary_pair:
			f2 = True
		f3 = boundary_path.contains_point(tuple((tri_point[k[2]]+tri_point[k[0]])/2.))
		if [list(coord[k[2]]),list(coord[k[0]])] in boundary_pair or [list(coord[k[0]]),list(coord[k[2]])] in boundary_pair:
			f3 = True
		if f1 + f2 + f3 >= 3:
			# parse central of each tri
			key = utils.tri_height([list(tri_point[k[0]]), list(tri_point[k[1]]), list(tri_point[k[2]])])
			# key = tuple(((tri_point[k[0]][0]+tri_point[k[1]][0]+tri_point[k[2]][0])/3.,(tri_point[k[0]][1]+tri_point[k[1]][1]+tri_point[k[2]][1])/3.))
			tri_centrals.append(key)
			tri[tuple(key)] = [list(tri_point[k[0]]), list(tri_point[k[1]]), list(tri_point[k[2]])]

	# part_num = partition
	part_num = int(len(tri_centrals)/2.5)

	if cluster_flag == "kmeans":
		clutser_centers = KMeans(n_clusters=part_num, algorithm='auto').fit(tri_centrals)
	elif cluster_flag == 'batchkmeans':
		clutser_centers = MiniBatchKMeans(n_clusters=part_num).fit(tri_centrals)
	elif cluster_flag == 'agglomanhattan':
		clutser_centers = AgglomerativeClustering(n_clusters=part_num, linkage='complete', affinity='manhattan').fit(tri_centrals)
	else:
		clutser_centers = AgglomerativeClustering(n_clusters=part_num, linkage='complete', affinity='euclidean').fit(tri_centrals)
	
	tri_cent_labels = clutser_centers.labels_

	features = []
	for i in range(part_num):
		features.append([])
	for i in range(len(tri_cent_labels)):
		features[tri_cent_labels[i]].append(tri[tuple(tri_centrals[i])])

	edges = []
	for polygons in features:
		edges.append(utils.parse_edges(polygons))
		# edges.append(polygons)

	return edges

def save_json(edges):
	part_num = len(edges)
	feature_list = []
	for i in range(part_num):
		property_dict = {'name': i}
		geometry_dict = {'type': 'Polygon', 'coordinates': [edges[i]]}
		# geometry_dict = {'type': 'Polygon', 'coordinates': edges[i]}
		feature_list.append({'type': 'Feature', 'id': i, 'properties': property_dict, 'geometry': geometry_dict})	
	geo_dict = {'type': 'FeatureCollection', 'features': feature_list}
	json.dump(geo_dict, open(root_path+'\\data\\output\\clusters.geojson', 'w'))

def main(argv):
	# ADMIN_DICT = {
	# 1:'1_hongxinzhen',
	# 2:'2_heshanzhen',
	# 3:'3_sanjiangxiang',
	# 4:'4_qionglaishi',
	# 5:'5_pengshanxian',
	# 6:'6_xinjinxian',
	# 7:'7_shuangliuqu',
	# 8:'8_dayixian',
	# 9:'9_chongzhoushi',
	# 10:'10_shuimozhen',
	# 11:'11_wenjiangqu',
	# 12:'12_wuhouqu',
	# 13:'13_qingyangqu',
	# 14:'14_jinniuqu',
	# 15:'15_pixian',
	# 16:'16_ziyangshi',
	# 17:'17_jianyangshi',
	# 18:'18_jinjiangqu',
	# 19:'19_chenghuaqu',
	# 20:'20_longquanyiqu',
	# 21:'21_xinduqu',
	# 22:'22_qingbaijiangqu',
	# 23:'23_jintangxian',
	# 24:'24_wolongzhen',
	# 25:'25_gengdaxiang',
	# 26:'26_caopoxiang',
	# 27:'27_lixian'
	# }

	if len(argv) not in [6,7]:
		# print 'u need to input the right params...'
		print 0
	elif len(argv) == 7:
		cluster_flag = argv[6].lower()
		# cluster_flag = 'kmeans'
		region_code = int(argv[1])
		partition = int(argv[2])
		road = False if (argv[3]).lower()=="false" else True
		railway = False if (argv[4]).lower()=="false" else True
		river = False if (argv[5]).lower()=="false" else True
		edges = partition_call(region_code, partition, road, railway, river, cluster_flag)

		save_json(edges)
		print edges
	else:
		cluster_flag = 'aggloeuc'
		region_code = int(argv[1])
		partition = int(argv[2])
		road = False if (argv[3]).lower()=="false" else True
		railway = False if (argv[4]).lower()=="false" else True
		river = False if (argv[5]).lower()=="false" else True
		edges = partition_call(region_code, partition, road, railway, river, cluster_flag)

		save_json(edges)
		# print len(edges)
		print edges

if __name__ == '__main__':
	sys.argv.extend([20,20,'True','True','True','aggloeuc'])
	main(sys.argv)