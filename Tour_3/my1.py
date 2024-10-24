import multiprocessing
# print("Num of cpu: ",multiprocessing.cpu_count()) # My CPU cores = 12

class CompressionAlgorithm:
    """Абстрактний клас стиснення/розпакування"""
    def compress(self, data):
        '''Стискає вміст'''
        raise NotImplementedError

    def decompress(self, data):
        '''Розпаковує вміст'''
        raise NotImplementedError



class Compressor(CompressionAlgorithm):
    """Клас який виконує стичнення/розпаковування"""
    def compress(self, content):
        """Стискає вміст за алгоритмом RLE"""
        compressed = []
        i = 0
        while i < len(content):
            count = 1
            ch = content[i]
            while i + 1 < len(content) and content[i] == content[i + 1]:
                count += 1
                i += 1
            compressed.append(f'{count}{ch}')
            i += 1
        return ''.join(compressed)

    def decompress(self, content):
        """Розпаковує вміст за алгоритмом RLE"""
        decompressed = []
        i = 0
        while i < len(content):
            count = int(content[i])
            ch = content[i + 1]
            decompressed.append(ch * count)
            i += 2
        return ''.join(decompressed)


class FileManager:
    """Взаємодія з файлами, для спрощення роботи"""
    def __init__(self, file_path):
        """Налаштування шляху до файлу"""
        self.filepath = file_path

    def read_fl(self):
        """Читає вміст файлу"""
        with open(self.filepath, 'r') as file:
            return file.read()

    def write_fl(self, file_path, content):
        """Записує вміст до файлу"""
        with open(file_path, 'w') as file:
            file.write(content)



class CompressionService:
    """Виконує стискання і розпакування"""
    def __init__(self, algorithm: CompressionAlgorithm):
        self.algorithm = algorithm

    def compress_fl(self, inp_fl, out_fl):
        """Стискає"""
        fl_manager = FileManager(inp_fl)
        content_comp = fl_manager.read_fl()
        compressed_content = self.algorithm.compress(content_comp)
        fl_manager.write_fl(out_fl, compressed_content)

    def decompress_fl(self, inp_fl, out_fl):
        """Розпаковує"""
        fl_manager = FileManager(inp_fl)
        content_decomp = fl_manager.read_fl()
        decompressed_content = self.algorithm.decompress(content_decomp)
        fl_manager.write_fl(out_fl, decompressed_content)


def parallel_compress(fl_chunk, algorithm):
    """Функція для паралельного стиснення"""
    return algorithm.compress(fl_chunk)


if __name__ == "__main__":
    INP_FL = 'input.txt'
    COMPRESSED_FL = 'compressed.txt'
    DECOMPRESSED_FL = 'decompressed.txt'

    rle_compressor = Compressor()
    compression_service = CompressionService(rle_compressor)

    compression_service.compress_fl(INP_FL, COMPRESSED_FL)

    compression_service.decompress_fl(COMPRESSED_FL, DECOMPRESSED_FL)

    with open(INP_FL, 'r') as fl:
        content = fl.read()

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pl:
        sides = [content[i:i+len(content)//4] for i in range(0, len(content), len(content)//4)]
        '''Ділиться на 4 частини для паралелизму'''
        compressed_sides=pl.starmap(parallel_compress,[(sd,rle_compressor) for sd in sides])
        '''Cтискається 4 частини'''

    with open(COMPRESSED_FL, 'w') as fl:
        fl.write(''.join(compressed_sides))