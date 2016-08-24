#include <stdint.h>

#ifndef __GENERATOR_H
#define __GENERATOR_H


#define GEN_BASE_ADDR 0x40200000
#define GEN_BASE_SIZE 0x30000

typedef struct generator_s {
	uint32_t state_machine_conf;
	uint32_t cha_scale_off;
	uint32_t cha_count_wrap;
	uint32_t cha_start_off;
	uint32_t cha_count_step;
	uint32_t reserved_regs[4];
	uint32_t chb_scale_off;
	uint32_t chb_count_wrap;
	uint32_t chb_start_off;
	uint32_t chb_count_step;
    uint32_t atAdr34;
    uint32_t atAdr38;
    uint32_t atAdr3C;
    uint32_t atAdr40;
    uint32_t atAdr44;
} generator_t;


int generator_init();
int generator_release();
int get_generator_ptr(generator_t **generator);

#endif // GENERATOR_H
