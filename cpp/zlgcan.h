#pragma once

//only Support ZLG USBCAN
//Author : richard xu (junzexu@outlook.com)
//Date : Dec 02, 2026

#include <stdint.h>

//constants
#define CAN_EFF_FLAG 0x80000000u    //EFF/SFF is set in the MSB
#define CAN_RTR_FLAG 0x40000000u    //remote transmission request
#define CAN_ERR_FLAG 0x20000000u    //error message frame
#define CAN_ID_FLAG  0x1FFFFFFFu    //id

#define CAN_SEF_MASK 0x000007FFu    //standard frame format 
#define CAN_EFF_MASK 0x1FFFFFFFu    //extended frame format
#define CAN_ERR_MASK 0x1FFFFFFFu    //omit EFF, RTR, ERR flags

#define CAN_SFF_ID_BITS     11
#define CAN_EFF_ID_BITS     29

#define CAN_MAX_DLC  8
#define CAN_MAX_DLEN 8

#define TX_DELAY_SEND_FLAG 0x80 // indicate tx frame in delay send mode, 1:send in device queue; 0:send direct to bus
#define TX_ECHO_FLAG 0x20   // indicate tx frame will be echoed(recieved) when tx frame trasmit to the bus

#define CANFD_BRS 0x01  // bit rate switch (second bitrate for payload data)
#define CANFD_ESI 0x02  // error state indicator of the transmitting node

#define ZCAN_USBCAN1        3
#define ZCAN_USBCAN2        4

#define INVALID_DEVICE_HANDLE   0
#define INVALID_CHANNEL_HANDLE  0

#define ZCAN_TRANSMIT_NORMAL 0
#define ZCAN_TRANSMIT_SINGLE 1
#define ZCAN_TRANSMIT_SELFLOOP 2
#define ZCAN_TRANSMIT_SINGLE_SELFLOOP 3

#define ZCAN_ERROR_CAN_OVERFLOW        0x0001
#define ZCAN_ERROR_CAN_ERRALARM        0x0002
#define ZCAN_ERROR_CAN_PASSIVE         0x0004
#define ZCAN_ERROR_CAN_LOSE            0x0008
#define ZCAN_ERROR_CAN_BUSERR          0x0010
#define ZCAN_ERROR_CAN_BUSOFF          0x0020
#define ZCAN_ERROR_CAN_BUFFER_OVERFLOW 0x0040

#define ZCAN_ERROR_DEVICEOPENED   0x0100
#define ZCAN_ERROR_DEVICEOPEN     0x0200
#define ZCAN_ERROR_DEVICENOTOPEN  0x0400
#define ZCAN_ERROR_BUFFEROVERFLOW 0x0800
#define ZCAN_ERROR_DEVICENOTEXIST 0x1000
#define ZCAN_ERROR_LOADKERNELDLL  0x2000
#define ZCAN_ERROR_CMDFAILED      0x4000
#define ZCAN_ERROR_BUFFERCREATE   0x8000

#define ZCAN_ERROR_CANETE_PORTOPENED 0x00010000
#define ZCAN_ERROR_CANETE_INDEXUSED  0x00020000
#define ZCAN_ERROR_REF_TYPE_ID       0x00030001
#define ZCAN_ERROR_CREATE_SOCKET     0x00030002
#define ZCAN_ERROR_OPEN_CONNECT      0x00030003
#define ZCAN_ERROR_NO_STARTUP        0x00030004
#define ZCAN_ERROR_NO_CONNECTED      0x00030005
#define ZCAN_ERROR_SEND_PARTIAL      0x00030006
#define ZCAN_ERROR_SEND_TOO_FAST     0x00030007

#define STATUS_ERR              0
#define STATUS_OK               1
#define STATUS_ONLINE           2
#define STATUS_OFFLINE          3
#define STATUS_UNSUPPORTED      4
#define STATUS_BUFFER_TOO_SMALL 5

//types
enum ZcanErrorDEF {
    ZCAN_ERR_TYPE_NO_ERR            = 0,
    ZCAN_ERR_TYPE_BUS_ERR           = 1,
    ZCAN_ERR_TYPE_CONTROLLER_ERR    = 2,
    ZCAN_ERR_TYPE_DEVICE_ERR        = 3,

