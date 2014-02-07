#!/usr/bin/env python
#
# Small Python utility that reads an ABAQUS file and creates an image of the
# model.
#
# ABAQUS entities supported:
# Shells:
#	S4, S4R, S4RS, S3, S3R, S3RS, M3D4, M3D4R, M3D3, S8R, S8R5, M3D8, 
#	M3D8R, M3D6, SFM3D4, SFM3D4R, SFM3D3
# Bars:
#	B31, CONN3D2
# Solids: TODO
#
# This utility requires the Python Imaging Library (PIL). It has been 
# tested with PIL 1.1.6. You can get PIL at:
# 	http://www.pythonware.com/products/pil/
#
# Images are created in PNG and EPS formats. Other formats supported by PIL can
# also be implemented.
# 
# Writen by: Michalis Giannakidis, mgiannakidis@gmail.com

"""
usage: %prog [options] filename

Read an ABAQUS file in memory.
Save an image with the model's contents.
"""

__author__ = 'Michalis Giannakidis, 2007 June 17'
__version__ = '0.1'

#==============================================================================
# if PIL is not site installed, download it and provide the path to it here:
_PATH_TO_PIL_LIBRARY = '/home/mgiann/Imaging-1.1.6/PIL'
# angle (in degrees) between shells to consider as features
_FEATURE_ANGLE = 40

#==============================================================================

import os
import re
import optparse
import math
import random
import sys

try:
	import Image, ImageDraw, ImageFont
except ImportError:
	sys.path.append( _PATH_TO_PIL_LIBRARY )
	import Image, ImageDraw, ImageFont


#==============================================================================
# angle between facets to consider as feature
Costheta_feature = math.cos(_FEATURE_ANGLE * math.pi / 180.)
# rotation of the view to take image, in degrees
Rot_view_x = -45
Rot_view_y = 0
Rot_view_z = 30
# default width for images
Width = 400

#==============================================================================
abaqus_keyword_pattern = re.compile('^\*[A-Za-z ]+')
def l_is_keyword(line):
	m = abaqus_keyword_pattern.match(line)

	if m:
		return m.group(0).upper()
	else:
		return None

#==============================================================================
abaqus_comment_pattern = re.compile('^\*\*')
def l_is_comment(line):
	m = abaqus_comment_pattern.match(line)

	if m:
		return True
	else:
		return False


#==============================================================================
def nnormal(nodes):
	l = len(nodes)
	if l == 3:
		d1x = nodes[1].x - nodes[0].x
		d1y = nodes[1].y - nodes[0].y
		d1z = nodes[1].z - nodes[0].z

		d2x = nodes[2].x - nodes[0].x
		d2y = nodes[2].y - nodes[0].y
		d2z = nodes[2].z - nodes[0].z
	else:
		d1x = nodes[2].x - nodes[0].x
		d1y = nodes[2].y - nodes[0].y
		d1z = nodes[2].z - nodes[0].z

		d2x = nodes[3].x - nodes[1].x
		d2y = nodes[3].y - nodes[1].y
		d2z = nodes[3].z - nodes[1].z

	dx = d1y*d2z - d1z*d2y
	dy = d1z*d2x - d1x*d2z
	dz = d1x*d2y - d1y*d2x

	dd = math.sqrt(dx*dx+dy*dy+dz*dz)
	if dd:
		dx = dx/dd
		dy = dy/dd
		dz = dz/dd
	else:
		dx = 0.
		dy = 0.
		dz = 0.

	return dx, dy, dz


#==============================================================================
class Node(object):
	__slots__ = ('id', 'x', 'y', 'z')
	def __init__(self, id, xc = 0., yc = 0, zc = 0):
		self.id = id	
		self.x = xc
		self.y = yc
		self.z = zc

	def populate(self):
		return True
	
#==============================================================================
class Element(object):
	__slots__ = ('id', 'prop')
	def __init__(self, id, prop):
		self.id = id
		self.prop = prop

	# FIXME populate for Element.... check if prop is compatible.
	def populate(self):
		sec_arr = entities_array('PROP')
		if sec_arr.has_key(self.prop):
			self.prop = sec_arr[self.prop]
			self.prop.elements.append(self)
		else:
			self.prop = None
			
		return True

