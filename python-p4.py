class Point:
    
    def __init__(self, point):
        self._points = {point : (0.00,0.00,0.00)}
        
    def add_point(self, x: float, y: float, z: float, point):
        if point in self._points.keys():
            raise TypeError('This point already exists')
        
        self._points[point] = (x,y,z)
    
    def get_point(self, point):
        if point not in self._points.keys():
            raise TypeError('This point does not exist')
        
        return self._points[point]
    def get_coordinates(self,point):
        
        if point not in self._points.keys():
            raise TypeError('This point does not exist')
        return list(self._points[point])
    
    def change_representation(self, t, coordinates):
        for x,y,z in coordinates:
            return t(x),t(y),t(z)
        
    def __str__(self, rpr = None):
        
        for point,coordinates in self._points.items():
            if rpr == None:
                return 'point:' + str(self._points[point]) + ':' + str(self.change_representation(rpr,coordinates)) + '\n'
            else:
                
                return 'point:' + str(self._points[point])+ ':' + str(self.change_representation(rpr,coordinates)) + '\n'
class Vector(Point):
    def __init__(self, vector):
        self._vectors = {vector : (0,0,0)}
        
    def add_vector(self,vector, x, y, z):
        if vector in self._vectors.keys():
            raise TypeError('Vertex already exists')
        self._vectors[vector] = (x,y,z)
        
    def add_vector_point(self, point1,point2 , vector):
        (x1,y1,z1) = Point(point1) #donde sale el vector
        (x2,y2,z2) = Point (point2) #donde acaba
        
        if vector in self._vectors.keys():
            raise TypeError('Vertex already exists')
        self._vectors[vector] = (x2-x1,y2-y1,z2-z1)
    
    def get_vector(self,vector):
        if vector not in self._vectors.keys():
            raise TypeError('This vector does not exist')
        return self._vectors[vector]
    
    def change_representation(self, t, coordinates):
        return super().change_representation(t, coordinates)
    
    def __str__(self, rpr=None):
        return super().__str__(rpr)
    
class Line (Vector):
    
    def __init__(self, point, vector, line, mode = 'implicit'):
        super().__init__(point,vector)
        self._lines = {line: (point,vector)}
        self._mode = mode 
    def add_line(self, point, vector, line):
        if line in self._lines.keys():
            raise TypeError('Line already exists')
        
        self._lines[line] = (Point(point), Vector(vector))

    def change_mode(self,modo:str):

        m = ['vectorial', 'parametrics', 'continuous', 'implicit']
        if modo not in m:
            raise TypeError('This is not a line ecuation')
        self._mode = modo

    def __str__(self):
        
        for (point,vector) in self._lines.items():
            
            if self._mode == 'vectorial':
                return '(x,y,z) = ' + str(point) + 't' + str(vector)
            
            elif self._mode == 'parametrics':
                return 'x = ' + str(point.get_coordinates(point)[0]) + ' + ' + str(vector.get_coordinates(vector)[0])+'t \n' + 'y = ' + str(point.get_coordinates(point)[1]) + ' + ' + str(vector.get_coordinates(vector)[1])+'t \n' + 'z = ' + str(point.get_coordinates(point)[2]) + ' + ' + str(vector.get_coordinates(vector)[2])+'t \n'
            
            elif self._mode == 'continuous':
                
                return 'x - '+ str(point.get_coordinates(point)[0])+ '/ ' + str(vector.get_coordinates(vector)[0]) + ' = y - ' + str(point.get_coordinates(point)[1]) + ' / ' + str(vector.get_coordinates(vector)[1]) + '= z - ' + str(point.get_coordinates(point)[2]) +' / ' + str(vector.get_coordinates(vector)[2])
            
            elif self._mode == 'implicit':
                
                pass