import numpy as np
import math
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
        
    def aligned(self,point1, point2):
        x1,y1,z1 = self.get_coordinates(point1)
        x2,y2,z2 = self.get_coordinates(point2)
        if x1%x2 == 0 and y1%y2 == 0 and z1%z2 == 0:
            return True
        return False
    
    def __add__(self,other):
        if isinstance(other,Point):
            x1,y1,z1 = self._points.get(other)
            x2,y2,z2 = self._points.get(self)
            self._points[self] = (x1+x2,y1+y2,z1+z2)
            return self
        elif not isinstance(other, Point):
            x1,y1,z1 = other.get_coordinates(other)
            x2,y2,z2 = self._points.get(self)
            self._points[self] = (x1+x2,y1+y2,z1+z2)
            return self
    def __sub__(self,other):

        if isinstance(other,Point):
            x1,y1,z1 = self._points.get(other)
            x2,y2,z2 = self._points.get(self)
            self._points[self] = (x2-x1,y2-y1,z2-z1)
            return self
        elif not isinstance(other, Point):
            x1,y1,z1 = other.get_coordinates(other)
            x2,y2,z2 = self._points.get(self)
            self._points[self] = (x2-x1,y2-y1,z2-z1)
            return self
        
    def __str__(self, rpr = None):
        
        for point,coordinates in self._points.items():
            if rpr == None:
                return 'point:' + str(self._points[point]) + ':' + str(self.change_representation(rpr,coordinates)) + '\n'
            else:
                
                return 'point:' + str(self._points[point])+ ':' + str(self.change_representation(rpr,coordinates)) + '\n'
class Vector(Point):
    def __init__(self, vector):
        self._vectors = {vector : (0.00,0.00,0.00)}
        
    def add_vector(self,vector, x, y, z):
        if vector in self._vectors.keys():
            raise TypeError('Vertex already exists')
        self._vectors[vector] = (x,y,z)
    
    def update_vector(self,vector,item):
        if vector not in self._vectors.items():
            raise TypeError('This vector doesnt exists')
        self._vectors[vector] = item
         
    def add_vector_point(self, point1,point2 , vector):
        #(x1,y1,z1) = Point(point1) #donde sale el vector
        #(x2,y2,z2) = Point (point2) #donde acaba
        
        if vector in self._vectors.keys():
            raise TypeError('Vertex already exists')
        #self._vectors[vector] = (x2-x1,y2-y1,z2-z1)
        self._vectors[vector] = (point2-point1)
    def get_vector(self,vector):
        if vector not in self._vectors.keys():
            raise TypeError('This vector does not exist')
        return self._vectors[vector]
    
    def module(self):
        return math.sqrt(self.get_coordinates()[0] **2 + self.get_coordinates()[1] **2 + self.get_coordinates()[2] **2)
    
    def escalar(self,vector2):
        if len(self.get_coordinates(self)) != len(self.get_coordinates(vector2)):
            raise TypeError('You cant multiply two vectors of different lenght')
        e = self.get_coordinates(self)[0] * self.get_coordinates(vector2)[0] + self.get_coordinates(self)[1] * self.get_coordinates(vector2)[1] + self.get_coordinates(self)[2] * self.get_coordinates(vector2)[2]
        return e
    
    def angle(self,vector2):
        cos = self.escalar(vector2)/(self.module() * vector2.module())
        return cos
    
    def independent(self,v1,v2):
        return super().aligned(v1,v2)
    
    def change_representation(self, t, coordinates):
        return super().change_representation(t, coordinates)
    
    def __add__(self, other):

        if isinstance(other,Vector):
            return super().__add__(other)
    def __radd__(self,other):

        if isinstance(other,Point):
            x1,y1,z1 = tuple(Point.get_coordinates(other))
            x2,y2,z2 = self._vectors.get(self)
            self._points[self] = (x1+x2,y1+y2,z1+z2)
        return self
    
    def __sub__(self, other):

        if isinstance(other,Vector):
            return super().__sub__(other)
        
    def __rsub__(self,other):

        if isinstance(other,Point):
            x1,y1,z1 = tuple(Point.get_coordinates(other))
            x2,y2,z2 = self._vectors.get(self)
            self._points[self] = (x2-x1,y2-y1,z2-z1)
        return self
    
    def __mul__(self,other):
        
        if type(other) == int or type(other) == float:
           c = [other * coordinate for coordinate in self.get_coordinates(self)]
           self.update_vector(self,tuple(c))
           return self.get_vector(self)
        
        elif isinstance(other, Vector):#vale también para el vector afín de un punto
            #también producto vectorial
            for c2 in self.get_coordinates(self):
                n = [c1*c2 for c1 in other.get_coordinates(self)]
            self.add_vector(self+other,n[0],n[1],n[2])
            return self.get_vector(self)
    def __rmul__(other,self):
        
        if isinstance(self,Vector):
            other.__mul__(self)
         
    
    def __str__(self, rpr=None):
        return super().__str__(rpr)
    
