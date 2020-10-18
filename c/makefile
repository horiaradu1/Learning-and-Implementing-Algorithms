CFLAGS=-g -Wall -std=c99
LDFLAGS=-lm
CC=gcc

# "make darray", "make bstree" or "make hash" to compile your code

darray: 
	$(CC) $(CFLAGS) -DDARRAY $(LDFLAGS) global.c speller.c darray.c sorting.c -o speller_darray 

bstree:
	$(CC) $(CFLAGS) -DBSTREE $(LDFLAGS) global.c speller.c bstree.c -o speller_bstree

hash: 
	$(CC) $(CFLAGS) -DHASH $(LDFLAGS) global.c speller.c hashset.c -o speller_hash


tidy:
	-rm *.o speller_darray speller_bstree speller_hash 

.PHONY: darray bstree hash

