import numpy as np
import math
class Point:
    
    def __init__(self,point,coordinates:tuple):
        """Clase plano

        Args:
            point (str): nombre plano
            coordinates (tuple): las coordenadas
        """
        
        self._points = {'point':point,'coordinates':coordinates}
        
    def get_coordinates(self):
        
        return list(self._points['coordinates'])#devuelve las coordenadas
        
    def aligned(self, point2): #para saber si dos puntos están alineados
        x1,y1,z1 = self.get_coordinates()
        x2,y2,z2 = point2.get_coordinates()
        if x1%x2 == 0 and y1%y2 == 0 and z1%z2 == 0:
            return True
        return False
    
    def __add__(self,other):
        if isinstance(other,Point):
            
            x1,y1,z1 = other.get_coordinates()
            x2,y2,z2 = self.get_coordinates()
            return (x1+x2,y1+y2,z1+z2)
    
        elif not isinstance(other, Point):
            x1,y1,z1 = other.get_coordinates()
            x2,y2,z2 = self.get_coordinates()
            return (x1+x2,y1+y2,z1+z2)
        
    def __sub__(self,other):

        if isinstance(other,Point):
            
            x1,y1,z1 = other.get_coordinates()
            x2,y2,z2 = self.get_coordinates()
            return (x2-x1,y2-y1,z2-z1)
         
        
        elif not isinstance(other, Point):
            x1,y1,z1 = other.get_coordinates(other)
            x2,y2,z2 = self._points.get(self)
            self._points[self] = (x2-x1,y2-y1,z2-z1)
            return self
        
    def __str__(self):
        
        return str(self._points['point']) + ':' + str(self._points['coordinates']) + '\n'
    
class Vector:
    def __init__(self, vector,coordinates):
        """Vector

        Args:
            vector (str): nombre vector
            coordinates (tuple): las coordenadas del vector
        """
        
        self._vectors = {'vector':vector, 'coordinates': coordinates}#diccionario para almacenar los elementos del vector
    
    def update_vector(self,key,item):#actualiza un vector
        self._vectors[key] = item
         
    def add_vector_point(self, point1,point2):#añadir un vector si sabes las coordenadas
        
        self._vectors['coordinates'] = (point2-point1)
        
    def get_coordinates(self):
        
        return list(self._vectors['coordinates'])
        
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
    
    def independent(self,v2,v3):#para saber si son independientes
        m = np.array([self.get_coordinates(),v2.get_coordinates(),v3.get_coordinates()])
        det = np.linalg.det(m)
        if det == 0:
            return False
        else:
            return True
    
    def __add__(self, other):

        if isinstance(other,Vector):
            
            x1,y1,z1 = other.get_coordinates()
            x2,y2,z2 = self.get_coordinates()
            return (x1+x2,y1+y2,z1+z2)
        
    def __radd__(self,other):

        if isinstance(other,Point):
            return other.__add__(self)
    
    def __sub__(self, other):

        if isinstance(other,Vector):
            return super().__sub__(other)
        
    def __rsub__(self,other):

        if isinstance(other,Point):
            x1,y1,z1 = tuple(Point.get_coordinates(other))
            x2,y2,z2 = self._vectors.get(self)
            self._points[self] = (x2-x1,y2-y1,z2-z1)
        return self
    def __eq__(self, v2) -> bool:
        if self.get_coordinates() == list(v2):
            return True
        else:
            return False
    
    def __mul__(self,other):
        
        if type(other) == int or type(other) == float:
           c = [other * coordinate for coordinate in self.get_coordinates()]
           self.update_vector(self,tuple(c))
           return self.get_vector(self)
        
        elif isinstance(other, Vector):#vale también para el vector afín de un punto
            #también producto vectorial
            for c2 in self.get_coordinates():
                n = [c1*c2 for c1 in other.get_coordinates()]
            self.update_vector('coordinates',tuple(n))
            return self
    def __rmul__(other,self):
        
        if isinstance(self,Vector):
            other.__mul__(self)
         
    
    def __str__(self):
            return str(self._vectors['vector']) + ':' + str(self._vectors['coordinates'])
    
