import struct
import zlib


class ZUnpack(object):
    def __init__(self, src_file, dst_file):
        self.src_file = src_file
        self.dst_file = dst_file

    @staticmethod
    def str_to_l(st):
        return struct.unpack('q', st)[0]

    def z_unpack(self):
        with open(self.src_file, 'rb') as f_src:
            with open(self.dst_file, 'wb') as f_dst:
                f_src.read(8)
                size1 = self.str_to_l(f_src.read(8))
                f_src.read(8)
                size2 = self.str_to_l(f_src.read(8))
                if size1 == -1641380927:
                    size1 = 131072L
                runs = (size2 + size1 - 1L) / size1
                array = []
                for i in range(runs):
                    array.append(f_src.read(8))
                    f_src.read(8)
                for i in range(runs):
                    to_read = array[i]
                    compressed = f_src.read(self.str_to_l(to_read))
                    decompressed = zlib.decompress(compressed)
                    f_dst.write(decompressed)

# Usage:
# this = ZUnpack('BabyDinosMod.umap.z', 'BabyDinosMod.umap')
# this.z_unpack()
