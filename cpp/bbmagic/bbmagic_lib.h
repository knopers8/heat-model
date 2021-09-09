


#ifndef __BBMAGIC_LIB_H
#define __BBMAGIC_LIB_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef unsigned char   uint8_t ;
typedef unsigned short  uint16_t ;
typedef short           int16_t;
typedef unsigned int    uint32_t ;
typedef int             int32_t ;

//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// BBMagic MODULES DEFs
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//-BBMagic devices types
//---------------------------------------------------------------------------------------------
#define BBMAGIC_M_METEO                 1
#define BBMAGIC_M_MOTION                2
#define BBMAGIC_M_BUTTON                3
#define BBMAGIC_M_FLOOD                 4
#define BBMAGIC_M_MAGNETO               5
#define BBMAGIC_M_LINUXDEVICE           6
#define BBMAGIC_M_UART                  7
#define BBMAGIC_M_RELAY                 20
#define BBMAGIC_M_DIMMER                21
#define BBMAGIC_M_PWM                   22
#define BBMAGIC_M_BBAIR                 40

//-BBMagic METEO module
//---------------------------------------------------------------------------------------------
#define BBM_METEO_WORKTIME_0            0
#define BBM_METEO_WORKTIME_1		    1
#define BBM_METEO_WORKTIME_2		    2
#define BBM_METEO_WORKTIME_3            3
#define BBM_METEO_V_SUP			        5
#define BBM_METEO_ADV_TIME              6
#define BBM_METEO_DIN_STATE		        7
#define BBM_METEO_TEMPER_MSB		    8
#define BBM_METEO_TEMPER_LSB		    9
#define BBM_METEO_HUM		            10
#define BBM_METEO_LIGHT   			    11
#define BBM_METEO_ADC_1_MSB             12
#define BBM_METEO_ADC_1_LSB             13
#define BBM_METEO_ADC_2_MSB             14
#define BBM_METEO_ADC_2_LSB             15

//-BBMagic BUTTON module
//---------------------------------------------------------------------------------------------
#define BBM_BUTTON_SIGN_0               0
#define BBM_BUTTON_SIGN_1               1
#define BBM_BUTTON_SIGN_2		        2
#define BBM_BUTTON_SIGN_3               3
#define BBM_BUTTON_V_SUP			    5
#define BBM_BUTTON_BUTTON_FUNCTION      7
#define BBM_BUTTON_INPUT_PINS           8
#define BBM_BUTTON_CHIP_TEMP            9
#define BBM_BUTTON_LIGHT			    10
#define BBM_BUTTON_FIRM_1               14
#define BBM_BUTTON_FIRM_0               15
#define BBM_BUTTON_FN_SINGLE_CLICK      1
#define BBM_BUTTON_FN_DOUBLE_CLICK      2
#define BBM_BUTTON_FN_HOLDING           3

//-BBMagic MOTION module
//---------------------------------------------------------------------------------------------
#define BBM_MOTION_WORKTIME_0           0
#define BBM_MOTION_WORKTIME_1           1
#define BBM_MOTION_WORKTIME_2           2
#define BBM_MOTION_WORKTIME_3           3
#define BBM_MOTION_V_SUP			    5
#define BBM_MOTION_FLAGS	            7
#define BBM_MOTION_CHIP_TEMP            8
#define BBM_MOTION_LIGHT			    9
#define BBM_MOTION_ADC_1_MSB            10
#define BBM_MOTION_ADC_1_LSB            11
#define BBM_MOTION_ADC_2_MSB            12
#define BBM_MOTION_ADC_2_LSB            13
#define BBM_MOTION_FIRM_1               14
#define BBM_MOTION_FIRM_0               15
#define BBM_MOTION_ALERT_MASK           0x80

