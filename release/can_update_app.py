#please use python3 x64 version, only Support ZLG USBCAN II
#Author : richard xu (junzexu@outlook.com)
#Date : Dec 02, 2026

from ctypes import *
import threading
import time
import sys
import struct 

udll = cdll.LoadLibrary('./can_update.dll')

#uint16_t crc16(uint8_t *buffer, uint32_t len, uint16_t start)
udll.crc16.argtypes = [POINTER(c_ubyte), c_uint, c_ushort]
udll.crc16.restype = c_ushort
#uint32_t crc32(uint8_t *buffer, uint32_t len, uint32_t start)
udll.crc32.argtypes = [POINTER(c_ubyte), c_uint, c_uint]
udll.crc32.restype = c_uint
#bool can_connect(int can_chan, int can_speed)
udll.can_connect.argtypes = [c_int, c_int]
udll.can_connect.restype = c_bool
#bool can_disconnect(void)
udll.can_disconnect.restype = c_bool 
#bool can_getDeviceInfo(char *sn)
udll.can_getDeviceInfo.argtypes = [c_char_p]
udll.can_getDeviceInfo.restype = c_bool
#int can_prepareCmd(uint8_t addr, uint8_t *resp)
udll.can_prepareCmd.argtypes = [c_ubyte, c_char_p]
udll.can_prepareCmd.restype = c_int
#int can_getBootloaderVerCmd(uint8_t addr, uint8_t *resp)
udll.can_getBootloaderVerCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getBootloaderVerCmd.restype = c_int
#int can_getBatterySN(uint8_t addr, uint8_t *resp)
udll.can_getBatterySN.argtypes = [c_ubyte, c_char_p]
udll.can_getBatterySN.restype = c_int
#int can_getHardwareInfoCmd(uint8_t addr, uint8_t *resp)
udll.can_getHardwareInfoCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getHardwareInfoCmd.restype = c_int
#int can_getHardwareTypeCmd(uint8_t addr, uint8_t *resp)
udll.can_getHardwareTypeCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getHardwareTypeCmd.restype = c_int
#int can_getApplicationVerCmd(uint8_t addr, uint8_t *resp)
udll.can_getApplicationVerCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getApplicationVerCmd.restype = c_int
#int can_getPacketLenCmd(uint8_t addr, uint8_t *resp)
udll.can_getPacketLenCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getPacketLenCmd.restype = c_int
#int can_setPacketLenCmd(uint8_t addr, uint16_t packetLen)
udll.can_setPacketLenCmd.argtypes = [c_ubyte, c_ushort]
udll.can_setPacketLenCmd.restype = c_int
#int can_setApplicationLenCmd(uint8_t addr, uint32_t applicationLen, uint8_t *resp)
udll.can_setApplicationLenCmd.argtypes = [c_ubyte, c_uint, c_char_p]
udll.can_setApplicationLenCmd.restype = c_int
#int can_setPacketSeqCmd(uint8_t addr, uint16_t packetSeq, uint8_t *resp)
udll.can_setPacketSeqCmd.argtypes = [c_ubyte, c_ushort, c_char_p]
udll.can_setPacketSeqCmd.restype = c_int
#int can_setPacketAddrCmd(uint8_t addr, uint32_t packetAddr, uint8_t *resp)
udll.can_setPacketAddrCmd.argtypes = [c_ubyte, c_uint, c_char_p]
udll.can_setPacketAddrCmd.restype = c_int
#int can_sendPacketData(uint16_t packetLen, uint8_t *data)
udll.can_sendPacketData.argtypes = [c_ushort, POINTER(c_ubyte)]
udll.can_sendPacketData.restype = c_int
#int can_verifyPacketDataCmd(uint8_t addr, uint16_t packetCrc)
udll.can_verifyPacketDataCmd.argtypes = [c_ubyte, c_ushort]
udll.can_verifyPacketDataCmd.restype = c_int
#int can_verifyAllDataCmd(uint8_t addr, uint8_t crcType, uint32_t fileCrc)
udll.can_verifyAllDataCmd.argtypes = [c_ubyte, c_ubyte, c_uint]
udll.can_verifyAllDataCmd.restype = c_int
#int can_updateAllStationCmd(void)
udll.can_updateAllStationCmd.restype = c_int
#int can_updateCurrentStationCmd(uint8_t addr)
udll.can_updateCurrentStationCmd.argtypes = [c_ubyte]
udll.can_updateCurrentStationCmd.restype = c_int
#int can_getUpdateStatusCmd(uint8_t addr, uint8_t *resp)
udll.can_getUpdateStatusCmd.argtypes = [c_ubyte, c_char_p]
udll.can_getUpdateStatusCmd.restype = c_int

