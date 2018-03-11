import array
import rt

# a simple color method
def Color(ray):
	unitDirection = rt.UnitVector(ray.Direction)
	t = 0.5 * (unitDirection.Y + 1.0)
	tmp = rt.Vec3(1.0,1.0,1.0)
	tmp2 = rt.Vec3(0.5,0.7,1.0)
	return tmp.Lerp(tmp2,t)

# PPM header
nx = 200
ny = 100
maxval = 255
ppm_header = f'P6 {nx} {ny} {maxval}\n'

# PPM image data
image = array.array('B', [0, 0, 0] * nx * ny)

lowerLeftCorner = rt.Vec3(-2.0,-1.0,-1.0)
horizontal = rt.Vec3(4.0,0.0,0.0)
vertical = rt.Vec3(0.0,2.0,0.0)
origin = rt.Vec3(0.0,0.0,0.0)

for i in range(0, nx-1):
	for j in range(0, ny-1):
		u = float(i) / float(nx)
		v = float(i) / float(ny)
		ray = rt.Ray(origin, lowerLeftCorner+horizontal.Mul(u)+vertical.Mul(v))
		color = Color(ray)
		index = 3 * ((ny-1-j) * nx + i) #matching what is in the book
		image[index] = int(color.X*255.99)
		image[index + 1] = int(color.Y*255.99)
		image[index + 2] = int(color.Y*255.99)

test = rt.Vec3(1.0, 2.0, 3.0)

# Save the PPM image as a binary file
with open('raytracing.ppm', 'wb') as f:
	f.write(bytearray(ppm_header, 'ascii'))
	image.tofile(f)