REPO := registry.gitlab.com
IMAGE_NAME := allhere/platform_v1/web
IMAGE_TAG := v$(shell git rev-parse --short HEAD)

all: help

help: ## Prints help for targets with comments
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

docker-build: ## Builds the Dockerfile-prod image
	@echo "Building $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)"
	docker build -t $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile-prod .

docker-publish: ## Pushes the image to gitlab
	@echo "Pushing $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) and latest"
	docker tag $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) $(REPO)/$(IMAGE_NAME):latest
	docker push $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) 
	docker push $(REPO)/$(IMAGE_NAME):latest
	docker image rm -f $(REPO)/$(IMAGE_NAME):latest
	docker image rm -f $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

