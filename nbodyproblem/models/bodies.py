from dataclasses import dataclass
import numpy as np

@dataclass
class AbstractVector():
    x : float
    y : float

    @property
    def size(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)
    
    @property
    def azimuth(self) -> float: # rad
        return np.arctan2(self.y,self.x)
    
    def to_polar(self):
        return (np.sqrt(self.x**2 + self.y**2),np.arctan2(self.y,self.x))
    
    @classmethod
    def from_cartesian(cls, x, y):
        return cls(x, y)

    @classmethod
    def from_polar(cls, size, azimuth):
        x = size * np.cos(azimuth)
        y = size * np.sin(azimuth)
        return cls(x, y)
    
    def get_difference(self,other):
        if not isinstance(other,AbstractVector):
            raise TypeError("Cant diff something that is not a vector")
        x_diff = other.x - self.x
        y_diff = other.y - self.y

        return self.__class__(x_diff,y_diff)
        
    def __add__(self, other):
        if not isinstance(other, AbstractVector):
            raise TypeError("Unsupported operand type for +: AbstractVector and {}".format(type(other)))
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __mul__(self, other):
        if not isinstance(other, (float,int)):
            raise TypeError("Multiplication factor must be a scalar")
        return self.__class__.from_polar(self.size * other,self.azimuth)
    
    def __eq__(self, other):
        if not isinstance(other, AbstractVector):
            return False
        return self.x == other.x and self.y == other.y
    
class Point(AbstractVector):
    pass

class Velocity(AbstractVector):
    pass

class Acceleration(AbstractVector):
    pass

class Force(AbstractVector):
    pass

@dataclass
class CelestialBody():
    name : str
    mass : float
    radius : float
    X : Point
    V : Velocity
    A : Acceleration

