import Queue
import numpy as np
"""
dealing with adjacency and orientation problem
"""

def get_vf_list(vertices,facet):
	""" return the facet index of each vertex(which triangles the vertex is in) """
	vf_list = [[] for k in range(len(vertices))]
	for k in range(len(facet)):
		for j in range(3):
			vf_list[facet[k,j]].append(k)
	return vf_list


def make_winding_consistent(vertices,facet):
	"""https://stackoverflow.com/questions/17036970/how-to-correct-winding-of-triangles-to-counter-clockwise-direction-of-a-3d-mesh"""
	"""
	note: to_process use python Queue to realize(store the element:[face_id,v1_id,v2_id]) where v1 v2 refers
	to the vertices of an oriented edge
	"""
	#winding_consistent = True
	vf_list = get_vf_list(vertices,facet)
	to_process = Queue.Queue()
	to_process.put((0, facet[0,1], facet[0,0]))
	# record whether the triangle facet has been processed; initially all false
	processed = np.zeros(len(facet),dtype=np.bool)
	while len(facet[processed]) < len(facet):
		next_process = to_process.get()
		processed[next_process[0]] = True
		if is_edge_face_opposite(facet[next_process[0]], next_process[1], next_process[2]) == False:
			# repair
			temp = facet[next_process[0]][1]
			facet[next_process[0]][1] = facet[next_process[0]][2]
			facet[next_process[0]][2] = temp
		for k in range(3):
			nei_id = get_edge_triangle_neighbor(vf_list, next_process[0],
				facet[next_process[0]][k], facet[next_process[0]][(k+1)%3])
			if nei_id >= 0 and processed[nei_id] == False: 
				to_process.put((nei_id, facet[next_process[0]][k], facet[next_process[0]][(k+1)%3]))	
	return vertices,facet

def is_winding_consistent(vertices,facet):
	"""https://stackoverflow.com/questions/17036970/how-to-correct-winding-of-triangles-to-counter-clockwise-direction-of-a-3d-mesh"""
	"""
	note: to_process use python Queue to realize(store the element:[face_id,v1_id,v2_id]) where v1 v2 refers
	to the vertices of an oriented edge
	"""
	winding_consistent = True
	vf_list = get_vf_list(vertices,facet)
	to_process = Queue.Queue()
	to_process.put((0, facet[0,1], facet[0,0]))
	# record whether the triangle facet has been processed; initially all false
	processed = np.zeros(len(facet),dtype=np.bool)
	while len(facet[processed]) < len(facet):
		next_process = to_process.get()
		processed[next_process[0]] = True
		if is_edge_face_opposite(facet[next_process[0]], next_process[1], next_process[2]) == False:
			winding_consistent = False
			return winding_consistent
		for k in range(3):
			nei_id = get_edge_triangle_neighbor(vf_list, next_process[0],
				facet[next_process[0]][k], facet[next_process[0]][(k+1)%3])
			if nei_id >= 0 and processed[nei_id] == False: 
				to_process.put((nei_id, facet[next_process[0]][k], facet[next_process[0]][(k+1)%3]))	
	return winding_consistent

def get_edge_triangle(vf_list,v1_id,v2_id):
	""" return the triangle face index which has the edge v1,v2 """
	face_id = list(set.intersection(set(vf_list[v1_id]), set(vf_list[v2_id])))
	return face_id

def get_edge_triangle_neighbor(vf_list,face_id,v1_id,v2_id):
	""" return the id of the triangle exactly share the same edge """
	tri_id = get_edge_triangle(vf_list, v1_id, v2_id)
	nei_id = -1
	for k in range(len(tri_id)):
		if tri_id[k] != face_id:
			nei_id = tri_id[k]
			break
	return nei_id

def get_triangle_neighbor(vf_list,facet,face_id):
	""" 
	return the facet index of the given triangle
	para::face_id: the id the query triangle face
	return: 3 face index
	..arranged in this way: neighbor on edge[0,1],[1,2],[2,0]
	"""
	nei_id = []
	for j in range(3):
		tri_id = get_edge_triangle(vf_list, facet[face_id][j], facet[face_id][(j+1)%3])
		if len(tri_id) < 2:
			continue
		if tri_id[0] == face_id:
			nei_id.append(tri_id[1])
		else:
			nei_id.append(tri_id[0])
	return nei_id

def is_edge_face_opposite(face, v1_id, v2_id):
	"""
	judge whether the edge is oriented opposite to the given face
	para::face: array like, id of the 3 vertices
	para::v1_id,v2_id: the id of the edge v1,v2
	"""
	temp_index = -1
	for k in range(3):
		if face[k] == v1_id:
			temp_index = k
			break
	if face[(temp_index+1)%3] == v2_id:
		return False
	else:
		return True

def get_edges(facet):
	""" 
	return the array(m,2) of the edges in the triangle mesh
	and we put the smaller index first
	"""
	edge_list = []
	for k in range(len(facet)):
		for j in range(3):
			if facet[k][j] < facet[k][(j+1)%3]:
				edge_list.append((facet[k][j], facet[k][(j+1)%3]))
			else:
				edge_list.append((facet[k][(j+1)%3], facet[k][j]))
			
	# remove the duplicate
	edge_list = list(set(edge_list))
	return edge_list

def get_ef_adjacency(vertices, facet):
	"""
	for each edge, give the id of the triangles that the edge is in
	"""
	vf_list = get_vf_list(vertices, facet)
	edge_list = get_edges(facet)
	tri_id = [get_edge_triangle(vf_list, edge_list[k][0], edge_list[k][1]) for k in range(len(edge_list))]
	return edge_list, tri_id

def get_vv_adjacency(vertices, facet):
	"""
	for each vertex, find the neighbor of it 
	can traverse each edge, anyway
	"""
	vv_list = [[] for k in range(len(vertices))]
	edge_list = get_edges(facet)
	for k in range(len(edge_list)):
		vv_list[edge_list[k][0]].append(edge_list[k][1])
		vv_list[edge_list[k][1]].append(edge_list[k][0])
	return vv_list

def get_edge_bdy_judge(edge_list, tri_id):
	"""
	return the edge list and another judge list
	whether the edge is interior or on the boundary
	if the adjacency face is 1, the edge is on the boundary
	"""
	judge = np.zeros(len(edge_list), dtype=np.bool)
	for k in range(len(edge_list)):
		if len(tri_id[k]) > 1:
			judge[k] = True
	return judge

def get_vertex_bdy_judge(vv_list):
	"""
	return the judge whether the vertex is on the boundary
	if its neighbours <=2, on the boundary
	"""
	judge = np.zeros(len(vv_list),dtype=np.bool)
	for k in range(len(vv_list)):
		if len(vv_list[k]) > 2:
			judge[k] = True
	return judge