
#include <stdio.h>
#include <stdlib.h>
#include "bbmagic/bbmagic_lib.h"
#include "influxdb-cpp/influxdb.hpp"

#include <iomanip>

template <typename T>
std::string to_string_hex(T number) {
    std::stringstream stream;
    stream << std::hex << number;
    return stream.str();
}

    void rec_meteo(unsigned char *bbm_buf, influxdb_cpp::server_info& si) ;

int main(int argc, char** argv)
{
    if (argc != 4) {
        printf("3 arguments expected: db name, login, password\n");
	return 1;
    }


    influxdb_cpp::server_info si("127.0.0.1", 8086, argv[1], argv[2], argv[3]);


    unsigned char bbm_buf[100] ;
    int i, bbm_id ;

    printf("\n\r======== BBMagic sensor test app ========\n\r") ;

    //-check bbmagic_lib version
    i = bbm_bt_lib_version() ;
    if(i != 0x200)
    {
        printf("bbmagic_lib version: %X - nok - stop\n\r", i) ;
        exit(1) ;
    }

    i =bbm_bt_open(0, 0, 0, LIB_SHOW_CONFIG) ;
    if(i) {
        exit(1) ;
    }

    do
    {
        bbm_id = bbm_bt_read(bbm_buf) ;
        switch( bbm_id )
        {
            case BBMAGIC_M_METEO:
                rec_meteo(bbm_buf, si) ;
            break ;
           
            default:
            break ;
        } ;

        bbm_sleep_ms(100) ;
    }while(bbm_id != -1) ;
    
    bbm_bt_close() ;
    exit(0) ;
}

//---------------------------------------------------------------
//-data from BBMagic METEO
//---------------------------------------------------------------
void rec_meteo(unsigned char *bbm_buf, influxdb_cpp::server_info& si)
{
    int i, ad1, ad2 ;
    float vcc_f, tem_f ;

    printf("BBM_METEO [") ;
    //- BT address - 6 B

    uint64_t dev_addr = 0;
    for(i=0; i<BBM_BT_ADDR_SIZE; i++) {
	dev_addr |= uint64_t(0xFF & bbm_buf[BBMAGIC_DEVICE_ADDR_5 + i]) << ((BBM_BT_ADDR_SIZE - 1 - i) * 8); 
	printf("%0.2X", bbm_buf[BBMAGIC_DEVICE_ADDR_5 + i]) ;

    }
    //- vcc
    vcc_f = (float)bbm_buf[BBM_METEO_V_SUP] ; vcc_f/=BBMAGIC_VCC_DIVIDER ;       //-calculate power suuply voltage
    printf("] < %0.2fV", vcc_f) ;
    //- RSSI
    printf(" | %ddBm", (signed char)bbm_buf[BBMAGIC_DEVICE_RSSI]) ;  //-RSSI
    printf(" >\n") ;

    //- working time
    i =bbm_buf[BBM_METEO_WORKTIME_3] ; i<<=8 ; i |=bbm_buf[BBM_METEO_WORKTIME_2] ; i<<=8 ;
    i |=bbm_buf[BBM_METEO_WORKTIME_1] ; i<<=8 ; i |=bbm_buf[BBM_METEO_WORKTIME_0] ;
    printf(" Work time: %ds\n",i) ;

    //-temperature, RH, Light, DIN
    tem_f =(float)(signed char)bbm_buf[BBM_METEO_TEMPER_MSB] ; tem_f *=256.0 ;
    tem_f +=(float)bbm_buf[BBM_METEO_TEMPER_LSB] ; tem_f /=100.0 ;  //-temperature
    printf(" T=%0.2f*C RH=%2d Light=%0.3d DIN=%0.2X", tem_f, bbm_buf[BBM_METEO_HUM], bbm_buf[BBM_METEO_LIGHT], bbm_buf[BBM_METEO_DIN_STATE]) ;

    //-adc data
    ad1 =bbm_buf[BBM_METEO_ADC_1_MSB] ; ad1 *=256 ; ad1 +=bbm_buf[BBM_METEO_ADC_1_LSB] ;
    ad2 =bbm_buf[BBM_METEO_ADC_2_MSB] ; ad2 *=256 ; ad2 +=bbm_buf[BBM_METEO_ADC_2_LSB] ;
    printf(" ADC1=%dmV ADC2=%dmV\n", ad1, ad2) ;

    //-Next message
    printf(" Next msg=%ds\n\n", bbm_buf[BBM_METEO_ADV_TIME] * 2) ;

    //for(i=0; i<BBM_BT_ADDR_SIZE; i++) fprintf(fout, "%0.2X", bbm_buf[BBMAGIC_DEVICE_ADDR_5 + i]) ;
    //fprintf(fout, ", %0.2f, %2d, %0.3d\n", tem_f, bbm_buf[BBM_METEO_HUM], bbm_buf[BBM_METEO_LIGHT]);
    //fflush(fout);
    influxdb_cpp::builder()
	    .meas("bbmeteo")
	    .tag("address", to_string_hex(dev_addr))
	    .field("temperature", tem_f)
	    .field("humidity", bbm_buf[BBM_METEO_HUM])
	    .field("brightness", bbm_buf[BBM_METEO_LIGHT]) 
	    .field("vcc", vcc_f)
	    .field("rssi", (signed char)bbm_buf[BBMAGIC_DEVICE_RSSI])
	    .field("work_time", i)
	    .field("rate", bbm_buf[BBM_METEO_ADV_TIME] * 2)
	    .post_http(si);
}
