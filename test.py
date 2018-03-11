import rt
import math

vec0 = rt.Vec3()
vec1 = rt.Vec3(1.0,2.0,3.0)
vec2 = rt.Vec3(5.0,4.0,1.0)
vec3 = vec1.Lerp(vec2,1)
vec3.PrintDesc()

length = vec1.Length()
print(length)

vec4 = rt.Vec3(4.0,0.0,0.0)
rt.UnitVector(vec4).PrintDesc()

vec4 = rt.Vec3(1.0,1.0,1.0)
rt.UnitVector(vec4).PrintDesc()



