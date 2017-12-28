# A Simple and Convenient Mesh Process Tool
## Why it named "simple" ?
The external dependency is just numpy. The vertices and the facet are represented in numpy.ndarray. It's very easy to use such representation in different part of a project or as a transit in different mesh data structures.
## Current functions
Currently simple_mesh is just a personal programming practice to realize the idea of processing mesh using only numpy. I will continue updating.

Functions:
1.IO (read/write .obj)
```
from meshIO import readOBJ,writeOBJ
vertices, facet = readOBJ(OBJpath)
# if write successfully, return true
save_status = writeOBJ(SAVEpath, vertices, facet)
```

## How to use simple_mesh ?
Currently just import the needed functions. Run test.py to see if everything is ok.

