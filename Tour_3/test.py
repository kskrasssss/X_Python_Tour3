import unittest
from my1 import Compressor

class TestCompression(unittest.TestCase):
    def test_compress(self):
        compressor = Compressor()
        result = compressor.compress("dddddkkkoooppp")
        self.assertEqual(result, "5d3k3o3p")

    def test_decompress(self):
        compressor = Compressor()
        result = compressor.decompress("5d3k3o3p")
        self.assertEqual(result, "dddddkkkoooppp")

if __name__ == "__main__":
    unittest.main()