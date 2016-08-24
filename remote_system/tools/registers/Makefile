#Cross compiler definition
CC = $(CROSS_COMPILE)gcc

CFLAGS = -g -std=gnu99 -Wall -Werror
OBJS = house_keep.o get_reg_data.o
EXECUTABLE = rp_registers

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJS)
	$(CC) -o $(EXECUTABLE) $(OBJS) $(CFLAGS)

clean:
	$(RM) *.o
	$(RM) $(OBJS)
