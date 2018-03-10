#import math

class Vec3:
	x=0.0
	y=0.0
	z=0.0
	
	def __init__(self, ax, ay, az):
		self.x=ax
		self.y=ay
		self.z=az

	def __add__(self, other):
		return vec3(self.__x+other.__x, self.__y+other.__y, self.__z+other.__z,)

	def __sub__(self, other):
		return vec3(self.__x-other.__x, self.__y-other.__y, self.__z-other.__z,)

	def Dot(other):
		return self.__x*other.__x + self.__y*other.__y + self.__z*other.__z