kZlgCanChn = 0          #0 - ZLG CAN Channel 0, 1 - ZLG CAN Channel 1
kCanSpeed = 500000      #bps
kBMSAddr = 0            #bms slave address, start from 0
kMode = 0               #0 - current station, 1 - all stations
kCrcType = 0            #0 - crc16, 1 - crc32
kPacketLen = 256        #options: 8, 16, 32, 64, 128, 256, 512
kBmsFile = "bms.dfu"

try:
    with open(kBmsFile, 'rb') as f:
        content = f.read()
except FileNotFoundError:
    print(f"cannot dfu file {kBmsFile}")

fileLen = len(content)
if ((fileLen & (kPacketLen - 1)) != 0):
    print("file length is not multiple of packetLength")
    sys.exit(1)
base_ptr = cast((c_ubyte * fileLen).from_buffer_copy(content), POINTER(c_ubyte))

print(f"target address is {kBMSAddr}, packet length is {kPacketLen}, mode is {kMode}, and crc type is {kCrcType}")
success = udll.can_connect(c_int(kZlgCanChn), c_int(kCanSpeed))
if (success != True):
    print("cannot connect zlg USBCANII")
    sys.exit(1)

sn = create_string_buffer(20)
success = udll.can_getDeviceInfo(sn)
if (success != True):
    print("cannot connect ZLG USBCAN serial number")
    sys.exit(1)
print(f"connected ZLG USBCAN II's serial number is {sn.value.decode('utf-8')}")

resp = create_string_buffer(8)
success = udll.can_getBootloaderVerCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("could not fetch LV BMS bootloader's version")
    print("Are you sure the board fw is in the dfu mode?");
    sys.exit(1)
print(f"LV BMS FW bootloader's version is {struct.unpack('B', resp[3])[0]}.{struct.unpack('B', resp[2])[0]}.{struct.unpack('B', resp[1])[0]}, build is {struct.unpack('B', resp[0])[0]}, HW is {struct.unpack('B', resp[4])[0]}")

success = udll.can_getApplicationVerCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("could not fetch LV BMS application's version")
    sys.exit(1)
var = (struct.unpack('B', resp[1])[0] << 8) | (struct.unpack('B', resp[0])[0])
print(f"LV BMS FW application's version is {struct.unpack('B', resp[4])[0]}.{struct.unpack('B', resp[3])[0]}.{struct.unpack('B', resp[2])[0]}, build is {var}")

success = udll.can_getHardwareTypeCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("could not get hardware type")
    sys.exit(1)
print(f"LV BMS's hardware type is {resp.value.decode('utf-8')}")

success = udll.can_getHardwareInfoCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("could not get hardware info")
    sys.exit(1)
year = struct.unpack('B', resp[0])[0]
month = struct.unpack('B', resp[1])[0]
day = struct.unpack('B', resp[2])[0]
var = (struct.unpack('B', resp[4])[0] << 8) | (struct.unpack('B', resp[3])[0])
print(f"LV BMS's hardware build date is year:20{year:02}, month:{month:02}, day:{day:02}, batch no: {var}")

batterySN = create_string_buffer(33)
success = udll.can_getBatterySN(c_ubyte(kBMSAddr), batterySN)
if (success < 0):
    print("could not get battery sn")
    sys.exit(1)
#print(f"LV BMS's battery sn is {batterySN.value.decode('utf-8')}")

success = udll.can_prepareCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("could not get hardware type")
    sys.exit(1)
print(f"LV BMS's cell num is {struct.unpack('B', resp[0])[0]}")