class Shell(Element):
	__slots__ = ('n1', 'n2', 'n3', 'n4')
	def __init__(self, id, n1, n2, n3, n4, prop = None):
		Element.__init__(self, id, prop)
		self.n1 = n1
		self.n2 = n2
		self.n3 = n3
		self.n4 = n4

	def nodes(self):
		if self.n4:
			return ( self.n1, self.n2, self.n3, self.n4 )
		else:
			return ( self.n1, self.n2, self.n3 )


	def populate(self):

		try:
			nodes = entities_array('NODE')


			self.n1 = nodes[self.n1]
			self.n2 = nodes[self.n2]
			self.n3 = nodes[self.n3]
			if self.n4: self.n4 = nodes[self.n4]
			else: self.n4 = None

			if not Element.populate(self):
				return False

			return True
		except KeyError:
			return False

class Bar(Element):
	__slots__ = ('n1', 'n2')
	def __init__(self, id, n1, n2, prop = None):
		Element.__init__(self, id, prop)
		self.n1 = n1
		self.n2 = n2

	def nodes(self):
		return ( self.n1, self.n2 )

	def populate(self):

		try:
			nodes = entities_array('NODE')

			self.n1 = nodes[self.n1]
			self.n2 = nodes[self.n2]

			if not Element.populate(self):
				return False

			return True
		except KeyError:
			return False

	
#==============================================================================
class Section(object):
	__slots__ = ('id', 'name', 'type', 'elements', 'feature_lines')
	def __init__(self, id, name, type):
		self.id = id
		self.name = name
		self.type = type

		self.elements = []

		self.feature_lines = None

	def populate(self):
		return True

	def calc_feature_lines(self):
		if not self.type == 'SHELL':
			return
		if self.feature_lines:
			return

		self.feature_lines = []

		edges_shells = []
		for elem in self.elements:
			nodes = elem.nodes()
			l = len(nodes)
			for i in range(0, l):
				n1, n2 = nodes[i%l], nodes[(i+1)%l]

				edges_shells.append( (n1, n2, elem) )

		# all elements, no feature lines.
		for n1, n2, elem in edges_shells:
			self.feature_lines.append((n1, n2))
		return


#==============================================================================
def decode_data_line(line, min_num_vals = 0):
	ivals = []
	fvals = []
	svals = []

	vals = line.split(',')
	for val in vals:
		val = val.strip()

		is_number = True

		try:
			fvals.append( float(val) )
		except ValueError:
			fvals.append( 0. )
			is_number = False

		try:
			ivals.append( int(val) )
		except ValueError:
			ivals.append( 0 )
			is_number = False
			
		if not is_number:
			svals.append( val )
		else:
			svals.append( '' )

	l = len(vals)
	if min_num_vals > l:
		fvals.extend( [ 0. ] * (min_num_vals - l ) )
		ivals.extend( [ 0  ] * (min_num_vals - l ) )
		svals.extend( [ '' ] * (min_num_vals - l ) )

	return ivals, fvals, svals

#==============================================================================
param_pairs_pattern = re.compile('([A-Za-z][\w ]*)(=([\w;\./ -]*)|)')
def decode_keyword_line(line):
	#k, p = decode_keyword_line("*ELEMENT, TYPE=LALALA, V=wwwww, V2=0.2, WW")
	keyword = l_is_keyword(line)

	param_pairs = line.split(',')

	parameters = {}
	for param_pair in param_pairs[1:]:
		param_pair = param_pair.strip()
		m = param_pairs_pattern.match(param_pair)
		if m:
			if m.group(3):
				parameters[m.group(1).strip().upper()] = \
						m.group(3).strip()
			else:
				parameters[m.group(1).strip().upper()] = None


	return keyword, parameters
		
#==============================================================================
def cmp_abaqus_names(x, y):

	x = x.replace(' ', '').upper()
	y = y.replace(' ', '').upper()
	return cmp(x, y)