class Line (Vector):
    
    def __init__(self, point:Point, vector:Vector, line, mode = 'implicit'):
        super().__init__(point,vector)
        self._lines = {line: (point,vector)}
        self._mode = mode 
    def add_line(self, point, vector, line):
        if line in self._lines.keys():
            raise TypeError('Line already exists')
        
        self._lines[line] = (Point(point), Vector(vector))
    
    def get_director(self):
        for point, vector in self._lines[self]:
            return vector

    def change_mode(self,modo:str):

        m = ['vectorial', 'parametrics', 'continuous', 'implicit']
        if modo not in m:
            raise TypeError('This is not a line ecuation')
        self._mode = modo

    def _implicit(ecuation1,ecuation2,ecuation3):

        for x,v1 in ecuation1:
            for y,v2 in ecuation2:
                x_ = str(v2) + 'x'
                n1_ = v2 * x
                y_ = str(v1) + 'y'
                n2_ = v1 * y

        ec1 = '-'+ x_ + y_ + str(-n1_ + n2_)

        for x,v1 in ecuation1:
            for z,v3 in ecuation3:
                x__ = str(v3) + 'x'
                n3_ = v3 * x
                z_ = str(v1) + 'z'
                n4_ = v1 * z
        ec2 =  '-'+ x__ + z_ + str(-n3_ + n4_)  

        return ec1,ec2
    
    def __mul__(vector, other):
        
        if isinstance(other,Point):
            raise TypeError('Cant multiply a line and a point')
        elif isinstance(other,Vector): #para el plano se debe hacer con el normal
            return super().__mul__(other)
        elif isinstance(other,Line):
            return super().__mul__(other.get_director())
    
    def __rmul__(other, vector):
        if isinstance(other,Point):
            raise TypeError('Cant multiply a line and a point')
        return super().__rmul__(vector)         

    def __str__(self):
        
        for (point,vector) in self._lines.items():
            
            if self._mode == 'vectorial':
                return '(x,y,z) = (' + str(point) + ') + t' + str(vector)
            
            elif self._mode == 'parametrics':
                return 'x = ' + str(point.get_coordinates(point)[0]) + ' + ' + str(vector.get_coordinates(vector)[0])+'t \n' + 'y = ' + str(point.get_coordinates(point)[1]) + ' + ' + str(vector.get_coordinates(vector)[1])+'t \n' + 'z = ' + str(point.get_coordinates(point)[2]) + ' + ' + str(vector.get_coordinates(vector)[2])+'t \n'
            
            elif self._mode == 'continuous':
                
                return 'x - '+ str(point.get_coordinates(point)[0])+ '/ ' + str(vector.get_coordinates(vector)[0]) + ' = y - ' + str(point.get_coordinates(point)[1]) + ' / ' + str(vector.get_coordinates(vector)[1]) + '= z - ' + str(point.get_coordinates(point)[2]) +' / ' + str(vector.get_coordinates(vector)[2])
            
            elif self._mode == 'implicit':
                
                for ec1, ec2 in self._implicit((point.get_coordinates(point)[0],vector.get_coordinates(vector)[0]),(point.get_coordinates(point)[1],vector.get_coordinates(vector)[1]),(point.get_coordinates(point)[2],vector.get_coordinates(vector)[2])):

                    return ec1 + '= 0 \n' + ec2 + '= 0'
                