class Line (Vector,Point):
    """REcta

    Args:
        Hereda de vector y punto
    """
    
    def __init__(self,line, point:Point, vector:Vector):
        """Recta

        Args:
            line (str): nombre del recta
            point (Point): punto
            vector (Vector): vector director
        """
        self._lines = {'line':line, 'elements': (point,vector)}

    def add_line_point(self, elem1,elem2): #con dos puntos
        if isinstance(elem1,Point) and isinstance(elem2,Point):

            d = Vector('director',None)
            d.add_vector_point(elem1,elem2)
            self._lines['elements'] = (elem1,d)

    
    def get_director(self):#devuelve el vector director
        point,vector = self._lines['elements']
        
        return vector
    
    def get_elements(self):
        e = []
        for elem in self._lines['elements']:
            e.append(elem)
        return e

    def imprimir(self,mode='implicit'):

        if mode == 'implicit':
            self.impression = 0
        elif mode == 'vectorial':
            self.impression = 1
        elif mode == 'parametrics':
            self.impression = 2
        elif mode == 'continuous':
            self.impression = 3
    

    def _implicit(self,ecuation1:list,ecuation2:list,ecuation3:list): #función para la ecuación implícita

        x,v1 = ecuation1
        y,v2 = ecuation2

        x_ = str(v2) + 'x + '
        n1_ = v2 * x
        y_ = str(v1) + 'y + '
        n2_ = v1 * y

        ec1 = '-'+ x_ + y_ + str(-n1_ + n2_)
        if v2 == 0:
            ec1 = x_ + y_ + str(-n1_ + n2_)
        x,v1 = ecuation1
        z,v3 = ecuation3
        x__ = str(v3) + 'x + '
        n3_ = v3 * x
        z_ = str(v1) + 'z + '
        n4_ = v1 * z
        ec2 =  '-'+ x__ + z_ + str(-n3_ + n4_)
        if  v3 == 0:
            ec2 = x__ + z_ + str(-n3_ + n4_)

        return [ec1,ec2]
    
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

    def __and__(self,other):
        if isinstance(other,Line):
            v1 = self.get_director()
            v2 = other.get_director()
            if v1 == v2:
                return True
            else:
                return False

    def __str__(self):
        
        if self.impression == 1:
            point = self.get_elements()[0]
            vector = self.get_coordinates()[1]
            return '(x,y,z) = ' + str(tuple(point.get_coordinates())) + ' + t' + str(tuple(vector.get_coordinates()))
            
        elif self.impression == 2:
            point = self.get_elements()[0]
            vector = self.get_coordinates()[1]
            return 'x = ' + str(point.get_coordinates()[0]) + ' + ' + str(vector.get_coordinates()[0])+'t \n' + 'y = ' + str(point.get_coordinates()[1]) + ' + ' + str(vector.get_coordinates()[1])+'t \n' + 'z = ' + str(point.get_coordinates()[2]) + ' + ' + str(vector.get_coordinates()[2])+'t \n'
            
        elif self.impression == 3:
            point = self.get_elements()[0]
            vector = self.get_coordinates()[1]
            return 'x - '+ str(point.get_coordinates()[0])+ '/ ' + str(vector.get_coordinates()[0]) + ' = y - ' + str(point.get_coordinates()[1]) + ' / ' + str(vector.get_coordinates()[1]) + '= z - ' + str(point.get_coordinates()[2]) +' / ' + str(vector.get_coordinates()[2])
            
        elif self.impression == 0:
            point = self.get_elements()[0]
            vector = self.get_elements()[1]
            e1 = [point.get_coordinates()[0],vector.get_coordinates()[0]]
            e2 = [point.get_coordinates()[1],vector.get_coordinates()[1]]
            e3 = [point.get_coordinates()[2],vector.get_coordinates()[2]]
            ec1, ec2 = self._implicit(e1,e2,e3)
            return str(ec1 + ' = 0 \n' + ec2 + ' = 0')
                
