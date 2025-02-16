import collections
import enum
import math
from random import random


class Vector3:
    """A 3-dimensional vector."""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float, y: float, z: float) -> None:
        """Create a new vector."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        """Pretty print a vector."""
        return 'Vector3(%.3f, %.3f, %.3f)' % (self.x, self.y, self.z)

    def __add__(self, other: 'Vector3') -> 'Vector3':
        """Add two vectors."""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        """Subtract two vectors."""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> 'Vector3':
        """Multiply a vector by a const"""
        return Vector3(self.x * other, self.y * other, self.z * other)

    def mag(self) -> float:
        """Return the magnitude (length) of a vector."""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def unit(self) -> 'Vector3':
        """
        Return the unit-vector in the same direction as a vector.

        WARNING: Undefined for zero-length vectors.
        """
        m = self.mag()
        return Vector3(self.x / m, self.y / m, self.z / m)

    def dot(self, other: 'Vector3') -> float:
        """Return the dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def angle_between(self, a: 'Vector3', c: 'Vector3') -> float:
        """
        Return the angle in degrees between (a - self) and (c - self):

        a       c
         \     /
          \.·./
           \ /
          self
        """
        m = (a - self).unit()
        n = (c - self).unit()
        r = m.dot(n)

        return math.degrees(math.acos(r))

def import_starmap(file:str)->list:
    """ Imports a starmap text file into a List(Tuple(Direction, Brightness)) """
    starmap = []
    with open(file) as f:
        for line in f:
            line = line.split('#')[0].strip()
            if line == '' :
                continue
            parts = line.split()

            if parts[0] == 'num_stars':
                continue

            pos = Vector3(*[float(x) for x in parts[0:3]])
            brightness = float(parts[3])

            starmap.append((pos, brightness))
    return starmap