//-BBMagic FLOOD module
//---------------------------------------------------------------------------------------------
#define BBM_FLOOD_WORKTIME_0    		0
#define BBM_FLOOD_WORKTIME_1	       	1
#define BBM_FLOOD_WORKTIME_2            2
#define BBM_FLOOD_WORKTIME_3            3
#define BBM_FLOOD_V_SUP		           	5
#define BBM_FLOOD_ADV_TIME              6
#define BBM_FLOOD_ALERT_FLAGS		    7
#define BBM_FLOOD_CHIP_TEMP             8
#define BBM_FLOOD_FIRM_1                14
#define BBM_FLOOD_FIRM_0                15
#define BBM_FLOOD_ALERT_MASK            0x01

//-BBMagic MAGNETO module
//---------------------------------------------------------------------------------------------
#define BBM_MAGNETO_WORKTIME_0    		0
#define BBM_MAGNETO_WORKTIME_1	       	1
#define BBM_MAGNETO_WORKTIME_2          2
#define BBM_MAGNETO_WORKTIME_3          3
#define BBM_MAGNETO_V_SUP		        5
#define BBM_MAGNETO_ADV_TIME            6
#define BBM_MAGNETO_FLAGS		        7
#define BBM_MAGNETO_CHIP_TEMP           8
#define BBM_MAGNETO_LIGHT               9
#define BBM_MAGNETO_ADC_1_MSB           10
#define BBM_MAGNETO_ADC_1_LSB           11
#define BBM_MAGNETO_ADC_2_MSB           12
#define BBM_MAGNETO_ADC_2_LSB           13
#define BBM_MAGNETO_FIRM_1              14
#define BBM_MAGNETO_FIRM_0              15
#define BBM_MAGNETO_MAGNET_MASK         0x80
#define BBM_MAGNETO_IN_0_BIT            0x01
#define BBM_MAGNETO_IN_1_BIT            0x02
#define BBM_MAGNETO_IN_2_BIT            0x04
#define BBM_MAGNETO_IN_3_BIT            0x08

//-BBMagic RELAY module
//---------------------------------------------------------------------------------------------
#define BBM_RELAY_WORKTIME_0		    0
#define BBM_RELAY_WORKTIME_1            1
#define BBM_RELAY_WORKTIME_2		    2
#define BBM_RELAY_WORKTIME_3            3
#define BBM_RELAY_V_SUP			        5
#define BBM_RELAY_ADV_TIME              6
#define BBM_RELAYS_STATE		        7
#define BBM_RELAY_CHIP_TEMP	            8
#define BBM_RELAY_LIGHT	                9
#define BBM_RELAY_ADC_1_MSB             10
#define BBM_RELAY_ADC_1_LSB             11
#define BBM_RELAY_ADC_2_MSB             12
#define BBM_RELAY_ADC_2_LSB             13
#define BBM_RELAY_FIRM_1                14
#define BBM_RELAY_FIRM_0                15
#define REL_CH0                         1
#define REL_CH1                         2
#define REL_CH2                         4
#define REL_CH3                         8

//-BBMagic DIMMER module
//---------------------------------------------------------------------------------------------
#define BBM_DIMMER_WORKTIME_0           0
#define BBM_DIMMER_WORKTIME_1           1
#define BBM_DIMMER_WORKTIME_2           2
#define BBM_DIMMER_WORKTIME_3           3
#define BBM_DIMMER_V_SUP			    5
#define BBM_DIMMER_ADV_TIME             6
#define BBM_DIMMER_CHIP_TEMP	        7
#define BBM_DIMMER_LIGHT	            8
#define BBM_DIMMER_VAL		            9
#define BBM_DIMMER_NU_1                 10
#define BBM_DIMMER_NU_2                 11
#define BBM_DIMMER_ADC_1_MSB            12
#define BBM_DIMMER_ADC_1_LSB            13
#define BBM_DIMMER_FIRM_1               14
#define BBM_DIMMER_FIRM_0               15