#==============================================================================
class AbaqusReader:

	def __init__(self, fname):
		self.filename = fname
		self.file = open(self.filename, 'rb')
		self.file_list = [ self.file ]
		self.current_line_num = 0
		self.end_of_file_reached = False

		self.prop_name_to_id = {}

	def __del__(self):
		map(file.close, self.file_list)

	def del_unused_after_input(self):
		del self.prop_name_to_id
		self.prop_name_to_id = None

	def readline(self):
		self.current_line = self.file.readline()
		# skip comments....
		while l_is_comment(self.current_line):
			self.current_line = self.file.readline()
		if self.current_line:
			self.current_line = self.current_line.rstrip()
			self.current_line_num = self.current_line_num + 1
			return True
		else:
			file = self.file_list.pop()
			file.close()
			if len(self.file_list) == 0:
				self.end_of_file_reached = True
				return False
			self.file = self.file_list[-1]
			return True


	def read_include(self, keyword, parameters):
		keyword, parameters = decode_keyword_line(self.current_line)
		if parameters.has_key('INPUT'):
			filename = parameters['INPUT']

			if not os.path.isabs(self.filename):
				filename = os.path.join(os.path.dirname(self.filename),filename)
			if os.path.isfile(filename):
				file = open(filename, 'rb')
				if file:
					self.file_list.append(file)
					self.file = file
			else:
				print '*INCLUDE %s is missing' % filename

		return 0

		
	def dummy_read_keyword(self):
		while self.readline():
			if l_is_keyword(self.current_line):
				return 1

			#print self.current_line


		return 0

	def prop_id_from_name(self, prop_name):
		if not self.prop_name_to_id.has_key(prop_name):
			self.prop_name_to_id[prop_name] = \
				len(self.prop_name_to_id) + 1
		return self.prop_name_to_id[prop_name]

	def read_nodes(self, keyword, parameters):
		
		# ar.current_line contains *NODE.
		n_arr = entities_array('NODE')
		while self.readline():

			if l_is_keyword(self.current_line):
				return 1

			i, f, s = decode_data_line(self.current_line, 4)

			id = i[0]
			if id > 0:
				n = Node(id, f[1], f[2], f[3])
				if not n_arr.has_key(id):
					n_arr[id] = n
				else:
					print "Node id: %d already exists" % id
		return 0

	def read_shells(self, keyword, parameters, is_tria):
		if parameters.has_key('ELSET'):
			prop = self.prop_id_from_name(parameters['ELSET'])
		else: prop = None

		sh_arr = entities_array('SHELL')
		while self.readline():

			if l_is_keyword(self.current_line):
				return 1

			i, f, s = decode_data_line(self.current_line, 5)

			id = i[0]
			n1 = i[1]
			n2 = i[2]
			n3 = i[3]
			n4 = i[4]
			if is_tria: n4 = 0

			if id > 0 and n1 > 0 and n2 > 0 and n3 > 0 and n4 >= 0:
				sh = Shell(id, n1, n2, n3, n4, prop)
				if not sh_arr.has_key(id):
					sh_arr[id] = sh
				else:
					print "Shell id: %d already exists" % id

		return 0

	def read_shells3(self, keyword, parameters):
		return self.read_shells(keyword, parameters, True)
	
	def read_shells4(self, keyword, parameters):
		return self.read_shells(keyword, parameters, False)
	
	def read_bars(self, keyword, parameters):
		if parameters.has_key('ELSET'):
			prop = self.prop_id_from_name(parameters['ELSET'])
		else: prop = None

		bar_arr = entities_array('BAR')
		while self.readline():

			if l_is_keyword(self.current_line):
				return 1

			i, f, s = decode_data_line(self.current_line, 5)

			id = i[0]
			n1 = i[1]
			n2 = i[2]

			if id > 0 and n1 > 0 and n2 > 0:
				bar = Bar(id, n1, n2, prop)
				if not bar_arr.has_key(id):
					bar_arr[id] = bar
				else:
					print "Bar id: %d already exists" % id

		return 0

	def read_section(self, keyword, parameters):
		if parameters.has_key('ELSET'):
			prop = parameters['ELSET']
			id = self.prop_id_from_name(parameters['ELSET'])
			sec = Section(id, prop, 
				self.properties_to_element_types[keyword])
			sec_arr = entities_array('PROP')
			if not sec_arr.has_key(id):
				sec_arr[id] = sec
			else:
				sec.type = self.properties_to_element_types[keyword]
				#print 'Section: %s already exists' % \
				#	parameters['ELSET']
			
		while self.readline():

			if l_is_keyword(self.current_line):
				return 1
			#skip all datalines...

		return 0


	def read_keyword(self, keyword):
		keyword, parameters = decode_keyword_line(self.current_line)
		if self.keywords_library_read_fun.has_key(keyword):
			print 'reading %s' % keyword
			reader = self.keywords_library_read_fun[keyword]
			try:
				return reader(self, keyword, parameters)
			except TypeError:
				for p, pval, rfun in reader:
					if parameters.has_key(p) and\
					   parameters[p] == pval:
						return rfun(self, keyword, parameters)
				print 'skipping, %s %s=%s' % \
					(keyword, p, parameters[p])
		else:
			print 'skipping %s' % keyword
			return self.dummy_read_keyword()

	#======================================================================
	keywords_library_read_fun = { 
		'*NODE' : read_nodes,
		'*INCLUDE' : read_include,
		'*ELEMENT' : ( ( 'TYPE', 'S4', read_shells4 ), 
		               ( 'TYPE', 'S4R', read_shells4 ),
		               ( 'TYPE', 'S4RS', read_shells4 ),
		               ( 'TYPE', 'S3', read_shells3 ),
		               ( 'TYPE', 'S3R', read_shells3 ),
		               ( 'TYPE', 'S3RS', read_shells3 ),
		               ( 'TYPE', 'M3D4', read_shells4 ),
		               ( 'TYPE', 'M3D4R', read_shells4 ),
		               ( 'TYPE', 'M3D3', read_shells3 ),

		               ( 'TYPE', 'S8R', read_shells4 ),
		               ( 'TYPE', 'S8R5', read_shells4 ),
		               ( 'TYPE', 'M3D8', read_shells4 ),
		               ( 'TYPE', 'M3D8R', read_shells4 ),
		               ( 'TYPE', 'M3D6', read_shells3 ),

			       # Joke: surfaces are shells!
		               ( 'TYPE', 'SFM3D4', read_shells4 ),
		               ( 'TYPE', 'SFM3D4R', read_shells4 ),
		               ( 'TYPE', 'SFM3D3', read_shells4 ),

		               ( 'TYPE', 'B31', read_bars ),
		               ( 'TYPE', 'CONN3D2', read_bars ),
			     ),
		'*SHELL SECTION' : read_section,
		'*MEMBRANE SECTION' : read_section,
		'*SURFACE SECTION' : read_section,
		'*SOLID SECTION' : read_section,
		'*BEAM SECTION' : read_section,
		'*BEAM GENERAL SECTION' : read_section,
		'*CONNECTOR SECTION' : read_section,
	}

	properties_to_element_types = { 
		'*SHELL SECTION' : 'SHELL',
		'*MEMBRANE SECTION' : 'SHELL',
		'*SURFACE SECTION' : 'SHELL',
		'*SOLID SECTION' : 'SOLID', # Trusses also....
		'*BEAM SECTION' : 'BAR',
		'*BEAM GENERAL SECTION' : 'BAR',
		'*CONNECTOR SECTION' : 'BAR',
		
	}