    ZCAN_NODE_STATE_ACTIVE          = 1,
    ZCAN_NODE_STATE_WARNNING        = 2,
    ZCAN_NODE_STATE_PASSIVE         = 3,
    ZCAN_NODE_STATE_BUSOFF          = 4,

    ZCAN_BUS_ERR_NO_ERR             = 0,
    ZCAN_BUS_ERR_BIT_ERR            = 1,
    ZCAN_BUS_ERR_ACK_ERR            = 2,
    ZCAN_BUS_ERR_CRC_ERR            = 3,
    ZCAN_BUS_ERR_FORM_ERR           = 4,
    ZCAN_BUS_ERR_STUFF_ERR          = 5,
    ZCAN_BUS_ERR_OVERLOAD_ERR       = 6,
    ZCAN_BUS_ERR_ARBITRATION_LOST   = 7,
    ZCAN_BUS_ERR_NODE_STATE_CHAGE   = 8,

    ZCAN_CONTROLLER_RX_FIFO_OVERFLOW          = 1,
    ZCAN_CONTROLLER_DRIVER_RX_BUFFER_OVERFLOW = 2,
    ZCAN_CONTROLLER_DRIVER_TX_BUFFER_OVERFLOW = 3,
    ZCAN_CONTROLLER_INTERNAL_ERROR            = 4,

    ZCAN_DEVICE_APP_RX_BUFFER_OVERFLOW = 1,
    ZCAN_DEVICE_APP_TX_BUFFER_OVERFLOW = 2,
    ZCAN_DEVICE_APP_AUTO_SEND_FAILED   = 3,
    ZCAN_CONTROLLER_TX_FRAME_INVALID   = 4,
};

typedef struct {
    char const *type;
    char const *value;
    char const *desc;
} Options;

typedef struct {
    char const *type;
    char const *desc;
    int read_only;
    char const *format;
    double min_value;
    double max_value;
    char const *unit;
    double delta;
    char const *visible;
    char const *enable;
    int editable;
    Options **options;
} Meta;

typedef struct {
    char const *key;
    char const *value;
} Pair;

typedef struct ConfigNode_ {
    char const *name;
    char const *value;
    char const *binding_value;
    char const *path;
    Meta *meta_info;
    struct ConfigNode_ **children;
    Pair **attributes;
} ConfigNode;

typedef ConfigNode const *(*GetPropertysFunc)();
typedef int (*SetValueFunc)(char const *path, char const *value);
typedef char const *(*GetValueFunc)(char const *path);

typedef struct {
    SetValueFunc SetValue;
    GetValueFunc GetValue;
    GetPropertysFunc GetPropertys;
} IProperty;

/*
* Controller Area Network Identifier structure
* bit 0-28    : CAN identifier (11/29 bit)
* bit 29    : error message frame flag (0 = data frame, 1 = error message)
* bit 30    : remote transmission request flag (1 = rtr frame)
* bit 31    : frame format flag (0 = standard 11 bit, 1 = extended 29 bit)
*/
typedef uint32_t canid_t;

/*
* Controller Area Network Error Message Frame Mask structure
* bit 0-28    : error class mask 
* bit 29-31    : set to zero
*/
typedef uint32_t can_err_mask_t;

typedef struct {
    canid_t can_id;     //32 bit MAKE_CAN_ID + EFF/RTR/ERR flags
    uint8_t can_dlc;    //frame payload length in byte (0 .. CAN_MAX_DLEN)
    uint8_t __pad;
    uint8_t __res0;
    uint8_t __res1;
    uint8_t data[CAN_MAX_DLEN];  // __attribute__((aligned(8)))
} can_frame;

typedef struct {
    uint16_t hw_Version;
    uint16_t fw_Version;
    uint16_t dr_Version;
    uint16_t in_Version;
    uint16_t irq_Num;
    uint8_t can_Num;
    char str_Serial_Num[20];
    char str_hw_Type[40];
    uint16_t reserved[4];
} ZCAN_DEVICE_INFO;

