#coding:utf-8

import geojson
import json
import os
import numpy as np
import sys
import codecs
import random
import matplotlib.pyplot as plt

from copy import deepcopy
from sklearn.cluster import *
from sklearn.mixture import *
from scipy.spatial import ConvexHull, Delaunay
from matplotlib.path import Path

import utils

root_path = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])

GLO_I = 14
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

def get_cd_geo():
	# file = codecs.open(root_path+'\\data\\chengdu_china_osm_polygon.geojson','r','latin-1')
	file = codecs.open(root_path+'\\source\\extract\\ex_osm_polygon.geojson','r','latin-1')
	cd_geo = geojson.load(file)
	idx = 0
	for f in cd_geo['features']:
		if f['properties']['boundary'] == 'administrative' and len(f['geometry']['coordinates'][0]) in range(80,1600):
			if int(f['properties']['osm_id']) not in [-6679988, -6680003]:
				geo_new = {'type': 'FeatureCollection', 'features': [{'geometry':{'type':'Polygon','coordinates':f['geometry']['coordinates']}}]}
				idx += 1
				print idx
				json.dump(geo_new, open(root_path+'\\source\\administrative\\boundary\\'+str(idx)+'.geojson', 'w'))	

def get_cd_geo_total_bound():
	# file = codecs.open(root_path+'\\data\\chengdu_china_osm_polygon.geojson','r','latin-1')
	file = codecs.open(root_path+'\\source\\extract\\ex_osm_polygon.geojson','r','latin-1')
	cd_geo = geojson.load(file)
	idx = 0
	fs = []
	for f in cd_geo['features']:
		if f['properties']['boundary'] == 'administrative' and len(f['geometry']['coordinates'][0]) in range(80,1600):
			if int(f['properties']['osm_id']) not in [-6679988, -6680003]:
				print f['properties']['name'].encode('utf-8')
				fs.append({'geometry':{'type':'Polygon','coordinates':f['geometry']['coordinates']}})
				idx += 1
				print idx
	geo_new = {'type': 'FeatureCollection', 'features': fs}
	json.dump(geo_new, open(root_path+'\\source\\administrative\\boundary\\'+str(0)+'.geojson', 'w'))			


def filt_geo_lst(geo, key, value_lst, fname):
	res_features = []
	for feature in geo['features']:
		if feature['properties'][key] in value_lst:		
			res_features.append(feature)
	geo_new = {'type': 'FeatureCollection', 'features': [res_features[GLO_I]]}
	json.dump(geo_new, open(root_path+'\\data\\source\\'+fname+'.geojson', 'w'))

def get_boundary_path(idx):
	name = 'i2_wenjiang'
	geo = geojson.load(codecs.open(root_path+'\\data\\source\\administrative\\boundary\\'+ADMIN_DICT[idx]+'.geojson','r','latin-1'))
	coords = geo['features'][0]['geometry']['coordinates'][0]
	codes = [Path.MOVETO]+[Path.LINETO]*(len(coords)-2)+[Path.CLOSEPOLY]
	boundary_path = Path(coords, codes)
	return boundary_path

def get_inner_geo(key, value_lst, idx):
	if key == 'highway':
		primlst = ['primary','trunk','motorway']
		fpath = 'road'
	elif key == 'railway':
		primlst = ['rail']
		fpath = 'rail'
	elif key == 'waterway':
		primlst = ['river']
		fpath = 'river'
	b_path = get_boundary_path(idx)
	geo_line = geojson.load(codecs.open(root_path+'\\data\\ex_osm_line.geojson','r','latin-1'))
	inner_features = []

	for feature in geo_line['features']:
		if feature['properties'][key] in value_lst:
		# if feature['properties'][key] not in ['subway','platform',None]:
			coord = feature['geometry']['coordinates']
			for i in range(len(coord)-1):
				p = [coord[i],coord[i+1]]
				c = [Path.MOVETO, Path.CLOSEPOLY]
				pth = Path(p,c)
				if b_path.contains_path(pth):
					inner_features.append(utils.downsample(p,0.003))
					# if feature['properties'][key] in primlst:
					# 	inner_features.append(utils.downsample(p,0.001))
					# 	# inner_features.append(p)
					# else:
					# 	inner_features.append(p)

	# geo_new = {'type': 'FeatureCollection', 'features': [{'geometry':{'type':'MultiLineString','coordinates':inner_features}}]}
	final_features = []
	for feature in inner_features:
		final_features.append({'geometry':{'type':'LineString','coordinates':feature}})
	geo_new = {'type': 'FeatureCollection', 'features': final_features}
	json.dump(geo_new, open(root_path+'\\data\\source\\administrative\\'+fpath+'\\'+ADMIN_DICT[idx]+'.geojson', 'w'))

if __name__ == '__main__':
	# lst = [3]
	lst = ADMIN_DICT.keys()
	for e in lst:
		# get_inner_geo('railway', ['rail'], e)
		# get_inner_geo('waterway', ['river'], e)
		# get_inner_geo('highway', ['primary','secondary','tertiary','trunk','residential','unclassified','motorway','construction'], e)
		get_inner_geo('highway', ['primary','secondary','tertiary','trunk','motorway'], e)
		# get_inner_geo('highway', ['primary','trunk'], e)
		print str(e)+' finished'