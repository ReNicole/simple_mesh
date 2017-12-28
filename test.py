import numpy as np
import unittest
import os
import inspect
import meshIO

current_path = os.path.dirname(os.path.abspath(__file__))
sphere_path = os.path.join(current_path,'./test_data/sphere.obj')

class TestmeshIO(unittest.TestCase):
	def test_obj(self):
		vertices, facet = meshIO.readOBJ(sphere_path)
		save_path = os.path.join(current_path,'./test_data/test_obj.obj')
		save_status = meshIO.writeOBJ(save_path, vertices, facet)
		# check the return value
		self.assertTrue(save_status)
		# reload
		re_vertices, re_facet = meshIO.readOBJ(save_path)
		# check the reload
		self.assertTrue(np.allclose(vertices, re_vertices))
		self.assertTrue(np.allclose(facet, re_facet))

if __name__ == '__main__':
	unittest.main()