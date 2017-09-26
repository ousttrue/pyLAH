'''
Linear Algebra Helper
'''

import math


class Vec3:
    def __init__(self, *args):
        self.array=(args[0], args[1], args[2])
    @property
    def x(self): return self.array[0]
    @property
    def y(self): return self.array[1]
    @property
    def z(self): return self.array[2]

    @staticmethod
    def zero():
        return Vec3(0, 0, 0)


class Vec4:
    def __init__(self, *args):
        if isinstance(args[0], Vec3):
            self.array=(args[0].x, args[0].y, args[0].z, args[1])
        else:
            self.array=(args[0], args[1], args[2], args[3])
    @property
    def x(self): return self.array[0]
    @property
    def y(self): return self.array[1]
    @property
    def z(self): return self.array[2]
    @property
    def w(self): return self.array[3]
    @property
    def vec3(self): return Vec3(*self.array[:3])

    def dot(self, rhs):
        return self.x * rhs.x + self.y * rhs.y + self.z * rhs.z + self.w * rhs.w


class Mat4:
    def __init__(self, *args):
        self.array=(args[0], args[1], args[2], args[3], 
                args[4], args[5], args[6], args[7],
                args[8], args[9], args[10], args[11],
                args[12], args[13], args[14], args[15])

    def row(self, n):
        return Vec4(*self.array[n*4:n*4+4])

    def col(self, n):
        return Vec4(*self.array[n:16:4])

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
                self.row(3).dot(rhs.col(3))
                )

    def apply(self, v):
        v4=Vec4(v, 1)
        return Vec4(self.row(0).dot(v4), 
                self.row(1).dot(v4), 
                self.row(2).dot(v4), 
                self.row(3).dot(v4)
                ).vec3

    @staticmethod
    def identity():
        return Mat4(1, 0, 0, 0,
                    0, 1, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                    )

    @staticmethod
    def perspective(fovy, aspect, zNear, zFar):
        tan=math.atan(fovy * TO_RADIANS / 2)
        f = 1/tan
        return Mat4(f/aspect, 0, 0, 0,
                    0, f, 0, 0,
                    0, 0, (zFar + zNear)/(zNear - zFar), 2*zFar*zNear/(zNear - zFar),
                    0, 0, -1, 0
                    )

    @staticmethod
    def translate(x, y, z):
        return Mat4(1, 0, 0, x,
                0, 1, 0, y,
                0, 0, 1, z,
                0, 0, 0, 1
                )

    @staticmethod
    def rotateZAxisByRadians(angle):
        s=math.sin(angle)
        c=math.cos(angle)
        return Mat4(c, s, 0, 0,
                    -s, c, 0, 0,
                    0, 0, 1, 0,
                    0, 0, 0, 1
                    )
