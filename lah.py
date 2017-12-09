'''
Linear Algebra Helper

This library is row vector style and matrix use row major layout.
(DirectX style)

# mult order

pos = vec4 * Model * View * Projection
    = vec4 * MVP

# row major layout

| 0  1  2  3|
| 4  5  6  7|
| 8  9 10 11|
|12 13 14 15|

# glsl(col major)

glUniformMatrix4fv(loc, cnt, False, matrix)
(transposed)

## col major layout

| 0  4  8 12|
| 1  5  9 13|
| 2  6 10 14|
| 3  7 11 15|

GL_Position = PVM * vPosition;

# glsl(row major)

glUniformMatrix4fv(loc, cnt, True, matrix)
(not transposed)

GL_Position = vPosition * MVP;
'''

import math
from typing import NamedTuple
import unittest

TO_RADIANS = math.pi / 180


class Float3(NamedTuple):
    x: float = 0
    y: float = 0
    z: float = 0


class Float4(NamedTuple):
    x: float
    y: float
    z: float
    w: float


class Vec3(Float3):
    @staticmethod
    def zero()->'Vec3':
        return Vec3(0, 0, 0)

    @staticmethod
    def one()->'Vec3':
        return Vec3(1, 1, 1)

    def __add__(self, rhs)->'Vec3':
        return Vec3(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __sub__(self, rhs: 'Vec3')->'Vec3':
        return Vec3(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __mul__(self, factor: float)->'Vec3':
        return Vec3(self.x * factor, self.y * factor, self.z * factor)

    def dot(self, rhs)->float:
        return self.x*rhs.x + self.y*rhs.y + self.z*rhs.z

    def cross(self, rhs)->'Vec3':
        return Vec3(self.y*rhs.z-self.z*rhs.y,
                    self.z*rhs.x-self.x*rhs.z,
                    self.x*rhs.y-self.y*rhs.x)

    @property
    def sqnorm(self)->float: return self.dot(self)

    @property
    def norm(self)->float: return math.sqrt(self.sqnorm)

    @property
    def normalized(self): return self * (1/self.norm)


class Vec4(Float4):
    @staticmethod
    def zero()->'Vec4':
        return Vec4(0, 0, 0, 0)

    @staticmethod
    def one()->'Vec4':
        return Vec4(1, 1, 1, 1)

    @property
    def vec3(self):
        return Vec3(self.x, self.y, self.z)

    @property
    def vec3_w_normalized(self):
        return Vec3(self.x/self.w, self.y/self.w, self.z/self.w)

    def __add__(self, rhs)->'Vec4':
        return Vec4(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z, self.w + rhs.w)

    def __sub__(self, rhs: 'Vec4')->'Vec4':
        return Vec4(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z, self.w - rhs.w)

    def dot(self, rhs)->float:
        return (self.x * rhs.x +
                self.y * rhs.y +
                self.z * rhs.z +
                self.w * rhs.w)


class Quaternion(Float4):
    @staticmethod
    def identity():
        return Quaternion(0, 0, 0, 1)

    @property
    def mat3(self):
        return Mat3(1-2*self.y*self.y-2*self.z*self.z,
                    2*self.x*self.y-2*self.w*self.z,
                    2*self.x*self.z-2*self.w*self.y,

                    2*self.x*self.y+2*self.w*self.z,
                    1-2*self.x*self.x-2*self.z*self.z,
                    2*self.y*self.z-2*self.w*self.x,

                    2*self.x*self.z-2*self.w*self.y,
                    2*self.y*self.z+2*self.w*self.x,
                    1-2*self.x*self.x-2*self.y*self.y)
        '''
        return Mat3(1-2*self.y*self.y-2*self.z*self.z,
                    2*self.x*self.y+2*self.w*self.z,
                    2*self.x*self.z-2*self.w*self.y,

                    2*self.x*self.y-2*self.w*self.z,
                    1-2*self.x*self.x-2*self.z*self.z,
                    2*self.y*self.z+2*self.w*self.x,

                    2*self.x*self.z-2*self.w*self.y,
                    2*self.y*self.z-2*self.w*self.x,
                    1-2*self.x*self.x-2*self.y*self.y
                    )
        '''

class Mat3:
    def __init__(self, *args):
        if isinstance(args[0], Vec3):
            if len(args) != 3:
                raise ValueError('Mat3.__init__ 3')
            self.array = [args[0].x, args[0].y, args[0].z,
                          args[1].x, args[1].y, args[1].z,
                          args[2].x, args[2].y, args[2].z]
        else:
            if len(args) != 9:
                raise ValueError('Mat3.__init__ 9')
            self.array = [args[0], args[1], args[2],
                          args[3], args[4], args[5],
                          args[6], args[7], args[8]]

    def row(self, n):
        return Vec3(*self.array[n*3:n*3+3])

    def col(self, n):
        return Vec3(*self.array[n:9:3])


class Mat4:
    def __init__(self, *args):
        if isinstance(args[0], Vec4):
            if len(args) != 4:
                raise ValueError('Mat4.__init__ 4')
            self.array = [args[0].x, args[0].y, args[0].z, args[0].w,
                          args[1].x, args[1].y, args[1].z, args[1].w,
                          args[2].x, args[2].y, args[2].z, args[2].w,
                          args[3].x, args[3].y, args[3].z, args[3].w]
        else:
            if len(args) != 16:
                raise ValueError('Mat4.__init__ 16')
            self.array = [args[0], args[1], args[2], args[3],
                          args[4], args[5], args[6], args[7],
                          args[8], args[9], args[10], args[11],
                          args[12], args[13], args[14], args[15]]

    def row(self, n):
        return Vec4(*self.array[n*4:n*4+4])

    def col(self, n):
        return Vec4(*self.array[n:16:4])

    @property
    def lefttop3(self):
        return Mat3(self.row(0).vec3, self.row(1).vec3, self.row(2))

    @property
    def transposed(self):
        return Mat4(self.col(0), self.col(1), self.col(2), self.col(3))

    '''
    def __eq__(self, rhs):
        for i in range(16):
            if(math.abs(self.array[i] - rhs.array[i]) > 1e-4):
                return False
        return True
    '''

    def __mul__(self, rhs):
        return Mat4(
            self.row(0).dot(rhs.col(0)),
            self.row(0).dot(rhs.col(1)),
            self.row(0).dot(rhs.col(2)),
            self.row(0).dot(rhs.col(3)),
            self.row(1).dot(rhs.col(0)),
            self.row(1).dot(rhs.col(1)),
            self.row(1).dot(rhs.col(2)),
            self.row(1).dot(rhs.col(3)),
            self.row(2).dot(rhs.col(0)),
            self.row(2).dot(rhs.col(1)),
            self.row(2).dot(rhs.col(2)),
            self.row(2).dot(rhs.col(3)),
            self.row(3).dot(rhs.col(0)),
            self.row(3).dot(rhs.col(1)),
            self.row(3).dot(rhs.col(2)),
            self.row(3).dot(rhs.col(3)))

    def apply(self, v):
        if isinstance(v, Vec3):
            v4 = Vec4(v.x, v.y, v.z, 1)
        elif isinstance(v, Vec4):
            v4 = v
        else:
            raise ValueError('apply')

        applied = Vec4(v4.dot(self.col(0)),
                       v4.dot(self.col(1)),
                       v4.dot(self.col(2)),
                       v4.dot(self.col(3)))

        if isinstance(v, Vec3):
            return applied.vec3
        else:
            return applied

    @staticmethod
    def identity():
        return Mat4(1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1)

    @staticmethod
    def perspective(fovy, aspect, zNear, zFar):
        tan = math.atan(fovy * TO_RADIANS / 2)
        f = 1 / tan
        return Mat4(f / aspect, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, (zFar + zNear) / (zNear - zFar), -1,
                    0, 0, 2 * zFar * zNear / (zNear - zFar), 0)

    @staticmethod
    def translate(x, y, z):
        return Mat4(1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    x, y, z, 1)

    @staticmethod
    def rotateXAxisByDegrees(degree):
        rad = degree * TO_RADIANS
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(1, 0, 0, 0,
                    0, c, s, 0,
                    0, -s, c, 0,
                    0, 0, 0, 1)

    @staticmethod
    def rotateYAxisByDegrees(degree):
        rad = degree * TO_RADIANS
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(c, 0, -s, 0,
                    0, 1, 0, 0,
                    s, 0, c, 0,
                    0, 0, 0, 1)

    @staticmethod
    def rotateZAxisByRadians(rad):
        s = math.sin(rad)
        c = math.cos(rad)
        return Mat4(c, s, 0, 0,
                    -s, c, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1)


class Transform:
    def __init__(self, pos, rot):
        self.pos = pos
        self.rot = rot

    @staticmethod
    def identity():
        return Transform(Vec3.zero(), Quaternion.identity())

    @property
    def mat4(self):
        r = self.rot.mat3
        return Mat4(
            Vec4(r.row(0), 0),
            Vec4(r.row(1), 0),
            Vec4(r.row(2), 0),
            Vec4(self.pos, 1))


##############################################################################
# TestCases
##############################################################################
class Vec3TestCase(unittest.TestCase):
    def test_vec3(self):
        self.assertEqual(Vec3(0, 0, 0), Vec3())
        self.assertEqual(Vec3(0, 0, 0), Vec3.zero())
        self.assertEqual((0, 0, 0), Vec3.zero())
        self.assertEqual(Vec3(1, 1, 1), Vec3.one())
        self.assertEqual(Vec3(2, 2, 2), Vec3.one() + Vec3.one())


class Vec4TestCase(unittest.TestCase):
    def test_vec4(self):
        self.assertEqual(Vec4(0, 0, 0, 0), Vec4.zero())
        self.assertEqual((0, 0, 0, 0), Vec4.zero())
        self.assertEqual(Vec4(1, 1, 1, 1), Vec4.one())
        self.assertEqual(Vec4(2, 2, 2, 2), Vec4.one() + Vec4.one())


class QuaternionTestCase(unittest.TestCase):
    def test_quaternion4(self):
        self.assertEqual(Quaternion(0, 0, 0, 1), Quaternion.identity())
        #self.assertEqual(Quaternion(0, 0, 0, 1), Quaternion.identity() * Quaternion.identity())


class Mat4TestCase(unittest.TestCase):

    def test_translate(self):
        p = Vec3.zero()
        m = Mat4.translate(1, 2, 3)
        pp = m.apply(p)
        self.assertEqual(Vec3(1, 2, 3), pp)

    def test_matrix(self):
        a = Mat4.translate(1, 2, 3)
        b = Mat4.translate(2, 3, 4)
        c = a * b
        self.assertEqual(Mat4.translate(3, 5, 7).array, c.array)

        d = Mat4.translate(4, 5, 6)
        e = Mat4(d.row(0), d.row(1), d.row(2), d.row(3))
        self.assertEqual(d.array, e.array)
        self.assertEqual(d.row(3), Vec4(4, 5, 6, 1))


if __name__ == '__main__':
    unittest.main()
