import numpy as np 

def readOBJ(meshpath):
	vertices = []
	facet = []
	with open(meshpath,'r') as f:
		for line in f:
			if line.startswith('v '):
				values = line.split()
				vertex = [float(values[k]) for k in range(1,4)]
				vertices.append(vertex)
			if line.startswith('f'):
				values = line.split()
				face = [int((values[k].split('/'))[0])-1 for k in range(1,4)]
				facet.append(face)
	vertices = np.array(vertices)
	facet = np.array(facet,dtype='int32')
	return vertices,facet

def writeOBJ(meshpath, vertices, facet):
	# save the mesh
	# if nothing wrong happened, True will be returned
	with open(meshpath, 'w') as f:
		# write the vertices
		for k in range(len(vertices)):
			towrite = 'v' + ' ' + str(vertices[k][0]) + ' ' + str(vertices[k][1]) +' ' + str(vertices[k][2]) + '\n'
			f.write(towrite)
		# write the facet
		for k in range(len(facet)):
			towrite = 'f' + ' ' + str(facet[k][0] + 1) + ' ' + str(facet[k][1] + 1) + ' ' + str(facet[k][2] + 1) + '\n'
			f.write(towrite)
	return True