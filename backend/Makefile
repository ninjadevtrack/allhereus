EDNUDGE_API_HOST := $(shell cat scripts/set_ednudge_api_host.sh | cut -d '=' -f2)
EDNUDGE_API_URL := https://${EDNUDGE_API_HOST}

all: help

help: ## Prints help for targets with comments
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ednudge-print-env-vars: ## Prints out whatever ENV vars we need for ednudge
	@echo "${EDNUDGE_API_URL}"

generate: ## Generates the EdNudge Python SDK using swagger-codegen
	@echo "Generating the EdNudge SDK using $(EDNUDGE_API_URL)"
	@bash ./scripts/ednudge_sdk_gen.sh $(EDNUDGE_API_URL)

install: ## Runs setup.y install for the ednudge python SDK
	@echo "Running setup.py install for ednudge SDK"
	@bash ./scripts/ednudge_sdk_python_install.sh

clean-old-sdks: ## Deletes all ednudge-sdk-python_*
	@bash ./scripts/ednudge_sdk_clean_old.sh y