//-BBMagic PWM module
//---------------------------------------------------------------------------------------------
#define BBM_PWM_WORKTIME_0              0
#define BBM_PWM_WORKTIME_1              1
#define BBM_PWM_WORKTIME_2              2
#define BBM_PWM_WORKTIME_3              3
#define BBM_PWM_V_SUP			        5
#define BBM_PWM_ADV_TIME                6
#define BBM_PWM_CHIP_TEMP	            7
#define BBM_PWM_LIGHT	                8
#define BBM_PWM_CH0		                9
#define BBM_PWM_CH1                     10
#define BBM_PWM_CH2                     11
#define BBM_PWM_ADC_1_MSB               12
#define BBM_PWM_ADC_1_LSB               13
#define BBM_PWM_FIRM_1                  14
#define BBM_PWM_FIRM_0                  15

//-BBMagic BBair smog sensor module
//---------------------------------------------------------------------------------------------
#define BBM_BBAIR_STATUS                0
#define BBM_BBAIR_MEAS_TIME             1
#define BBM_BBAIR_PERIOD                2
#define BBM_BBAIR_V_BAT                 3
#define BBM_BBAIR_TEMP_MSB              5
#define BBM_BBAIR_TEMP_LSB              6
#define BBM_BBAIR_RH                    7
#define BBM_BBAIR_PM10_MSB              8
#define BBM_BBAIR_PM10_LSB              9
#define BBM_BBAIR_PM2_5_MSB             10
#define BBM_BBAIR_PM2_5_LSB             11
#define BBM_BBAIR_PM1_MSB               12
#define BBM_BBAIR_PM1_LSB               13
#define BBM_BBAIR_FIRM_1                14
#define BBM_BBAIR_FIRM_0                15

//-BBMagic Lib buffer offsets for all devices
//---------------------------------------------------------------------------------------------
//-BBMagic device ID
#define BBMAGIC_DEVICE_TYPE		    	4
//-Bluetooth device address
#define BBMAGIC_DEVICE_ADDR_5           16
#define BBMAGIC_DEVICE_ADDR_4           17
#define BBMAGIC_DEVICE_ADDR_3           18
#define BBMAGIC_DEVICE_ADDR_2           19
#define BBMAGIC_DEVICE_ADDR_1           20
#define BBMAGIC_DEVICE_ADDR_0           21
//-Bluetooth Radio Sugnal Strength Indicator
#define BBMAGIC_DEVICE_RSSI             22
//-BBMagic Lib constants
//---------------------------------------------------------------------------------------------
//-bt addres size in bytes
#define BBM_BT_ADDR_SIZE                6
//-BBmagic_lib frame size
#define BBLIB_FRAME_SIZE                23
//-Divider to calculate module supply voltage in Volts
#define BBMAGIC_VCC_DIVIDER             71.0

//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// COMMUNICATION FUNCTIONS
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//===========================================================================================
//-Public Function: Opens BBMagic over Bluetooth communication
//led_rx_pin : number of RX LED pin, if 0 no RX LED
//led_tx_pin : number of TX LED pin, if 0 no TX LED
//led_run_pin : number of RUN LED pin, if 0 no RUN LED
//mode_flags : flags for library working mode (ex.LIB_SHOW_CONFIG | LIB_SHOW_BBAIR)
    // LIB_SHOW_CONFIG - show config messages
    // LIB_SHOW_SENSORS - show sensor messages
    // LIB_SHOW_ACTORS - show actors messages
    // LIB_SHOW_BBAIR - show BBair messages
//ret val:
// 2 - hci dev not found
// 4 - cant open hci socket
// 6 - cant bind socket
// 8 - cant set ioctl
// 22 - set scan param error
// 24 - ble scan enable error
// 26 - socket error 1
// 28 - socket error 2
// 41 - bbmagic_lib already running
// 200 - Cant export led_rx_pin
// 201 - Cant set direction for led_rx_pin
// 202 - Cant open led_rx_pin
// 203 - Cant export led_tx_pin
// 204 - Cant set direction for led_tx_pin
// 205 - Cant open led_tx_pin
// 206 - Cant export led_run_pin
// 207 - Cant set direction for led_run_pin
// 208 - Cant open led_run_pin
//===========================================================================================
    int bbm_bt_open(int led_rx_pin, int led_tx_pin, int led_run_pin, unsigned int mode_flags) ;

