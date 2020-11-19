CFLAGS=-g -Wall 
LDFLAGS=-lm
CC=gcc

# "make darray", "make bstree" or "make hashset" to compile your code

darray: 
	$(CC) $(CFLAGS) -DDARRAY global.c speller.c darray.c sorting.c $(LDFLAGS) -o speller_darray 

bstree:
	$(CC) $(CFLAGS) -DBSTREE global.c speller.c bstree.c $(LDFLAGS) -o speller_bstree

hashset: 
	$(CC) $(CFLAGS) -DHASH global.c speller.c hashset.c $(LDFLAGS) -o speller_hashset


tidy:
	-rm *.o speller_darray speller_bstree speller_hashset 

.PHONY: darray bstree hashset

