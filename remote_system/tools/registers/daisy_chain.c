
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "daisy_chain.h"

daisy_chain_t *daisy_chain = NULL;
int daisy_chain_fd = -1;

//Init resources in virtual mem
int daisy_chain_init(){

	if(daisy_chain_release() < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	daisy_chain_fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(daisy_chain_fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = DS_BASE_ADDR & (~(page_size - 1));

	page_off = DS_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, DS_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, daisy_chain_fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}

	daisy_chain = page_ptr + page_off;
	return 0;

}

//Release res
int daisy_chain_release(){
	 
	if(daisy_chain){
		if(munmap(daisy_chain, DS_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(daisy_chain_fd >= 1){
			close(daisy_chain_fd);
			daisy_chain_fd = -1;
		}
	}
	return 0;
}

int get_daisy_chain_ptr(daisy_chain_t **daisy_chain_ptr){
	*daisy_chain_ptr = daisy_chain;
	return 0;
}