//===========================================================================================
//-Public Function: Closes BBMagic over Bluetooth communication
//===========================================================================================
    void bbm_bt_close(void) ;

//===========================================================================================
//-Public Function: reads data from bbmagic modules
//bbm_data : pointer to buffer for bbm frame
//ret val:
// 0 : no new data
// >0 : received message from BBMagic device: BBMAGIC_DEVICE_TYPE
// -1 : lib is closed - you should end program
//===========================================================================================
    int bbm_bt_read(uint8_t *bbm_data) ;
    
//===========================================================================================
//-Public Function: checks if bbm frame contains requested device address
// addr_ascii - twelve ascii char string - BBMagic bluetooth address
// bbm_frame - bbmagic frame
//ret val:
// 0 : addresses dont match or
// 1 : addresses are the same
//===========================================================================================
    int bbm_check_addr(const unsigned char *addr_ascii, unsigned char *bbm_frame) ;

//===========================================================================================
//-Public Function: returns version of bbm library
//ret val:
// int - bbm_bt_lib version
//===========================================================================================
    int bbm_bt_lib_version(void) ;

//===========================================================================================
//-Public Function: gets machines bluetooth address
//ret val:
//pointer to six bytes Bluetooth MAC address
//===========================================================================================
    unsigned char* bbm_bt_myaddr_get(void) ;
    
//===========================================================================================
//-Public Function: returns last two seconds BBMagic lib load info
// *min_time - min execution time in miliseconds
// *max_time - max execution time in miliseconds
//ret val:
// two seconds average library load in % : 0-100
//===========================================================================================
    unsigned char bbm_lib_get_load(float *min_time, float *max_time) ;

//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// BBMagic RELAY MODULE FUNCTIONS
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//===========================================================================================
//-Public Function: adds new BBMagic RELAY device to application database
//- name - BBMagic RELAY name - its your choice : max 64 bytes
//- addr_ascii - twelve ascii char string - BBMagic bluetooth address
//ret val:
// 0 : device added successfully
//-2 : no more resources available
//-4 : bluetooth address error - check address
//-6 : no name specified - check your device name name
//-10 : device with this bt address have been used
//===========================================================================================
    int bbm_relay_add(const unsigned char *name, const unsigned char *addr_ascii, const unsigned char *key_ascii) ;

//===========================================================================================
//-Public Function: truns on requested channels of BBMagic RELAY device
//- name - BBMagic RELAY name : max 64 bytes
//- relays - relays to switch on : REL_CH0 | REL_CH1 | REL_CH2 | REL_CH3
//ret val:
// 0 : send ok
//-2 : no BBMagic RELAY module in database with such name
// <=-20 : sending error
//===========================================================================================
    int bbm_relay_on(const unsigned char *name, uint8_t relays) ;

//===========================================================================================
//-Public Function: truns off requested channels of BBMagic RELAY device
//- name - BBMagic RELAY name : max 64 bytes
//- relays - relays to switch off : REL_CH0 | REL_CH1 | REL_CH2 | REL_CH3
//ret val:
// 0 : send ok
//-2 : no BBMagic RELAY module in database with such name
// <=-20 : sending error
//===========================================================================================
    int bbm_relay_off(const unsigned char *name, uint8_t relays) ;

//===========================================================================================
//-Public Function: get state of channel REL_CH0 of the BBMagic RELAY module
//- name : BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : channel is OFF
// 1 : channel is ON
// -2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_get_ch0(const unsigned char *name) ;

