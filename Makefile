build: ./install.sh ./Dockerfile
	docker build -t manjaro:v1 . --network host
run: build
	docker run -it manjaro:v1  /bin/bash 

