import math

class TriObj(object):
	def __init__(self,p1,p2,p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.parse_edges()
	def get_central_weight(self):
		return [(p1[0]+p2[0]+p3[0])/3.,(p1[1]+p2[1]+p3[1])/3.]
	def get_central_vertical(self):
		p12,p23,p31 = [(self.p1[0]+self.p2[0])/2., (self.p1[1]+self.p2[1])/2.], [(self.p2[0]+self.p3[0])/2., (self.p2[1]+self.p3[1])/2.], [(self.p3[0]+self.p1[0])/2., (self.p3[1]+self.p1[1])/2.]
		h1 = [(self.p1[0]+p23[0])/2.,(self.p1[1]+p23[1])/2.]
		h2 = [(self.p2[0]+p31[0])/2.,(self.p2[1]+p31[1])/2.]
		h3 = [(self.p3[0]+p12[0])/2.,(self.p3[1]+p12[1])/2.]
		hline = [h1,h2,h3]
		hleng = [self.length(self.p1,p23),self.length(self.p2,p31),self.length(self.p3,p12)]
		return hline[hleng.index(max(hleng))]
	def parse_edges(self, linesets, weightsets):
		self.l1 = [p1,p2]
		self.l1_type = self.get_edge_type(self.l1, linesets, weightsets)
		self.l2 = [p2,p3]
		self.l2_type = self.get_edge_type(self.l2, linesets, weightsets)
		self.l3 = [p3,p1]
		self.l3_type = self.get_edge_type(self.l3, linesets, weightsets)
	def length(self,c1,c2):
		return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)
	def get_edge_type(self, line, linesets, weightsets):
		for idx,lineset in enumerate(linesets):
			if line in lineset:
				return weightsets[idx]
		return 0