//===========================================================================================
//-Public Function: get state of channel REL_CH1 of the BBMagic RELAY module
//- name : BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : channel is OFF
// 1 : channel is ON
// -2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_get_ch1(const unsigned char *name) ;

//===========================================================================================
//-Public Function: get state of channel REL_CH2 of the BBMagic RELAY module
//- name : BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : channel is OFF
// 1 : channel is ON
// -2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_get_ch2(const unsigned char *name) ;

//===========================================================================================
//-Public Function: get state of channel REL_CH3 of the BBMagic RELAY module
//- name : BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : channel is OFF
// 1 : channel is ON
// -2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_get_ch3(const unsigned char *name) ;

//===========================================================================================
//-Public Function: complies all channels state in BBMagic RELAY module
//- bbm_msg - pointer to bbmagic message
//ret val:
// 0 : comply ok
//-2 : no BBMagic RELAY module with such address
//-4 : not comply, msg send ok
//-6 : not comply, sending error
//===========================================================================================
    int bbm_relay_comply(const unsigned char *bbm_msg) ;

//===========================================================================================
//-Public Function: set BBMagic RELAY timer
//- name - BBMagic RELAY name : max 64 bytes
//- time_s - timer value to set in seconds : max 24*3600
//ret val:
// 0 : set ok
//-2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_set_trigger(const unsigned char *name, unsigned int time_s) ;
    
//===========================================================================================
//-Public Function: clears BBMagic RELAY trigger
//- name - BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : trigger cleared
//-2 : no BBMagic RELAY module in database with such name
//===========================================================================================
    int bbm_relay_clear_trigger(const unsigned char *name) ;

//===========================================================================================
//-Public Function: checks BBMagic RELAY trigger
//- name - BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : no active trigger or no BBMagic RELAY module in database with such name
// 1 : trigger is active - time has been expired
//===========================================================================================
    int bbm_relay_is_trigger(const unsigned char *name) ;


//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// BBMagic DIMMER MODULE FUNCTIONS
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//===========================================================================================
//-Public Function: adds new BBMagic DIMEMR device to application database
//- name - BBMagic DIMMER name - its your choice : max 64 bytes
//- addr_ascii - twelve ascii char string - BBMagic bluetooth address
//ret val:
// 0 : device added successfully
//-2 : no more resources available
//-4 : bluetooth address error - check address
//-6 : no name specified - check your device name name
//-10 : device with this bt address have been used
//===========================================================================================
    int bbm_dimmer_add(const unsigned char *name, const unsigned char *addr_ascii, const unsigned char *key_ascii) ;

//===========================================================================================
//-Public Function: sets BBMagic DIMMER to requested value
//- name - BBMagic DIMMER name : max 64 bytes
//- value - value to set ; 0-100%
//ret val:
// 0 : send ok
// <0 : sending error
// <=-20 : sending error
//===========================================================================================
    int bbm_dimmer_set(const unsigned char *name, unsigned char value) ;

//===========================================================================================
//-Public Function: gets BBMagic DIMMER setting
//- name - BBMagic DIMMER name : max 64 bytes
//ret val:
// 0-100 : dimmers current setting
// -2 : no BBMagic DIMMER module in database with such name
//===========================================================================================
    int bbm_dimmer_get(const unsigned char *name) ;

//===========================================================================================
//-Public Function: tries to comply BBMagic DIMMER setting
// bbm_msg : pointer to bbmagic message
//ret val:
// 0 : comply ok
//-2 : no BBMagic DIMMER module with such address
//-4 : not comply, msg send ok
//-6 : not comply, sending error
//===========================================================================================
    int bbm_dimmer_comply(const unsigned char *bbm_msg) ;

//===========================================================================================
//-Public Function: set BBMagic DIMMER trigger
//- name - BBMagic DIMMER name : max 64 bytes
//- time_s - timer value to set in seconds : max 24*3600
//ret val:
// 0 : set ok
//-2 : no BBMagic DIMMER module in database with such name
//===========================================================================================
    int bbm_dimmer_set_trigger(const unsigned char *name, unsigned int time_s) ;
    
