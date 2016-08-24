#include <stdint.h>

#ifndef __OSCILLOSCOPE
#define __OSCILLOSCOPE

#define OSC_BASE_ADDR 0x40100000
#define OSC_BASE_SIZE 0x30000

typedef struct oscilloscope_s {
	uint32_t conf;
	uint32_t trig_source;
	uint32_t cha_thr;
	uint32_t chb_thr;
	uint32_t trigger_delay;
	uint32_t data_dec;
	uint32_t wr_ptr_cur;
    uint32_t wr_ptr_trigger;
    uint32_t cha_hystersis;
    uint32_t chb_hystersis;
    uint32_t other;
    uint32_t reseved;
    uint32_t cha_filt_bb; 
    uint32_t cha_filt_kk;
    uint32_t cha_filt_pp;
    uint32_t chb_filt_aa;
    uint32_t chb_filt_bb;
    uint32_t chb_filt_kk;
    uint32_t chb_filt_pp;
} oscilloscope_t;


/* Function prototype definition */
int oscilloscope_init();
int oscilloscope_release();
int get_oscilloscope_ptr(oscilloscope_t **oscilloscope_ptr);

#endif // __OSCILLOSCOPE