cmain: src/main.o src/server.o src/handler.py src/histogram.py src/classification.py
	gcc src/main.o src/server.o -o out/main -ljansson -lulfius
	cp src/handler.py out/handler.py
	cp src/histogram.py out/histogram.py
	cp src/classification.py out/classification.py
	
main.o: src/main.c
	gcc -c src/main.c
	
server.o: src/server.c src/server.h
	gcc -c src/server.c

clean:
	rm src/*.o