//===========================================================================================
//-Public Function: clears BBMagic DIMMER trigger
//- name - BBMagic DIMMER name : max 64 bytes
//ret val:
// 0 : trigger cleared
//-2 : no BBMagic DIMMER module in database with such name
//===========================================================================================
    int bbm_dimmer_clear_trigger(const unsigned char *name) ;
    
//===========================================================================================
//-Public Function: clears BBMagic DIMMER trigger
//- name - BBMagic DIMMER name : max 64 bytes
//ret val:
// 0 : trigger cleared
//-2 : no BBMagic DIMMER module in database with such name
//===========================================================================================
    int bbm_dimmer_clear_trigger(const unsigned char *name) ;

//===========================================================================================
//-Public Function: checks BBMagic DIMMER trigger
//- name - BBMagic DIMMER name : max 64 bytes
//ret val:
// 0 : no active trigger or no BBMagic DIMMER module in database with such name
// 1 : trigger is active - time has been expired
//===========================================================================================
    int bbm_dimmer_is_trigger(const unsigned char *name) ;
    
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// BBMagic PWM MODULE FUNCTIONS
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//===========================================================================================
//-Public Function: adds new BBMagic PWM device to application database
//- name - BBMagic PWM name - its your choice : max 64 bytes
//- addr_ascii - twelve ascii char string - BBMagic bluetooth address
//ret val:
// 0 : device added successfully
//-2 : no more resources available
//-4 : bluetooth address error - check address
//-6 : no name specified - check your device name name
//-10 : device with this bt address have been used
//===========================================================================================
    int bbm_pwm_add(const unsigned char *name, const unsigned char *addr_ascii, const unsigned char *key_ascii) ;

//===========================================================================================
//-Public Function: sets BBMagic PWM channels to requested valuees
//- name - BBMagic pwm name : max 64 bytes
//- ch0 - pwm channel1 0; value to set: 0-100%
//- ch1 - pwm channel1 1; value to set: 0-100%
//- ch2 - pwm channel1 2; value to set: 0-100%
//ret val:
// 0 : send ok
// <0 : sending error
//===========================================================================================
    int bbm_pwm_set(const unsigned char *name, unsigned char ch0, unsigned char ch1, unsigned char ch2) ;

//===========================================================================================
//-Public Function: gets BBMagic PWM channel 0 setting
//- name - BBMagic PWM name : max 64 bytes
//ret val:
// 0-100 : pwm current channel 0 setting
// -2 : no BBMagic PWM module in database with such name
//===========================================================================================
    int bbm_pwm_get_ch0(const unsigned char *name) ;

//===========================================================================================
//-Public Function: gets BBMagic PWM channel 1 setting
//- name - BBMagic PWM name : max 64 bytes
//ret val:
// 0-100 : pwm current channel 0 setting
// -2 : no BBMagic PWM module in database with such name
//===========================================================================================
    int bbm_pwm_get_ch1(const unsigned char *name) ;

//===========================================================================================
//-Public Function: gets BBMagic PWM channel 2 setting
//- name - BBMagic PWM name : max 64 bytes
//ret val:
// 0-100 : pwm current channel 0 setting
// -2 : no BBMagic PWM module in database with such name
//===========================================================================================
    int bbm_pwm_get_ch2(const unsigned char *name) ;

//===========================================================================================
//-Public Function: tries to comply BBMagic PWM module settings
// bbm_msg : pointer to bbmagic message
//ret val:
// 0 : comply ok
//-2 : no BBMagic PWM module with such address
//-4 : not comply, msg send ok
//-6 : not comply, sending error
//===========================================================================================
    int bbm_pwm_comply(const unsigned char *bbm_msg) ;