#==============================================================================
def entities_array(keyword):
	if sup_keywords_library.has_key(keyword):
		array = sup_keywords_library[keyword]
		return array
	return None

#==============================================================================
# elements can all go to the same array, as properties.
# but, since we will not create any  new elements, let's have them separate for
# now
sup_keywords_library = { 
	'NODE': {},
	'SHELL': {},
	'BAR': {},
	'PROP': {},
}


#==============================================================================
def populate_group(ent_dict):
	
	to_del = []

	for id, ent in ent_dict.iteritems():
		if not ent.populate():
			to_del.append(id)

	map( ent_dict.pop, to_del )
	
def populate_entities():

	for group, array in sup_keywords_library.iteritems():
		populate_group(array)
		
#==============================================================================

#==============================================================================
def read_abaqus_file(filename):

	ar = AbaqusReader(filename)
	st = True
	keyword_line_pending = 0
	while st:
		if not keyword_line_pending:
			st = ar.readline()

		keyword_line_pending = 0

		keyword = l_is_keyword(ar.current_line)
		if keyword:
			keyword_line_pending = ar.read_keyword(keyword)

		if ar.end_of_file_reached: break
			
		if not keyword_line_pending:
			pass
			#print "Unread line: %d: `%s'" % \
			#	(ar.current_line_num, ar.current_line)
	
	ar.del_unused_after_input()

	# done with reading...
	del ar

