
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "mixed_signals.h"

mixed_signals_t *mixed_signals = NULL;
int mixed_signals_fd = -1;

//Init resources in virtual mem
int mixed_signals_init(){

	if(mixed_signals_release() < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	mixed_signals_fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(mixed_signals_fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = MS_BASE_ADDR & (~(page_size - 1));

	page_off = MS_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, MS_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, mixed_signals_fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}
	
	mixed_signals = page_ptr + page_off;

	return 0;
}

//Release res
int mixed_signals_release(){
	 
	if(mixed_signals){
		if(munmap(mixed_signals, MS_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(mixed_signals_fd >= 1){
			close(mixed_signals_fd);
			mixed_signals_fd = -1;
		}
	}
	return 0;
}

int get_mixed_signals_ptr(mixed_signals_t **mixed_signals_ptr) {
	*mixed_signals_ptr = mixed_signals;
	return 0;
}