class Plane(Vector):

    def __init__(self,vector:Vector,point:Point, plane, mode='implicit'):

        super().__init__(vector,point)
        self._planes = {plane : (point,vector)}
        self._mode = mode
        self._ecuation = {plane: (None,None,None)}

    def add_plane_(self,plane,*args):
        #para calcular el plano con tres puntos
        if plane in self._planes.keys():
            raise TypeError('Plane already exists')
        for point1,point2,point3 in args:
            if isinstance(point1,Point) and isinstance(point2,Point) and isinstance(point3, Point):
                if Point.aligned(point1,point2) or Point.aligned(point2,point3) or Point.aligned(point1,point3):
                    raise TypeError('You cannot add a plane if 3 points are aligned')
                v1 = self.add_vector_point(point1,point2) #!!!!!Cuidado
                v2 = self.add_vector_point(point2,point3)
                self._ecuation[plane] = (point1,v1,v2)
                m1 = np.array([[self.get_coordinates(v1)[1],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[1],self.get_coordinates(v2)[2]]]) #para calcular el vector normal
                m2 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[2]]])
                m3 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[1]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[1]]])
                i = np.linalg.det(m1)
                j = np.linalg.det(m2)
                k = np.linalg.det(m3)
                normal = (i,j,k)
                self._planes[plane] = (point1,normal)
        #con dos vectores in un punto
        for vector1, vector2, point in args:
            if isinstance(vector1, Vector) and isinstance(vector2, Vector):
                if self.independent(v1,v2):
                    raise TypeError('The two vectors need to be linearly independent')
                self._ecuation[plane] = (point,vector1,vector2)
                n1 = np.array([[self.get_coordinates(v1)[1],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[1],self.get_coordinates(v2)[2]]]) #para calcular el vector normal
                n2 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[2]]])
                n3 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[1]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[1]]])
                x = np.linalg.det(n1)
                y = np.linalg.det(n2)
                z = np.linalg.det(n3)
                perpendicular = (x,y,z)
                self._planes[plane] = (point,perpendicular)
    def get_plane(self,plane):
        if plane not in self._planes.keys():
            raise TypeError('This plane does not exist')
        return self._planes[plane]
    
    def get_normal(self):
        for point,vector in self._points[self]:
            return vector

    def change_mode(self,modo:str):

        m = ['vectorial', 'parametrics', 'continuous', 'implicit']
        if modo not in m:
            raise TypeError('This is not a line ecuation')
        self._mode = modo

    def _implicit(self,plane):
        for point, normal in self._planes[plane]:
            d = -(self.get_coordinates(point)[0]*self.get_coordinates(normal)[0]) - (self.get_coordinates(point)[1]*self.get_coordinates(normal)[1]) - (self.get_coordinates(point)[2]*self.get_coordinates(normal)[2])
        return self.get_coordinates(normal) + [d]
    
    def __mul__(vector, other):
        return super().__mul__(other)
    
    def __rmul__(other, vector):
        return super().__rmul__(vector)          

    def __str__(self):

        for (p,v_1, v_2) in self._ecuation.values():
            
            if self._mode == 'vectorial':
                return '(x,y,z) = (' + str(p) + ') + t' + str(v_1) + 'r' + str(v_2)
            
            elif self._mode == 'parametrics':
                return 'x = ' + str(self.get_coordinates(p)[0]) + ' + ' + str(self.get_coordinates(v_1)[0])+'t' + ' + ' + str(self.get_coordinates(v_2)[0])+'u \n' + 'y = ' + str(self.get_coordinates(p)[1]) + ' + ' + str(self.get_coordinates(v_1)[1])+'t' + ' + ' + str(self.get_coordinates(v_2)[1])+'u \n' + 'z = ' + str(self.get_coordinates(p)[2]) + ' + ' + str(self.get_coordinates(v_1)[2])+'t' + ' + ' + str(self.get_coordinates(v_2)[2])+'u \n' 
            
            
            elif self._mode == 'implicit':
                for plane in self._ecuation.keys():
                    if self._ecuation[plane] == (p,v_1,v_2):
                        return str(self._implicit(plane)[0]) + 'x' + str(self._implicit(plane)[1]) + 'y' + str(self._implicit(plane)[2]) +'z' +str(self._implicit(plane)[3]) +'= 0'
        