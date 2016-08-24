#include <stdint.h>

#ifndef PID_CONTTROLLER_H
#define PID_CONTTROLLER_H

#define PID_BASE_ADDR 0x40300000
#define PID_BASE_SIZE 0x30000

typedef struct pid_controller_s {
	uint32_t pid_config;
	uint32_t reserved[3];
	uint32_t pid11_set_point;
	uint32_t pid11_prop_coef;
	uint32_t pid11_integ_coef;
	uint32_t pid11_deriv_coef;
	uint32_t pid12_set_point;
	uint32_t pid12_prop_coef;
	uint32_t pid12_integ_coef;
	uint32_t pid12_deriv_coef;
	uint32_t pid21_set_point;
	uint32_t pid21_prop_coef;
	uint32_t pid21_integ_coef;
	uint32_t pid21_deriv_coef;
	uint32_t pid22_set_point;
	uint32_t pid22_prop_coef;
	uint32_t pid22_integ_coef;
	uint32_t pid22_deriv_coef;
} pid_controller_t;

int pid_control_init();
int pid_control_release();
int get_pid_control_ptr(pid_controller_t **pid_controller_ptr);

#endif // PID_CONTROLLER_H