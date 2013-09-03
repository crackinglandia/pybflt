from struct import unpack
from baseclasses import DataTypeBaseClass

class ReadData(object):
    """Returns a ReadData-like stream object."""
    def __init__(self, data, endianness = "<",  signed = False):
        """
        @type data: str
        @param data: The data from which we want to read.
        
        @type endianness: str
        @param endianness: (Optional) Indicates the endianness used to read the data. The C{<} indicates little-endian while C{>} indicates big-endian.
        
        @type signed: bool
        @param signed: (Optional) If set to C{True} the data will be treated as signed. If set to C{False} it will be treated as unsigned.
        """
        self.data = data
        self.offset = 0
        self.endianness = endianness
        self.signed = signed
        self.log = False

    def __len__(self):
        return len(self.data[self.offset:])
        
    def readDword(self):
        """
        Reads a dword value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The dword value read from the L{ReadData} stream.
        """
        dword = unpack(self.endianness + ('L' if not self.signed else 'l'), self.readAt(self.offset,  4))[0]
        self.offset += 4
        return dword

    def readWord(self):
        """
        Reads a word value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The word value read from the L{ReadData} stream.
        """
        word = unpack(self.endianness + ('H' if not self.signed else 'h'), self.readAt(self.offset, 2))[0]
        self.offset += 2
        return word
        
    def readByte(self):
        """
        Reads a byte value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The byte value read from the L{ReadData} stream.
        """
        byte = unpack('B' if not self.signed else 'b', self.readAt(self.offset,  1))[0]
        self.offset += 1
        return byte
    
    def readQword(self):
        """
        Reads a qword value from the L{ReadData} stream object.
        
        @rtype: int
        @return: The qword value read from the L{ReadData} stream.
        """
        qword = unpack(self.endianness + ('Q' if not self.signed else 'b'),  self.readAt(self.offset, 8))[0]
        self.offset += 8
        return qword
        
    def readString(self):
        """
        Reads an ASCII string from the L{ReadData} stream object.
        
        @rtype: str
        @return: An ASCII string read form the stream.
        """
        resultStr = ""
        while self.data[self.offset] != "\x00":
            resultStr += self.data[self.offset]
            self.offset += 1
        return resultStr

    def readAlignedString(self, align = 4):
        """ 
        Reads an ASCII string aligned to the next align-bytes boundary.
        
        @type align: int
        @param align: (Optional) The value we want the ASCII string to be aligned.
        
        @rtype: str
        @return: A 4-bytes aligned (default) ASCII string.
        """
        s = self.readString()
        r = align - len(s) % align
        while r:
            s += self.data[self.offset]
            self.offset += 1
            r -= 1
        return s
        
    def read(self, nroBytes):
        """
        Reads data from the L{ReadData} stream object.
        
        @type nroBytes: int
        @param nroBytes: The number of bytes to read.
        
        @rtype: str
        @return: A string containing the read data from the L{ReadData} stream object.
        
        @raise DataLengthException: The number of bytes tried to be read are more than the remaining in the L{ReadData} stream.
        """
        if nroBytes > len(self.data[self.offset:]):
            if self.log:
                print "Warning: Trying to read: %d bytes - only %d bytes left" % (nroBytes,  len(self.data[self.offset:]))
            nroBytes = len(self.data[self.offset:])

        resultStr = self.data[self.offset:self.offset + nroBytes]
        self.offset += nroBytes
        return resultStr
        
    def skipBytes(self, nroBytes):
        """
        Skips the specified number as parameter to the current value of the L{ReadData} stream.
        
        @type nroBytes: int
        @param nroBytes: The number of bytes to skip.        
        """
        self.offset += nroBytes
        
    def setOffset(self, value):
        """
        Sets the offset of the L{ReadData} stream object in wich the data is read.
        
        @type value: int
        @param value: Integer value that represent the offset we want to start reading in the L{ReadData} stream.
            
        @raise WrongOffsetValueException: The value is beyond the total length of the data. 
        """
        #if value >= len(self.data):
        #    raise excep.WrongOffsetValueException("Wrong offset value. Must be less than %d" % len(self.data))
        self.offset = value
    
    def readAt(self, offset, size):
        """
        Reads as many bytes indicated in the size parameter at the specific offset.

        @type offset: int
        @param offset: Offset of the value to be read.

        @type size: int
        @param size: This parameter indicates how many bytes are going to be read from a given offset.

        @rtype: str
        @return: A packed string containing the read data.
        """
        if offset > len(self.data):
            if self.log:
                print "Warning: Trying to read: %d bytes - only %d bytes left" % (nroBytes,  len(self.data[self.offset:]))
            offset = len(self.data[self.offset:])
        tmpOff = self.tell()
        self.setOffset(offset)
        r = self.read(size)
        self.setOffset(tmpOff)
        return r
        
    def tell(self):
        """
        Returns the current position of the offset in the L{ReadData} sream object.
        
        @rtype: int
        @return: The value of the current offset in the stream.
        """        
        return self.offset
        