#==============================================================================
class ScreenView(object):
	def __init__(self, width):
		from math import sin, cos, pi

		a = Rot_view_x*pi/180 # x axis rot
		b = Rot_view_y*pi/180 # y axis rot
		c = Rot_view_z*pi/180 # z axis rot
		self.dxx = cos(c)*cos(b)
		self.dxy = -sin(c)*cos(b)
		self.dxz = sin(b)

		self.dyx = cos(c)*sin(b)*sin(a) + sin(c)*cos(a)
		self.dyy = cos(c)*cos(a) -  sin(c)*sin(b)*sin(a)
		self.dyz = -cos(b)*sin(a)

		self.dzx = sin(c)*sin(a) - cos(c)*sin(b)*cos(a)
		self.dzy = sin(c)*sin(b)*cos(a) +  sin(a)*cos(c)
		self.dzz = cos(b)*cos(a)

		self.width = width
		self.height = width/math.sqrt(2)

		self.xmin = 10e9
		self.ymin = 10e9
		self.zmin = 10e9
		self.xmax = -10e9
		self.ymax = -10e9
		self.zmax = -10e9

		self.xm = 0
		self.ym = 0

		self.scale = 1

	def view_bounds(self):

		for id, sec in entities_array('PROP').iteritems():
			for elem in sec.elements:
				nodes = elem.nodes()
				for n in nodes:
					nx, ny, nz = self.from_global(n.x, n.y, n.z)
					if nx < self.xmin:
						self.xmin = nx
					elif nx > self.xmax:
						self.xmax = nx
					if ny < self.ymin:
						self.ymin = ny
					elif ny > self.ymax:
						self.ymax = ny
					if nz < self.zmin:
						self.zmin  = nz
					elif nz > self.zmax:
						self.zmax  = nz
		dx = (self.xmax - self.xmin)
		dy = (self.ymax - self.ymin)
		
		sx = float(self.width)/float(dx)
		sy = float(self.height)/float(dy)
		self.scale = min(sx, sy)
		self.scale = self.scale*0.95

		self.xm = self.xmin-dx*0.025 # 0.95 + 0.025*2 = 1
		self.ym = self.ymin-dy*0.025

		xoffs = self.width - dx*self.scale/0.95
		if xoffs > 0:
			self.xm = self.xm - xoffs/(2*self.scale)
		yoffs = self.height - dy*self.scale/0.95
		if yoffs > 0:
			self.ym = self.ym - yoffs/(2*self.scale)

	def from_global(self, x, y, z):
		xn = self.dxx * x + self.dxy * y + self.dxz * z
		yn = self.dyx * x + self.dyy * y + self.dyz * z
		zn = self.dzx * x + self.dzy * y + self.dzz * z
		
		return xn, yn, zn

		
	def to_image(self, x, y, z):

		x, y = (x-self.xm)*self.scale, (y-self.ym)*self.scale

		return x, self.height - y

	def from_global_to_image(self, x, y, z):
		x, y, z = self.from_global(x, y, z)
		x, y = self.to_image(x, y, z)
		return x, y


	def edge_mid_z_key(self, e):
		x, y, z1 = self.from_global(e[0].x, e[0].y, e[0].z)
		x, y, z2 = self.from_global(e[1].x, e[1].y, e[1].z)
		zm = (z1 + z2) * 0.5
		return zm

	def print_vec(self):
		print '----------------------'
		print self.dxx, self.dxy, self.dxz
		print self.dyx, self.dyy, self.dyz
		print self.dzx, self.dzy, self.dzz
		print '----------------------'

	pass
#==============================================================================
def write_vrml(filename):
	try:
		file = open(filename, 'wb')
	except IOError:
		print 'Cannot write to file %s' % filename
		return
	
	n_arr = entities_array("NODE")

	# FIXME Implement vrml output.

	file.write('#VRML V2.0 utf8\n')
	file.close()


#==============================================================================
def random_color():
	r, g, b = random.randrange(1, 255), \
			random.randrange(1, 255), random.randrange(1, 255)
	return r, g, b

