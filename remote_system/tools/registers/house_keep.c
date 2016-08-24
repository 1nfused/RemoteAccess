
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>

#include "house_keep.h"

house_kp_t *house_keep = NULL;
int fd = -1;

//Init resources in virtual mem
int init_housekeep(){

	if(release_housekeep(HK_BASE_ADDR, HK_BASE_SIZE) < -1){
		printf("Mapping resources failed.");
		return -1;
	}

	void *page_ptr;
	long page_addr, page_off, page_size = sysconf(_SC_PAGESIZE);

	/* OPEN THE DEVICE */
	fd = open("/dev/mem", O_RDWR | O_SYNC);

	if(fd  < -1){
		printf("Error opening /dev/mem\n");
		return -1;
	}

	/* Calculate page correct addresses */
	page_addr = HK_BASE_ADDR & (~(page_size - 1));

	page_off = HK_BASE_ADDR - page_addr;

	/* mmap physical memory */
	page_ptr = mmap(NULL, HK_BASE_SIZE, PROT_READ | 
		PROT_WRITE, MAP_SHARED, fd, page_addr);

	if((void *)page_ptr == MAP_FAILED){
		printf("Mapping failed.\n");
		return -1;
	}

	house_keep = page_ptr + page_off;
	return 0;

}

//Release res
int release_housekeep(){
	 
	if(house_keep){
		if(munmap(house_keep, HK_BASE_SIZE) < 0){
			printf("Unmapping failed.\n");
			return -1;
		}
		if(fd >= 1){
			close(fd);
			fd = -1;
		}
	}
	return 0;
}

int get_house_kp_ptr(house_kp_t **house_keep_ptr){
	printf("%d\n", house_keep->led_control);
	*house_keep_ptr = house_keep;
	return 0;
}