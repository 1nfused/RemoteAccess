#include <stdio.h>

#include "get_reg_data.h"

// Main registers method
int main(int argc, char **argv){
	//Struct init
	house_kp_t *house_keep = NULL;
	oscilloscope_t *oscilloscope = NULL;

	//mmap init
	housekeep_init();
	oscilloscope_init();

	//Get data from ptr
	get_house_ptr(&house_keep);
	get_oscilloscope_ptr(&oscilloscope);

	printf("%d\n", oscilloscope->conf);

	//Write data to file
	//TODO

	//Release resources
	housekeep_release();
	oscilloscope_release();

	return 0;
}
