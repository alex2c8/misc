flag: libmumu.so
	LD_LIBRARY_PATH=./ ./link_me 
mumu.o: mumu.c
	gcc -c $^ -o $@
libmumu.so: mumu.o
	gcc -shared $^ -o $@
clean:
	rm -f mumu.o libmumu.so
