class Point:
    
    def __init__(self, point:str):
        self._points = {point : (0,0,0)}
        
    def add_point(self, x, y, z, name):
        if name in self._points.keys():
            raise TypeError('This point already exists')
        
        self._points[name] = (x,y,z)
    
    def get_point(self, name):
        if name not in self._points.keys():
            raise TypeError('This point does not exist')
        
        return self._points[name]
    
class Vector:
    def __init__(self, vector):
        self._vectors = {vector : (0,0,0)}
    def add_vector_point(point1,point2):
        '''La idea es que tome dos puntos los reste y los añada al diccionario'''
        pass 