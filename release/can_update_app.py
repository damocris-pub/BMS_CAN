#only Support ZLG USBCAN
#Author : richard xu (junzexu@outlook.com)
#Date : Dec 02, 2026

from ctypes import *
import threading
import time

'''
typedef void (*out_fct_type)(char character, void *buffer, size_t idx, size_t maxlen);
void register_internal_putchar(out_fct_type custom_putchar);

bool can_getDeviceInfo(char *sn);
int can_prepareCmd(uint8_t addr, uint8_t *resp);
int can_getBootloaderVerCmd(uint8_t addr, uint8_t *resp);
int can_getBatterySN(uint8_t addr, uint8_t *resp);
int can_getHardwareInfoCmd(uint8_t addr, uint8_t *resp);
int can_getHardwareTypeCmd(uint8_t addr, uint8_t *resp);
int can_getApplicationVerCmd(uint8_t addr, uint8_t *resp);
int can_getPacketLenCmd(uint8_t addr, uint8_t *resp);
int can_setPacketLenCmd(uint8_t addr, uint16_t packetLen);
int can_setApplicationLenCmd(uint8_t addr, uint32_t applicationLen, uint8_t *resp);
int can_setPacketSeqCmd(uint8_t addr, uint16_t packetSeq, uint8_t *resp);
int can_setPacketAddrCmd(uint8_t addr, uint32_t packetAddr, uint8_t *resp);
int can_sendPacketData(uint16_t packetLen, uint8_t *data);
int can_verifyPacketDataCmd(uint8_t addr, uint16_t packetCrc);
int can_verifyAllDataCmd(uint8_t addr, uint8_t crcType, uint32_t fileCrc);
int can_updateAllStationCmd(void);
int can_updateCurrentStationCmd(uint8_t addr);
__declspec(dllimport) int can_getUpdateStatusCmd(uint8_t addr, uint8_t *resp);
'''

udll = cdll.LoadLibrary('./can_update.dll')
#uint16_t crc16(uint8_t *buffer, uint32_t len, uint16_t start)
udll.crc16.argtypes = [c_char_p, c_uint32, c_uint16]
udll.crc16.restypes = c_uint16
#uint32_t crc32(uint8_t *buffer, uint32_t len, uint32_t start)
udll.crc32.argtypes = [c_char_p, c_uint32, c_uint16]
udll.crc32.restypes = c_uint32
#bool can_connect(int zlg_chan, int can_speed)
udll.can_connect.argtypes = [c_int, c_int]
udll.can_connect.restypes = c_bool
#bool can_disconnect(void)
udll.can_disconnect.restype = c_bool 


