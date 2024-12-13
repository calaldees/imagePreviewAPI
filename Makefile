DOCKER_IMAGE:=image_preview
DOCKER_RUN:=docker run --rm -it --publish 8000:8000 --volume ${PWD}:/app/ ${DOCKER_IMAGE}

build:
	docker build --tag ${DOCKER_IMAGE} .
run: build
	${DOCKER_RUN}
shell:
	${DOCKER_RUN} /bin/sh
