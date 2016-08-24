
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "pid_controller.h"

pid_controller_t *pid_controller = NULL;
int pid_controller_fd = -1;

//Init resources in virtual mem
int pid_control_init(){

	if(pid_control_release() < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	pid_controller_fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(pid_controller_fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = PID_BASE_ADDR & (~(page_size - 1));

	page_off = PID_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, PID_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, pid_controller_fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}

	pid_controller = page_ptr + page_off;
	return 0;

}

//Release res
int pid_control_release(){
	 
	if(pid_controller){
		if(munmap(pid_controller, PID_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(pid_controller_fd >= 1){
			close(pid_controller_fd);
			pid_controller_fd = -1;
		}
	}
	return 0;
}

int get_pid_control_ptr(pid_controller_t **pid_controller_ptr) {
	*pid_controller_ptr = pid_controller;
	return 0;
}