class ZCAN(object):
    def __init__(self):
        self.__dll = windll.LoadLibrary("./zlgcan.dll")
        if self.__dll == None:
            print("DLL couldn't be loaded!")

    def OpenDevice(self, device_type, device_index, reserved):
        try:
            return self.__dll.ZCAN_OpenDevice(device_type, device_index, reserved)
        except:
            print("Exception on OpenDevice!")
            raise

    def CloseDevice(self, device_handle):
        try:
            return self.__dll.ZCAN_CloseDevice(device_handle)
        except:
            print("Exception on CloseDevice!")
            raise

    def GetDeviceInf(self, device_handle):
        try:
            info = ZCAN_DEVICE_INFO()
            ret = self.__dll.ZCAN_GetDeviceInf(device_handle, byref(info))
            return info if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_GetDeviceInf")
            raise

    def DeviceOnLine(self, device_handle):
        try:
            return self.__dll.ZCAN_IsDeviceOnLine(device_handle)
        except:
            print("Exception on ZCAN_ZCAN_IsDeviceOnLine!")
            raise

    def InitCAN(self, device_handle, can_index, init_config):
        try:
            return self.__dll.ZCAN_InitCAN(device_handle, can_index, byref(init_config))
        except:
            print("Exception on ZCAN_InitCAN!")
            raise

    def StartCAN(self, chn_handle):
        try:
            return self.__dll.ZCAN_StartCAN(chn_handle)
        except:
            print("Exception on ZCAN_StartCAN!")
            raise

    def ResetCAN(self, chn_handle):
        try:
            return self.__dll.ZCAN_ResetCAN(chn_handle)
        except:
            print("Exception on ZCAN_ResetCAN!")
            raise

    def ClearBuffer(self, chn_handle):
        try:
            return self.__dll.ZCAN_ClearBuffer(chn_handle)
        except:
            print("Exception on ZCAN_ClearBuffer!")
            raise

    def ReadChannelErrInfo(self, chn_handle):
        try:
            ErrInfo = ZCAN_CHANNEL_ERR_INFO()
            ret = self.__dll.ZCAN_ReadChannelErrInfo(chn_handle, byref(ErrInfo))
            return ErrInfo if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelErrInfo!")
            raise

    def ReadChannelStatus(self, chn_handle):
        try:
            status = ZCAN_CHANNEL_STATUS()
            ret = self.__dll.ZCAN_ReadChannelStatus(chn_handle, byref(status))
            return status if ret == ZCAN_STATUS_OK else None
        except:
            print("Exception on ZCAN_ReadChannelStatus!")
            raise

    def GetReceiveNum(self, chn_handle, can_type=ZCAN_TYPE_CAN):
        try:
            return self.__dll.ZCAN_GetReceiveNum(chn_handle, can_type)
        except:
            print("Exception on ZCAN_GetReceiveNum!")
            raise

    def Transmit(self, chn_handle, std_msg, len):
        try:
            return self.__dll.ZCAN_Transmit(chn_handle, byref(std_msg), len)
        except:
            print("Exception on ZCAN_Transmit!")
            raise

    def Receive(self, chn_handle, rcv_num, wait_time=c_int(-1)):
        try:
            rcv_can_msgs = (ZCAN_Receive_Data * rcv_num)()
            ret = self.__dll.ZCAN_Receive(chn_handle, byref(rcv_can_msgs), rcv_num, wait_time)
            return rcv_can_msgs, ret
        except:
            print("Exception on ZCAN_Receive!")
            raise

    def TransmitFD(self, chn_handle, fd_msg, len):
        try:
            return self.__dll.ZCAN_TransmitFD(chn_handle, byref(fd_msg), len)
        except:
            print("Exception on ZCAN_TransmitFD!")
            raise

    def TransmitData(self, device_handle, msg, len):
        try:
            return self.__dll.ZCAN_TransmitData(device_handle, byref(msg), len)
        except:
            print("Exception on ZCAN_TransmitData!")
            raise

    def ReceiveFD(self, chn_handle, rcv_num, wait_time=c_int(-1)):
        try:
            rcv_canfd_msgs = (ZCAN_ReceiveFD_Data * rcv_num)()
            ret = self.__dll.ZCAN_ReceiveFD(chn_handle, byref(rcv_canfd_msgs), rcv_num, wait_time)
            return rcv_canfd_msgs, ret
        except:
            print("Exception on ZCAN_ReceiveF D!")
            raise

    def ReceiveData(self, device_handle, rcv_num, wait_time=c_int(-1)):
        try:
            rcv_can_data_msgs = (ZCANDataObj * rcv_num)()
            ret = self.__dll.ZCAN_ReceiveData(device_handle, byref(rcv_can_data_msgs), rcv_num, wait_time)
            return rcv_can_data_msgs, ret
        except:
            print("Exception on ZCAN_ReceiveData!")
            raise

    def GetIProperty(self, device_handle):
        try:
            self.__dll.GetIProperty.restype = POINTER(IProperty)
            return self.__dll.GetIProperty(device_handle)
        except:
            print("Exception on ZCAN_GetIProperty!")
            raise

    def SetValue(self, iproperty, path, value):
        try:
            func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(iproperty.contents.SetValue)
            return func(c_char_p(path.encode("utf-8")), c_char_p(value.encode("utf-8")))
        except:
            print("Exception on IProperty SetValue")
            raise

    def SetValue1(self, iproperty, path, value):
        try:
            func = CFUNCTYPE(c_uint, c_char_p, c_char_p)(iproperty.contents.SetValue)
            return func(c_char_p(path.encode("utf-8")), c_void_p(value))
        except:
            print("Exception on IProperty SetValue")
            raise

    def GetValue(self, iproperty, path):
        try:
            func = CFUNCTYPE(c_char_p, c_char_p)(iproperty.contents.GetValue)
            return func(c_char_p(path.encode("utf-8")))
        except:
            print("Exception on IProperty GetValue")
            raise

    def ReleaseIProperty(self, iproperty):
        try:
            return self.__dll.ReleaseIProperty(iproperty)
        except:
            print("Exception on ZCAN_ReleaseIProperty!")
            raise

    def ZCAN_SetValue(self, device_handle, path, value):
        try:
            self.__dll.ZCAN_SetValue.argtypes = [c_void_p, c_char_p, c_void_p]
            return self.__dll.ZCAN_SetValue(device_handle, path.encode("utf-8"), value)
        except:
            print("Exception on ZCAN_SetValue")
            raise

    def ZCAN_GetValue(self, device_handle, path):
        try:
            self.__dll.ZCAN_GetValue.argtypes = [c_void_p, c_char_p]
            self.__dll.ZCAN_GetValue.restype = c_void_p
            return self.__dll.ZCAN_GetValue(device_handle, path.encode("utf-8"))
        except:
            print("Exception on ZCAN_GetValue")
            raise
