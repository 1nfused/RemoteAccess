#include <stdio.h>

#include "get_reg_data.h"

// Main registers method
int main(int argc, char **argv){
	//Struct init
	house_kp_t *house_keep = NULL;

	//mmap init
	init_housekeep();

	//Get data from ptr
	get_house_kp_ptr(&house_keep);
	printf("DATA\n");
	printf("DATA: %d\n", house_keep->led_control);

	//Write data to file
	//TODO
	return 0;
}
