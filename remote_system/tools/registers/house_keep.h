#include <stdint.h>

#ifndef __HOUSE_KEEP
#define __HOUSE_KEEP

/* Global address and offset definition */
#define HK_BASE_ADDR 0x40000000
#define HK_BASE_SIZE 0x30000

/* Stucture definition */
typedef struct house_keep{
	uint32_t id; //0x0
	uint32_t dna_p1; //0x4
	uint32_t dna_p2; //0x8
	uint32_t exp_c_P; //0xC
	uint32_t reserved; //0x10
	uint32_t exp_c_N; //0x14
	uint32_t exp_out_P; //0x18
	uint32_t exp_out_N; //0x1C
	uint32_t exp_c_in_P; //0x20
	uint32_t exp_c_in_N; //0x24
	uint32_t reserved2; //0x28
	uint32_t reserved3; //0x2C
	uint32_t led_control; // 0x30  [ 7: 1 RW | 0 RESERVED | 
						  // 7 > RESERVED]
} house_kp_t;

/* Function prototype definition */
int housekeep_init();
int housekeep_release();
int get_house_ptr(house_kp_t **house_keep_ptr);

#endif // __HOUSE_KEEP