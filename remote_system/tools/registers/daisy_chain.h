#include <stdint.h>

#ifndef __DAISY_CHAIN
#define __DAISY_CHAIN

#define DS_BASE_ADDR 0x40500000
#define DS_BASE_SIZE 0x30000

typedef struct daisy_chain_s {
	uint32_t control;
	uint32_t trans_data_selector;
	uint32_t received_training;
	uint32_t received_data;
	uint32_t testing_control;
	uint32_t testing_error_counter;
	uint32_t testing_data_counter;
} daisy_chain_t;

int daisy_chain_init();
int daisy_chain_release();
int get_daisy_chain_ptr(daisy_chain_t **daisy_chain_ptr);

#endif // __DAISY_CHAIN