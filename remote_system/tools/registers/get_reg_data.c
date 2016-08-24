#include <stdio.h>

#include "get_reg_data.h"

// Main registers method
int main(int argc, char **argv){
	//Struct init
	house_kp_t *house_keep = NULL;
	oscilloscope_t *oscilloscope = NULL;
	generator_t *generator = NULL;
	pid_controller_t *pid_controller = NULL;
	mixed_signals_t *mixed_signals = NULL;
	daisy_chain_t *daisy_chain = NULL;

	//mmap init
	housekeep_init();
	oscilloscope_init();
	generator_init();
	pid_control_init();
	mixed_signals_init();
	daisy_chain_init();

	//Get data from ptr
	get_house_ptr(&house_keep);
	get_oscilloscope_ptr(&oscilloscope);
	get_generator_ptr(&generator);
	get_pid_control_ptr(&pid_controller);
	get_mixed_signals_ptr(&mixed_signals);
	get_daisy_chain_ptr(&daisy_chain);

	printf("%d\n", daisy_chain->control);

	//Write data to file
	int ret_val = write_data_to_file();
	if(ret_val != 0) {
		printf("Failed to write register data to file %s\n", OUTPUT_FILE);
		return -1;
	}

	//Release resources
	housekeep_release();
	oscilloscope_release();
	generator_release();
	pid_control_release();
	mixed_signals_release();
	daisy_chain_release();

	return 0;
}

int write_data_to_file(){
	return 0;
}