success = udll.can_setPacketLenCmd(c_ubyte(kBMSAddr), c_ushort(kPacketLen))
if (success < 0):
    print(f"try to set packet length {kPacketLen} failed")
    sys.exit(1)

success = udll.can_getPacketLenCmd(c_ubyte(kBMSAddr), resp)
if (success < 0):
    print("try to get packet length failed")
    sys.exit(1)
var = (struct.unpack('B', resp[1])[0] << 8) | (struct.unpack('B', resp[0])[0])
if (var != kPacketLen):
    print("packetLen are not equal")

success = udll.can_setApplicationLenCmd(c_ubyte(kBMSAddr), c_uint(fileLen), resp)
var = (struct.unpack('B', resp[3])[0] << 24) | (struct.unpack('B', resp[2])[0] << 16) | (struct.unpack('B', resp[1])[0] << 8) | (struct.unpack('B', resp[0])[0])
if (success < 0 or var != fileLen):
    print(f"try to set application length {fileLen} failed")
    sys.exit(1)

seq = 1
while (seq <= fileLen//kPacketLen):     #TODO: test with different sequence order
    success = udll.can_setPacketSeqCmd(c_ubyte(kBMSAddr), c_ushort(seq), resp)
    var = (struct.unpack('B', resp[1])[0] << 8) | (struct.unpack('B', resp[0])[0])
    if (success < 0 or var != seq):
        print(f"try to set packet sequence num {seq} failed")
        sys.exit(1)
    current_ptr = cast(c_void_p(addressof(base_ptr.contents) + (seq-1) * kPacketLen), POINTER(c_ubyte)) 
    success = udll.can_sendPacketData(c_ushort(kPacketLen), current_ptr)
    if (success < 0):
        print(f"try to send packet data for {seq} failed")
        sys.exit(1)
    packetCrc = udll.crc16(current_ptr, c_uint(kPacketLen), c_ushort(0xFFFF))
    print(f"packet seq {seq} 's crc is 0x{packetCrc:04x}")
    success = udll.can_verifyPacketDataCmd(c_ubyte(kBMSAddr), c_ushort(packetCrc))
    if (success < 0):
        print(f"try to verify packet crc for {seq} failed")
        sys.exit(1)
    seq = seq + 1

if (kCrcType == 0): #crc16
    fileCrc = udll.crc16(base_ptr, c_uint(fileLen), c_ushort(0xFFFF))
else:   #crc32
    fileCrc = udll.crc32(base_ptr, c_uint(fileLen), c_uint(0))
success = udll.can_verifyAllDataCmd(c_ubyte(kBMSAddr), c_ubyte(kCrcType), c_uint(fileCrc))
if (success < 0):
    print("try to set verify application failed")
    sys.exit(1)
if (kCrcType == 0): #crc16
    print(f"whole file length is {fileLen}, crc uses crc16 : 0x{fileCrc:04x}")
else:   #crc32
    print(f"whole file length is {fileLen}, crc uses crc32 : 0x{fileCrc:08x}")

if (kMode == 0):
    success = udll.can_updateCurrentStationCmd(c_ubyte(kBMSAddr))
    if (success < 0):
        print("try to update current station failed")
        sys.exit(1)
else:
    success = udll.can_updateAllStationCmd()
    if (success < 0):
        print("try to update all stations failed")
        sys.exit(1)

while (True):
    success = udll.can_getUpdateStatusCmd(c_ubyte(kBMSAddr), resp)
    if (success < 0):
        print("try to get update status failed")
        sys.exit(1)
    status = struct.unpack('B', resp[0])[0]
    if (status == 0xAA):
        print("update bms app successfully")
        break
    elif (status == 0x0C):
        print("progressing: transfer bms app internal data")
        time.sleep(0.01)
    elif (status == 0x0D):
        print("progressing: verify bms internal crc")
        time.sleep(0.01)
    else:
        print(f"update bms app failed, error code is {status}")
        sys.exit(1)

success = udll.can_disconnect()
if (success != True):
    print("cannot disconnect ZLG USBCAN II")
    sys.exit(1)
print("ZLG USBCAN II disconnected successfully")
sys.exit(0)
