#!/bin/sh

# a script to compile assembly code and dump it into hex
# for one of the tasks in MP1 in CS461

echo "Starting..."
rm -f tcp.txt
gcc -c tcp.S
objdump -d tcp.o > tcp.txt
echo "Done."
