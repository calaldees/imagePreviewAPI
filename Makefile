DOCKER_IMAGE:=image_preview
DOCKER_RUN:=docker run --rm -it --publish 8000:8000

run: build
	${DOCKER_RUN} ${DOCKER_IMAGE}
build:
	docker build --tag ${DOCKER_IMAGE} .
shell:
	${DOCKER_RUN} --volume ${PWD}:/app/ ${DOCKER_IMAGE} /bin/sh
run_local:
	python3 -m sanic --host 0.0.0.0 app --single-process --debug
