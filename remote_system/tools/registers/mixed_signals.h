#include <stdint.h>

#ifndef __MIXED_SIGNALS_H
#define __MIXED_SIGNALS_H

#define MS_BASE_ADDR 0x40400000
#define MS_BASE_SIZE 0x30000

typedef struct mixed_signals_s {
	uint32_t xadc_aif0;
	uint32_t xadc_aif1;
	uint32_t xadc_aif2;
	uint32_t xadc_aif3;
	uint32_t xadc_aif4;
	uint32_t pwm_dac0;
	uint32_t pwm_dac1;
	uint32_t pwm_dac2;
	uint32_t pwm_dac3;
} mixed_signals_t;

int mixed_signals_init();
int mixed_signals_release();
int get_mixed_signals_ptr(mixed_signals_t **mixed_signals_ptr);

#endif // __MIXED_SIGNALS_H