.PHONY: get-files rm-files image clean-image run bash push pull

HOST_NAME=$(shell hostname)

REGISTRY=$(HOST_NAME):5000
REGISTRY_REMOTE=localhost:5001
DOCKER_IMAGE_V3 = planetbosman/esp32_vscode:latest
DOCKER_IMAGE_V4 = planetbosman/esp32_vscode_v4:latest
DOCKER_CONTAINER = vscode_esp32_container
BUILD_DIR = build-env

# build the image using the cache
image: 
	docker build --cache-from $(DOCKER_IMAGE_V3) --build-arg ESP_IDF_VERSION=v3.3 -t $(DOCKER_IMAGE_V3) .

image_local_cache: 
	docker build --build-arg ESP_IDF_VERSION=v3.3 -t $(DOCKER_IMAGE_V3) .


image_v4: 
	docker build --cache-from $(DOCKER_IMAGE_V3) --cache-from $(DOCKER_IMAGE_V4) --build-arg ESP_IDF_VERSION=v4.0.1 -t $(DOCKER_IMAGE_V4) .


# This empty directory '$(BUILD_DIR)' exists in git, with only an .gitignore file, set to ignore the entire contents of the dir.
# This helps to avoid committing files in that dir to git.
rm-files:
	cd $(BUILD_DIR) && \
	find . ! -name '.gitignore' -type f -exec rm -f {} + && \
	find . ! -name '.gitignore' -type d -exec rm -rf {} + > /dev/null 2>&1 ; \
	exit 0

get-files: rm-files
	# Add these archived files from external sources to the current directory.
	# Docker will automatically extract them, during image building, with the ADD command.
	echo "none required"

clean-image: rm-files get-files
	docker build --no-cache -t $(DOCKER_IMAGE_V3) .


# push in a local registry
push_v3:
	docker tag $(DOCKER_IMAGE_V3) $(REGISTRY)/$(DOCKER_IMAGE_V3)
	docker push $(REGISTRY)/$(DOCKER_IMAGE_V3)

# pull from a registry
pull_v3:
	docker pull $(REGISTRY)/$(DOCKER_IMAGE_V3)
	docker tag $(REGISTRY)/$(DOCKER_IMAGE_V3) $(DOCKER_IMAGE_V3)

pull_hub:
	docker pull $(DOCKER_IMAGE_V3)

pull_hub_v4:
	docker pull $(DOCKER_IMAGE_V4)


# transfer from remote registry into local registry
transfer_remote:
	docker pull $(REGISTRY_REMOTE)/$(DOCKER_IMAGE_V3)
	docker tag $(REGISTRY_REMOTE)/$(DOCKER_IMAGE_V3) ${DOCKER_IMAGE_V3)


docker_login:
	echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin

push_hub:
	docker push $(DOCKER_IMAGE_V3)

push_hub_v4:
	docker push $(DOCKER_IMAGE_V4)