//===========================================================================================
//-Public Function: set BBMagic PWM trigger timer
//- name - BBMagic RELAY name : max 64 bytes
//- time_s - timer value to set in seconds : max 24*3600
//ret val:
// 0 : set ok
//-2 : no BBMagic PWM module in database with such name
//===========================================================================================
    int bbm_pwm_set_trigger(const unsigned char *name, unsigned int time_s) ;
    
//===========================================================================================
//-Public Function: clears BBMagic PWM trigger
//- name - BBMagic PWM name : max 64 bytes
//ret val:
// 0 : trigger cleared
//-2 : no BBMagic PWM module in database with such name
//===========================================================================================
    int bbm_pwm_clear_trigger(const unsigned char *name) ;

//===========================================================================================
//-Public Function: checks BBMagic PWM trigger
//- name - BBMagic RELAY name : max 64 bytes
//ret val:
// 0 : no active trigger or no BBMagic PWM module in database with such name
// 1 : trigger is active - time has been expired
//===========================================================================================
    int bbm_pwm_is_trigger(const unsigned char *name) ;

//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------
// TIME FUNCTIONS
//---------------------------------------------------------------------------------------------
//---------------------------------------------------------------------------------------------

//===========================================================================================
//-Public Function: checks if now there is requested time
// week_day_bits : day of week : SU | MO |TU | WE | TH | FR | SA or ND | PN | WT | SR | CZ | PT | SO
// f_time : time in float ex.:23.21
//ret val:
// 1 : yes, it is the time
// 0 : no, it is not the time
//===========================================================================================
    int bbm_time_is_now(uint8_t week_day_bits, float f_time) ;

//===========================================================================================
//-Public Function: checks if now is in requested boundaries
// f_start : start boundary - time in float form ex. 12:23
// f_end : end boundary - time in float form ex. 12:23
//ret val:
// 1 : yes, now is between
// 0 : no, now is not in boundaries or boundaries are out of range
//===========================================================================================
    int bbm_time_is_between(float f_start, float f_end) ;

//===========================================================================================
//-Public Function: stops program for requested miliseconds
// ms - miliseconds to sleep, max. 60000
//ret val:
//===========================================================================================
    void bbm_sleep_ms(int ms) ;
    
//===========================================================================================
//-Public Function: prints local time in requested form
// form - like strftime function:
// %H - The hour as a decimal number using a 24-hour clock (range 00 to 23)
// %I - The hour as a decimal number using a 12-hour clock (range 01 to 12)
// %p - Either "AM" or "PM" according to the given time value
// %M - The minute as a decimal number (range 00 to 59)
// %S - The second as a decimal number (range 00 to 60). (The range is up to 60 to allow for occasional leap seconds.)
// %d - The day of the month as a decimal number (range 01 to 31)
// %m - The month as a decimal number (range 01 to 12)
// %y - The year as a decimal number without a century (range 00 to 99)
// %Y - The year as a decimal number including the century.
// %j - The day of the year as a decimal number (range 001 to 366)
// %n - A newline character.
// %R - The time in 24-hour notation (%H:%M)
// %T - The time in 24-hour notation (%H:%M:%S)
//ret val:
//===========================================================================================
    void bbm_print_local_time(const char *form) ;
    

//---------------------------------------------------
#define LIB_SHOW_CONFIG                 0x01
#define LIB_SHOW_SENSORS                0x02
#define LIB_SHOW_ACTORS                 0x04
#define LIB_SHOW_BBAIR                  0x08

#define SU      0x01
#define MO      0x02
#define TU      0x04
#define WE      0x08
#define TH      0x10
#define FR      0x20
#define SA      0x40

#define ND      0x01
#define PN      0x02
#define WT      0x04
#define SR      0x08
#define CZ      0x10
#define PT      0x20
#define SO      0x40

#ifdef __cplusplus
}
#endif



#endif  //-ndef __BBMAGIC_LIB_H
