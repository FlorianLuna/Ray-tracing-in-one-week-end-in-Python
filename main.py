import array
import rt
import sys
import random

def RescaleColorToPPM(color, maxValue):
	return color.Mul(maxValue)

def Color(ray, world):
	tmp = rt.HitRecord()
	if world.Hit(ray, 0.0, sys.float_info.max, tmp):
		return rt.Vec3(tmp.Normal.X + 1.0, tmp.Normal.Y + 1.0, tmp.Normal.Z + 1.0).Mul(0.5)
	else:
		unitDirection = rt.UnitVector(ray.Direction)
		t = 0.5 * (unitDirection.Y + 1.0)
		return rt.Vec3(1.0,1.0,1.0).Lerp(rt.Vec3(0.5,0.7,1.0),t)

# PPM header
nx = 200
ny = 100
nsample = 10 # 100 but for performance purpose do not use much
maxval = 255
ppm_header = f'P6 {nx} {ny} {maxval}\n'

# PPM image data
image = array.array('B', [0, 0, 0] * nx * ny)

lowerLeftCorner = rt.Vec3(-2.0,-1.0,-1.0)
horizontal = rt.Vec3(4.0,0.0,0.0)
vertical = rt.Vec3(0.0,2.0,0.0)
origin = rt.Vec3()
scale = 255.9

scene = rt.HitableList()
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,0.0,-1.0), 0.5))
scene.Elems.append(rt.Sphere(rt.Vec3(0.0,-100.5,-1.0), 100.0))

mainCamera = rt.Camera()

for i in range(0, nx-1):
	for j in range(0, ny-1):
		color = rt.Vec3()		
		for k in range(0, nsample-1):
			u = ( float(i) + random.random() ) / float(nx)
			v = ( float(j) + random.random() ) / float(ny)		
			ray = mainCamera.GetRay(u,v)
			color += Color(ray,scene)			
		color = color.Mul(1.0/float(nsample))
		color = RescaleColorToPPM(color, scale)
		index = 3 * ((ny-1-j) * nx + i) #matching what is in the book
		image[index] = int(color.X)
		image[index + 1] = int(color.Y)
		image[index + 2] = int(color.Z)

# Save the PPM image as a binary file
with open('raytracing.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)