#==============================================================================
def write_image(image_fname_format, width):

	transp = 255

	sv = ScreenView(width)
	#sv.print_vec()

	sv.view_bounds();

	img = Image.new('RGB', (int(sv.width), int(sv.height)), \
				(255,255,255, 0) )
	img.info['Creator']= 'abq2img'

	draw = ImageDraw.Draw(img)

	font = ImageFont.load_default()
	# draw cord
	al = 20 #axis len
	xn = sv.dxx * 1 + sv.dxy * 0 + sv.dxz * 0
	yn = sv.dyx * 1 + sv.dyy * 0 + sv.dyz * 0
	draw.line((0 + al , sv.height - al, al*xn +al, sv.height - al*yn - al),\
				fill=(255, 0, 0, 255), width=2)
	xn = sv.dxx * 2 + sv.dxy * 0 + sv.dxz * 0
	yn = sv.dyx * 2 + sv.dyy * 0 + sv.dyz * 0
	draw.text((al*xn +al, sv.height - al*yn - al),\
				'x', font=font, fill=(255, 0, 0, 255))

	xn = sv.dxx * 0 + sv.dxy * 1 + sv.dxz * 0
	yn = sv.dyx * 0 + sv.dyy * 1 + sv.dyz * 0
	draw.line((0 + al , sv.height - al, al*xn +al, sv.height - al*yn - al),\
				fill=(0, 255, 0, 255), width=2)
	xn = sv.dxx * 0 + sv.dxy * 2 + sv.dxz * 0
	yn = sv.dyx * 0 + sv.dyy * 2 + sv.dyz * 0
	draw.text((al*xn +al, sv.height - al*yn - al),\
				'y', font=font, fill=(0, 255, 0, 255))

	xn = sv.dxx * 0 + sv.dxy * 0 + sv.dxz * 1
	yn = sv.dyx * 0 + sv.dyy * 0 + sv.dyz * 1
	draw.line((0 + al , sv.height - al, al*xn +al, sv.height - al*yn - al),\
				fill=(0, 0, 255, 255), width=2)
	xn = sv.dxx * 0 + sv.dxy * 0 + sv.dxz * 2
	yn = sv.dyx * 0 + sv.dyy * 0 + sv.dyz * 2
	draw.text((al*xn +al, sv.height - al*yn - al),\
				'z', font=font, fill=(0, 0, 255, 255))

	model_edges = []
	color_map = {}

	for id, sec in entities_array('PROP').iteritems():
		r, g, b = random_color()
		color_map[id] = random_color()

		if sec.feature_lines:
			map(lambda e : model_edges.append( (e[0], e[1], id)), \
				sec.feature_lines)
			del sec.feature_lines
			sec.feature_lines = None
		elif sec.type == 'BAR':
			for bar in sec.elements:
				(n1, n2) = bar.nodes()
				model_edges.append((n1, n2, id))

	model_edges.sort(key=sv.edge_mid_z_key)

	for n1, n2, id in model_edges:
		r, g, b = color_map[id]

		x1, y1 = sv.from_global_to_image(n1.x, n1.y, n1.z)
		x2, y2 = sv.from_global_to_image(n2.x, n2.y, n2.z)
		draw.line((x1, y1, x2, y2), fill=(r, g, b, transp))


	del draw 

	for fname, format in image_fname_format:
		img.save(fname, format)


#==============================================================================
def reader():

	# args parsing
	parser = optparse.OptionParser(usage=__doc__.strip(), 
		version='%prog '+ __version__)

	#parser.add_option('-v', '--output-vrml', action="store",
	#	metavar='ouptut_file',
	#	dest="ouptut_vrml_filename", 
	#	help='write model in VRML format to file')

	parser.add_option('-p', '--output-png', action="store",
		metavar='ouptut_file',
		dest="ouptut_png_filename", 
		help='write model in PNG format to file')

	parser.add_option('-e', '--output-eps', action="store",
		metavar='ouptut_file',
		dest="ouptut_eps_filename", 
		help='write model in EPS format to file')

	parser.add_option('-w', '--width', action="store",
		metavar='view_width',
		dest="view_width", 
		help='width of the image to create in pixels (default %d)' % Width)

	opts, args = parser.parse_args()

	if len(args) == 0:
		raise SystemExit('Error: no input file has been specified')
	filename = args[0]
	if not os.path.isfile(filename):
		raise SystemExit('Error: not a valid filename')
	# args parsing

	read_abaqus_file(filename)
	# done with reading...

	populate_entities()

	print 'NODES: %d' % len(entities_array('NODE'))
	print 'SHELLS: %d' % len(entities_array('SHELL'))
	print 'BARS: %d' % len(entities_array('BAR'))
	print 'PROPS: %d' % len(entities_array('PROP'))

	for id, sec in entities_array('PROP').iteritems():
		#print '%d: %s, %s: %d' % (id, sec.name, sec.type, \
		#			len(sec.elements))
		sec.calc_feature_lines()

	width = Width
	if opts.view_width:
		if float(opts.view_width) > 0:
			width = float(opts.view_width)

	image_formats = []

	if opts.ouptut_png_filename:
		image_formats.append((opts.ouptut_png_filename, 'PNG'))
	if opts.ouptut_eps_filename:
		image_formats.append((opts.ouptut_eps_filename, 'EPS'))

	print 'Please wait. Creating Images...'
	if len( image_formats ):
		write_image(image_formats, width)

	#if opts.ouptut_vrml_filename:
	#	write_vrml(opts.ouptut_vrml_filename)

	
#==============================================================================
if __name__ == "__main__": reader()
