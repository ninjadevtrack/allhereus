EDNUDGE_API_HOST := $(shell cat scripts/set_ednudge_api_host.sh | cut -d '=' -f2)
EDNUDGE_API_URL := https://api.ednudge.com
REPO := registry.gitlab.com
IMAGE_NAME := allhere/platform_v1/web
IMAGE_TAG := v$(shell if [[ ! -z "${CI_COMMIT_SHORT_SHA}" ]]; then echo "${CI_COMMIT_SHORT_SHA}"; else git rev-parse --short=8 HEAD; fi)
DJANGO_STATIC_BUCKET := "a05-allherestatic-837582"

all: help

help: ## Prints help for targets with comments
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ednudge-print-env-vars: ## Prints out whatever ENV vars we need for ednudge
	@echo "${EDNUDGE_API_URL}"

ednudge-sdk-generate: ## Generates the EdNudge Python SDK using swagger-codegen
	@echo "Generating the EdNudge SDK using $(EDNUDGE_API_URL)"
	./scripts/ednudge_sdk_gen.sh $(EDNUDGE_API_URL)

ednudge-sdk-install: ## Runs setup.y install for the ednudge python SDK
	@echo "Running setup.py install for ednudge SDK"
	./scripts/ednudge_sdk_python_install.sh

ednudge-sdk-clean-old: ## Deletes all ednudge-sdk-python_*
	./scripts/ednudge_sdk_clean_old.sh y

docker-echo-tag: ## Echos the tag that will be used for tagging the image.
	@echo "IMAGE_TAG=$(IMAGE_TAG)"

docker-build: ## Builds the Dockerfile-prod image
	@echo "Building $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)"
	docker build -t $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) -f Dockerfile-prod .

docker-ci-publish-test: ## Pushes the image to gitlab so that it can be pulled later to tag latest
	@echo "Pushing $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)"
	docker push $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) 

docker-ci-publish-final: ## Used in CI to tag the image latest and push to gitlab registry
	@echo "Pushing $(REPO)/$(IMAGE_NAME):latest"
	docker pull $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker tag $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) $(REPO)/$(IMAGE_NAME):latest
	docker push $(REPO)/$(IMAGE_NAME):latest

docker-publish: ## Pushes the image to gitlab
	@echo "Pushing $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) and latest"
	docker tag $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) $(REPO)/$(IMAGE_NAME):latest
	docker push $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG) 
	docker push $(REPO)/$(IMAGE_NAME):latest
	docker image rm -f $(REPO)/$(IMAGE_NAME):latest
	docker image rm -f $(REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

django-static-publish: ## runs python manage.py collectstatic then pushes it to s3
	@echo "running collectstatic then pushing to s3://$(DJANGO_STATIC_BUCKET)/static/$(IMAGE_TAG)/"
	docker-compose -f ../docker-compose-dev.yml exec web python manage.py collectstatic
	aws s3 sync ./django/ s3://$(DJANGO_STATIC_BUCKET)/static/$(IMAGE_TAG)/
