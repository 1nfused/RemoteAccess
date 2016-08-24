
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "oscilloscope.h"

oscilloscope_t *oscilloscope = NULL;
int housekeep_fd = -1;

//Init resources in virtual mem
int oscilloscope_init(){

	if(oscilloscope_release() < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	housekeep_fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(housekeep_fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = OSC_BASE_ADDR & (~(page_size - 1));

	page_off = OSC_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, OSC_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, housekeep_fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}

	oscilloscope = page_ptr + page_off;
	return 0;

}

//Release res
int oscilloscope_release(){
	 
	if(oscilloscope){
		if(munmap(oscilloscope, OSC_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(housekeep_fd >= 1){
			close(housekeep_fd);
			housekeep_fd = -1;
		}
	}
	return 0;
}

int get_oscilloscope_ptr(oscilloscope_t **oscilloscope_ptr){
	*oscilloscope_ptr = oscilloscope;
	return 0;
}