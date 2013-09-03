import bfltutils
import bfltconstants
import bfltdatatypes

class BFLTHeader(object):
    def __init__(self):
        self.magic = bfltdatatypes.DWORD(0x544c4662)
        self.rev = bfltdatatypes.DWORD()
        self.entry = bfltdatatypes.DWORD()
        self.dataStart = bfltdatatypes.DWORD()
        self.dataEnd = bfltdatatypes.DWORD()
        self.bssEnd = bfltdatatypes.DWORD()
        self.stackSize = bfltdatatypes.DWORD()
        self.relocStart = bfltdatatypes.DWORD()
        self.relocCount = bfltdatatypes.DWORD()
        self.flags = bfltdatatypes.DWORD()
        self.filler = bfltdatatypes.Array(bfltdatatypes.TYPE_DWORD)
        
        for i in range(6):
            self.filler.append(bfltdatatypes.DWORD())

    @staticmethod
    def parse(self, read_data_instance):
        bflt_header = BFLTHeader()

        bflt_header.magic = read_data_instance.readDword()
        bflt_header.rev = read_data_instance.readDword()
        bflt_header.entry = read_data_instance.readDword()
        bflt_header.dataStart = read_data_instance.readDword()
        bflt_header.dataEnd = read_data_instance.readDword()
        bflt_header.bssEnd = read_data_instance.readDword()
        bflt_header.stackSize = read_data_instance.readDword()
        bflt_header.relocStart = read_data_instance.readDword()
        bflt_header.relocCount = read_data_instance.readDword()
        bflt_header.flags = read_data_instance.readDword()
        bflt_header.filler = read_data_instance.Array(bfltdatatypes.TYPE_DWORD)

        for i in range(6):
            bflt_header.filler.append(read_data_instance.readDword())

        return bflt_header

"""
TODO:
[] add compress()/decompress().
"""
class BFLT(object):
    def __init__(self, filename = "", data = ""):

        if filename:
            self.fdata = self.read_file(filename)
        elif data:
            self.fdata = data
        else:
            raise Exception("[!] filename or data parameter must be indicated!")

        self.__parse__(self.fdata)

    def __parse__(self, raw_data):
        rd = bfltutils.ReadData(raw_data)
        self.bflt_header = BFLTHeader.parse(rd)

    def read_file(self, filename):
        data = ""
        if filename:
            try:
                fd = open(filename, "rb")
                data = fd.read()
                fd.close()
            except IOError:
                raise Exception("Error when reading file.")
        else:
            print "[!] filename was not specified"
        return data
