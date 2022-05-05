build: ./install.sh ./Dockerfile
	docker build -t manjaro:v1 . --network host
	//docker build -t new_manjaro . --network host
run: build
	docker run -it \
		-v /tmp/.X11-unix:/tmp/.X11-unix \
		-e DISPLAY=${DISPLAY} \
		-e GDK_SCALE \
		-e GDK_DPI_SCALE  \
		--mount type=bind,source=/run/media/v/ASS,target=/app/mount\
		manjaro:v1  /bin/bash 

# docker run -it -e DISPLAY=host.docker.internal:0.0 -e GDK_SCALE -e GDK_DPI_SCALE  manjaro:v1  /bin/bash

