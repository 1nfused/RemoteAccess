
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "generator.h"

generator_t *generator = NULL;
int generator_fd = -1;

//Init resources in virtual mem
int generator_init(){

	if(generator_release() < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	generator_fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(generator_fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = GEN_BASE_ADDR & (~(page_size - 1));

	page_off = GEN_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, GEN_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, generator_fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}

	generator = page_ptr + page_off;
	return 0;

}

//Release res
int generator_release(){
	 
	if(generator){
		if(munmap(generator, GEN_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(generator_fd >= 1){
			close(generator_fd);
			generator_fd = -1;
		}
	}
	return 0;
}

int get_generator_ptr(generator_t **generator_ptr){
	*generator_ptr = generator;
	return 0;
}