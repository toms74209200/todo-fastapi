OPENAPI_SPEC =  https://raw.githubusercontent.com/toms74209200/openapi-todo-example/refs/heads/master/reference/spec.yaml

.PHONY: openapi
openapi: ## Generate rust code from OpenAPI spec
	openapi-generator-cli generate -i ${OPENAPI_SPEC} -g python-fastapi -o server