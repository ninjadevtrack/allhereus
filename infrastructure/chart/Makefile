
all: help

help: ## Prints help for targets with comments
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

deploy-chart: ## Runs `helm upgrade` eg `make deploy-chart NAMESPACE=default INSTANCE=allhere-dev DB_PASSWORD=password EDNUDGE_USERNAME=user@nidge.com EDNUDGE_PASSWORD=passwordo IMAGE_TAG=v7b3a39d`
	@echo "going to use instance=$(INSTANCE)"
	helm upgrade "$(INSTANCE)" ./allhere --debug --namespace $(NAMESPACE) -f allhere/environments/$(INSTANCE).yaml --set secret.dbPassword=$(DB_PASSWORD),secret.ednudgeUsername=$(EDNUDGE_USERNAME),secret.ednudgePassword=$(EDNUDGE_PASSWORD),image.tag=$(IMAGE_TAG)

install-chart: ## Runs `helm install` eg make install-chart NAMESPACE=default INSTANCE=allhere-dev DB_PASSWORD=password EDNUDGE_USERNAME=user@nidge.com EDNUDGE_PASSWORD=passwordo IMAGE_TAG=v7b3a39d DJANGO_SECRET_KEY=39138**3e0
	@echo "going to use instance=$(INSTANCE)"
	helm install ./allhere --name "$(INSTANCE)" --debug --namespace $(NAMESPACE) -f allhere/environments/$(INSTANCE).yaml --set secret.dbPassword=$(DB_PASSWORD),secret.ednudgeUsername=$(EDNUDGE_USERNAME),secret.ednudgePassword=$(EDNUDGE_PASSWORD),image.tag=$(IMAGE_TAG),secret.djangoSecretKey=$(DJANGO_SECRET_KEY)
