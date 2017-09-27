# coding: utf-8
import unittest
import lah


class TestLAH(unittest.TestCase):

    def test_translate(self):
        p=lah.Vec3.zero()
        m=lah.Mat4.translate(1, 2, 3)
        pp=m.apply(p)
        self.assertAlmostEqual(lah.Vec3(1, 2, 3).array, pp.array)

    def test_matrix(self):
        a=lah.Mat4.translate(1, 2, 3)
        b=lah.Mat4.translate(2, 3, 4)
        c = a * b
        self.assertEqual(lah.Mat4.translate(3, 5, 7).array, c.array)

        d=lah.Mat4.translate(4, 5, 6)
        e=lah.Mat4(d.row(0), d.row(1), d.row(2), d.row(3))
        self.assertEqual(d.array, e.array)
        self.assertEqual(d.col(3).array, lah.Vec4(4, 5, 6, 1).array)