class Plane(Vector,Point):
    """Clase plano

    Args:
        Hereda de vector y punto
    """
    def __init__(self,plane,vector:Vector,point:Point):
        """plano

        Args:
            plane (str): nombre del plano
            vector (Vector): vector normal
            point (Point): punto
        """
        self._planes = {'plane':plane, 'elements' : (point,vector)}
        self._ecuation = []

    def add_plane_(self,elem1,elem2,elem3):
        """Dos formas de añadir un plano

        Args:
            elem1 (vector o punto)
            elem2 (vector o punto)
            elem3 (punto)

        Raises:
            TypeError: si los puntos están alineados
        """
        #para calcular el plano con tres puntos
        if isinstance(elem1,Point) == True and isinstance(elem2,Point) == True and isinstance(elem3, Point) == True:
            if Point.aligned(elem1,elem2) or Point.aligned(elem2,elem3) or Point.aligned(elem1,elem3):
                raise TypeError('You cannot add a plane if 3 points are aligned')
            v1 = self.add_vector_point(elem1,elem2) #!!!!!Cuidado
            v2 = self.add_vector_point(elem2,elem3)
            self._ecuation.append(elem1)
            self._ecuation.append(v1)
            self._ecuation.append(v2)
            m1 = np.array([[self.get_coordinates(v1)[1],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[1],self.get_coordinates(v2)[2]]]) #para calcular el vector normal
            m2 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[2]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[2]]])
            m3 = np.array([[self.get_coordinates(v1)[0],self.get_coordinates(v1)[1]],[self.get_coordinates(v2)[0],self.get_coordinates(v2)[1]]])
            i = np.linalg.det(m1)
            j = np.linalg.det(m2)
            k = np.linalg.det(m3)
            normal = Vector('normal',(i,j,k))
            self._planes['elements'] = (elem1,normal)
        #con dos vectores in un punto
        if isinstance(elem1, Vector) and isinstance(elem2, Vector) and isinstance(elem3,Point):
            self._ecuation.append(elem1)
            self._ecuation.append(elem2)
            self._ecuation.append(elem3)
            n1 = np.array([[elem1.get_coordinates()[1],elem1.get_coordinates()[2]],[elem2.get_coordinates()[1],elem2.get_coordinates()[2]]]) #para calcular el vector normal
            n2 = np.array([[elem1.get_coordinates()[0],elem1.get_coordinates()[2]],[elem2.get_coordinates()[0],elem2.get_coordinates()[2]]])
            n3 = np.array([[elem1.get_coordinates()[0],elem1.get_coordinates()[1]],[elem2.get_coordinates()[0],elem2.get_coordinates()[1]]])
            x = np.linalg.det(n1)
            y = np.linalg.det(n2)
            z = np.linalg.det(n3)
            perpendicular = Vector('normal',(x,y,z))
            self._planes['elements'] = (elem3,perpendicular)
    def get_plane(self,plane):
        if plane not in self._planes.keys():
            raise TypeError('This plane does not exist')
        return self._planes[plane]
    
    def get_normal(self):
        point,vector = self._planes['elements']
        
        return vector
    def get_ecuation(self):
        return self._ecuation

    def _implicit(self):#función para la implicita
        point, normal = self._planes['elements']
        d = -(point.get_coordinates()[0]*normal.get_coordinates()[0]) - (point.get_coordinates()[1]*normal.get_coordinates()[1]) - float((point.get_coordinates()[2]*normal.get_coordinates()[2]))
        return d
    
    def imprimir(self,mode='implicit'):

        if mode == 'implicit':
            self.impression = 0
        elif mode == 'vectorial':
            self.impression = 1
        elif mode == 'parametrics':
            self.impression = 2
        
    def __mul__(vector, other):
        return super().__mul__(other)
    
    def __rmul__(other, vector):
        return super().__rmul__(vector)          

    def __str__(self, mode = 'implicit'):

        if self.impression == 0: 
            normal = self.get_normal()
            return str(self._planes['plane']) + ':' + str(normal.get_coordinates()[0])+'x + ' +str(normal.get_coordinates()[1])+'y + '+ str(normal.get_coordinates()[2])+'z + ' + str(self._implicit()) + ' = 0'

        elif self.impression == 1:
            p,v1,v2 = self._ecuation
            return '(x,y,z) = ' + str(tuple(p.get_coordinates())) + ' + t' + str(tuple(v1.get_coordinates())) + '+ r' + str(tuple(v2.get_coordinates()))
        
        elif self.impression == 2:
            p,v1,v2 = self._ecuation
            return 'x = ' + str(p.get_coordinates()[0]) + ' + ' + str(v1.get_coordinates()[0])+'t' + ' + ' + str(v2.get_coordinates()[0])+'u \n' + 'y = ' + str(p.get_coordinates()[1]) + ' + ' + str(v1.get_coordinates()[1])+'t' + ' + ' + str(v2.get_coordinates()[1])+'u \n' + 'z = ' + str(p.get_coordinates()[2]) + ' + ' + str(v1.get_coordinates()[2])+'t' + ' + ' + str(v2.get_coordinates()[2])+'u \n' 


