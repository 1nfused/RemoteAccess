#include <stdio.h>
#include <stdlib.h>

#include "get_reg_data.h"

// Main registers method
int main(int argc, char **argv){

	house_kp_t *house_keep_reg = malloc(sizeof(house_kp_t));
	oscilloscope_t *oscilloscope_reg = malloc(sizeof(oscilloscope_t));
	generator_t *generator_reg = malloc(sizeof(generator_t));
	pid_controller_t *pid_controller_reg = malloc(sizeof(pid_controller_t));
	mixed_signals_t *mixed_signals_reg = malloc(sizeof(mixed_signals_t));
	daisy_chain_t *daisy_chain_reg = malloc(sizeof(daisy_chain_t));

	//mmap init
	housekeep_init();
	oscilloscope_init();
	generator_init();
	pid_control_init();
	mixed_signals_init();
	daisy_chain_init();

	//Get data from ptr
	get_house_ptr(&house_keep_reg);
	get_oscilloscope_ptr(&oscilloscope_reg);
	get_generator_ptr(&generator_reg);
	get_pid_control_ptr(&pid_controller_reg);
	get_mixed_signals_ptr(&mixed_signals_reg);
	get_daisy_chain_ptr(&daisy_chain_reg);

	//Write data to file
	FILE *file = fopen(OUTPUT_FILE, "w+");
	if (file == NULL) {
		printf("Error creating file!");
		return 1;	
	}

	//Getting bus error on writing struct to file. Adding each memeber separately...
	//Maybe change to union struct someday :D
	fprintf(file, "HOUSE KEEP\n");
	fprintf(file, "%d\n", house_keep_reg->id);
	fprintf(file, "%d\n", house_keep_reg->dna_p1);
	fprintf(file, "%d\n", house_keep_reg->dna_p2);
	fprintf(file, "%d\n", house_keep_reg->exp_c_P);
	fprintf(file, "%d\n", house_keep_reg->exp_c_N);
	fprintf(file, "%d\n", house_keep_reg->exp_out_P);
	fprintf(file, "%d\n", house_keep_reg->exp_out_N);
	fprintf(file, "%d\n", house_keep_reg->exp_c_in_P);
	fprintf(file, "%d\n", house_keep_reg->led_control);
	fprintf(file, "\n");

	fprintf(file, "OSCILLOSCOPE\n");
	fprintf(file, "%d\n", oscilloscope_reg->conf);
	fprintf(file, "%d\n", oscilloscope_reg->trig_source);
	fprintf(file, "%d\n", oscilloscope_reg->cha_thr);
	fprintf(file, "%d\n", oscilloscope_reg->chb_thr);
	fprintf(file, "%d\n", oscilloscope_reg->trigger_delay);
	fprintf(file, "%d\n", oscilloscope_reg->data_dec);
	fprintf(file, "%d\n", oscilloscope_reg->wr_ptr_cur);
	fprintf(file, "%d\n", oscilloscope_reg->wr_ptr_trigger);
	fprintf(file, "%d\n", oscilloscope_reg->cha_hystersis);
	fprintf(file, "%d\n", oscilloscope_reg->chb_hystersis);
	fprintf(file, "\n");

	fprintf(file, "GENERATOR\n");
	fprintf(file, "%d\n", generator_reg->state_machine_conf);
	fprintf(file, "%d\n", generator_reg->cha_scale_off);
	fprintf(file, "%d\n", generator_reg->cha_count_wrap);
	fprintf(file, "%d\n", generator_reg->cha_count_step);
	fprintf(file, "%d\n", generator_reg->chb_scale_off);
	fprintf(file, "%d\n", generator_reg->chb_count_wrap);
	fprintf(file, "%d\n", generator_reg->chb_start_off);
	fprintf(file, "%d\n", generator_reg->cha_scale_off);
	fprintf(file, "%d\n", generator_reg->chb_count_step);
	fprintf(file, "\n");

	fprintf(file, "PID CONTROLLER\n");
	fprintf(file, "%d\n", pid_controller_reg->pid_config);
	fprintf(file, "%d\n", pid_controller_reg->pid11_set_point);
	fprintf(file, "%d\n", pid_controller_reg->pid11_prop_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid11_integ_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid11_deriv_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid12_set_point);
	fprintf(file, "%d\n", pid_controller_reg->pid12_prop_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid12_integ_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid12_deriv_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid21_set_point);
	fprintf(file, "%d\n", pid_controller_reg->pid21_prop_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid21_integ_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid21_deriv_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid22_set_point);
	fprintf(file, "%d\n", pid_controller_reg->pid22_prop_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid22_integ_coef);
	fprintf(file, "%d\n", pid_controller_reg->pid22_deriv_coef);
	fprintf(file, "\n");

	fprintf(file, "MIXED SIGNALS\n");
	fprintf(file, "%d\n", mixed_signals_reg->xadc_aif0);
	fprintf(file, "%d\n", mixed_signals_reg->xadc_aif1);
	fprintf(file, "%d\n", mixed_signals_reg->xadc_aif2);
	fprintf(file, "%d\n", mixed_signals_reg->xadc_aif3);
	fprintf(file, "%d\n", mixed_signals_reg->pwm_dac0);
	fprintf(file, "%d\n", mixed_signals_reg->pwm_dac1);
	fprintf(file, "%d\n", mixed_signals_reg->pwm_dac2);
	fprintf(file, "%d\n", mixed_signals_reg->pwm_dac3);
	fprintf(file, "\n");

	fprintf(file, "DAISY CHAIN\n");
	fprintf(file, "%d\n", daisy_chain_reg->control);
	fprintf(file, "%d\n", daisy_chain_reg->trans_data_selector);
	fprintf(file, "%d\n", daisy_chain_reg->received_training);
	fprintf(file, "%d\n", daisy_chain_reg->received_data);
	fprintf(file, "%d\n", daisy_chain_reg->testing_control);
	fprintf(file, "%d\n", daisy_chain_reg->testing_error_counter);
	fprintf(file, "%d\n", daisy_chain_reg->testing_data_counter);
	fprintf(file, "\n");

	//Release resources
	housekeep_release();
	oscilloscope_release();
	generator_release();
	pid_control_release();
	mixed_signals_release();
	daisy_chain_release();

	fclose(file);
	return 0;
}