typedef struct {
    uint32_t can_type;
    union {
        struct {
            uint32_t acc_code;
            uint32_t acc_mask;
            uint32_t reserved;
            uint8_t filter;
            uint8_t timing0;
            uint8_t timing1;
            uint8_t mode;
        } can;
        struct {
            uint32_t acc_code;
            uint32_t acc_mask;
            uint32_t abit_timing;
            uint32_t dbit_timing;
            uint32_t brp;
            uint8_t filter;
            uint8_t mode;
            uint16_t pad;
            uint32_t reserved;
        } canfd;
    };
} ZCAN_CHANNEL_INIT_CONFIG;

typedef struct {
    uint32_t error_code;
    uint8_t passive_ErrData[3];
    uint8_t arLost_ErrData;
} ZCAN_CHANNEL_ERR_INFO;

typedef struct {
    can_frame frame;
    uint32_t transmit_type;
} ZCAN_Transmit_Data;

typedef struct {
    can_frame frame;
    uint64_t timestamp; //us
} ZCAN_Receive_Data;

typedef void *DEVICE_HANDLE;
typedef void *CHANNEL_HANDLE;

//macros
#define MAKE_CAN_ID(id, eff, rtr, err)  (id | (!!(eff) << 31) | (!!(rtr) << 30) | (!!(err) << 29))
#define IS_EFF(id)  (!!(id & CAN_EFF_FLAG)) //1:extend frame, 0:standard frame
#define IS_RTR(id)  (!!(id & CAN_RTR_FLAG)) //1:remote frame, 0:data frame
#define IS_ERR(id)  (!!(id & CAN_ERR_FLAG)) //1:error frame, 0:normal frame
#define GET_ID(id)  (id & CAN_ID_FLAG)
#define IS_TX_ECHO(flag) (!!(flag & TX_ECHO_FLAG))  //0: normal recieved frame, 1: tx echoed frame

typedef DEVICE_HANDLE (__stdcall *can_openDevice)(uint32_t device_type, uint32_t device_index, uint32_t reserved);
typedef uint32_t (__stdcall *can_closeDevice)(DEVICE_HANDLE device_handle);
typedef uint32_t (__stdcall *can_getDeviceInf)(DEVICE_HANDLE device_handle, ZCAN_DEVICE_INFO *pInfo);
typedef uint32_t (__stdcall *can_isDeviceOnLine)(DEVICE_HANDLE device_handle);
typedef CHANNEL_HANDLE (__stdcall *can_initCAN)(DEVICE_HANDLE device_handle, uint32_t can_index, ZCAN_CHANNEL_INIT_CONFIG *pInitConfig);
typedef uint32_t (__stdcall *can_startCAN)(CHANNEL_HANDLE channel_handle);
typedef uint32_t (__stdcall *can_resetCAN)(CHANNEL_HANDLE channel_handle);
typedef uint32_t (__stdcall *can_clearBuffer)(CHANNEL_HANDLE channel_handle);
typedef uint32_t (__stdcall *can_readChannelErrInfo)(CHANNEL_HANDLE channel_handle, ZCAN_CHANNEL_ERR_INFO *pErrInfo);
typedef uint32_t (__stdcall *can_getReceiveNum)(CHANNEL_HANDLE channel_handle, uint8_t type);
typedef uint32_t (__stdcall *can_transmit)(CHANNEL_HANDLE channel_handle, ZCAN_Transmit_Data *pTransmit, uint32_t len);
typedef uint32_t (__stdcall *can_receive)(CHANNEL_HANDLE channel_handle, ZCAN_Receive_Data *pReceive, uint32_t len, int wait_time);
typedef uint32_t (__stdcall *can_setValue)(DEVICE_HANDLE device_handle, char const *path, void const *value);
typedef void const *(__stdcall *can_getValue)(DEVICE_HANDLE device_handle, char const *path);
typedef IProperty *(__stdcall *can_getIProperty)(DEVICE_HANDLE device_handle);
typedef uint32_t (__stdcall *can_geleaseIProperty)(IProperty *pIProperty);

