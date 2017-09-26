# coding: utf-8
import unittest
import lah


class TestLAH(unittest.TestCase):

    def test_translate(self):
        p=lah.Vec3.zero()
        m=lah.Mat4.translate(1, 2, 3)
        pp=m.apply(p)
        self.assertAlmostEqual(lah.Vec3(1, 2, 3).array, pp.array)

