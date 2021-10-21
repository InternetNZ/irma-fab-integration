help:                 ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build:                ## Create and start container
	docker-compose up --build -d

start:                ## Start the container
	docker-compose start

up-nd:	              ## Up non-detached
	docker-compose up

restart:              ## Restart the container
	docker-compose restart

stop:                 ## Stop the container
	docker-compose stop

down:                 ## Stop and remove the container
	docker-compose down

lint:                 ## Run linter
	docker-compose exec backend bash -c '/scripts/linter.sh'

lint-local:           ## Run linter using local machine applications
	./scripts/linter.sh

security:             ## Run security check
	docker-compose exec backend bash -c '/scripts/code-security-check.sh'

security-local:       ## Run security check using local machine applications
	./scripts/code-security-check.sh

package-audit:        ## Run package audit check
	docker-compose exec backend bash -c '/scripts/package-audit.sh'

package-audit-local:  ## Run package audit check using local machine applications
	./scripts/package-audit.sh

update-schemes:       ## Update IRMA schemes in container
	docker-compose exec backend bash -c 'mkdir -p ./go/irma_configuration && irma scheme download ./go/irma_configuration'


create-dynamodb-table:
	aws dynamodb create-table --endpoint-url http://localhost:8000 \
	--table-name fab-vc \
	--attribute-definitions AttributeName=id,AttributeType=S \
	--key-schema AttributeName=id,KeyType=HASH \
	--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
