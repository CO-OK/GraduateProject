build: ./install.sh ./Dockerfile
	docker build -t manjaro:v1 . --network host
run: build
	docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=${DISPLAY} -e GDK_SCALE -e GDK_DPI_SCALE  manjaro:v1  /bin/bash 

