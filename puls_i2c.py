from posix import open, O_RDWR
from struct import unpack
from fcntl import ioctl
from ctypes import c_uint32, c_uint8, POINTER, Structure

p_uint8 = POINTER(c_uint8)

class _Message(Structure):

    _fields_ = [
        ('read_write', c_uint8),
        ('command', c_uint8),
        ('size', c_uint32),
        ('data', p_uint8)]

    __slots__ = [name for name,type in _fields_]


class I2C(object):

	I2C_SLAVE = 0x0703
	I2C_SMBUS = 0x0720
	I2C_SMBUS_WRITE = 0
	I2C_SMBUS_READ = 1
	I2C_SMBUS_BYTE_DATA = 2
	
    def __init__(self, bus):
        self._fd = open(bus, O_RDWR)
        self._address = None

    def _set_address(self, address):
        if self._address != address:
			self._address = address;
            ioctl(self._fd, I2C_SLAVE, address);

    def write(self, slave_address, register, value):
        self._set_address(slave_address)
        
		data_pointer = p_uint8(c_uint8(value))
        msg = _Message(
            read_write = I2C_SMBUS_WRITE,
			command = register,
            size = I2C_SMBUS_BYTE_DATA,
			data = data_pointer)
			
        ioctl(self._fd, I2C_SMBUS, msg)

    def read(self, slave_address, register):
        self._set_address(slave_address)
        
		data_pointer = p_uint8(c_uint8())
        msg = _Message(
            read_write = I2C_SMBUS_READ,
			command = register,
            size = I2C_SMBUS_BYTE_DATA,
			data = data_pointer)
        
		ioctl(self._fd, I2C_SMBUS, msg)

        return unpack("@b", data_pointer.contents)[0]