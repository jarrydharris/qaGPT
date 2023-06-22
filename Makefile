# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.PHONY: find_and_del
.PHONY: check-ports

.PHONY: help
.PHONY: install
.PHONY: install-dev
.PHONY: pg-run
.PHONY: run
.PHONY: test
.PHONY: clean
.PHONY: add-dependency
.PHONY: add-dependency-dev
.PHONY: watch-dev

# Environment variable checks
ifndef PG_HOST
	$(error PG_HOST is not set (Postgres host))
else ifndef PG_PORT
	$(error PG_PORT is not set (Postgres port))
else ifndef PG_USER
  $(error PG_USER is not set (Postgres flask db owner username))
else ifndef PG_SECRET
  $(error PG_SECRET is not set (Postgres flask db owner password))
endif

# Functions
define check-ports =
$(shell netstat -l | grep $PG_PORT | wc -l)
endef

define find_and_del =
    find . -name ${1} -type ${2} | \
    xargs -I {} cp -r {} ~/.trash/ && rm -rf ${1}
endef


# Targets
install:
	@pip install -r requirements.txt

install-dev:
	@pip install -r requirements-dev.txt

pg-run:
ifeq ($(check-ports),2)
	$(error Port $PG_PORT already in use)
endif
	@docker run -itd -e POSTGRES_USER=$(PG_USER) -e POSTGRES_PASSWORD=$(PG_SECRET) -p $(PG_PORT):5432 --dbname=$(APP_ENVIRONMENT)
	@echo "Waiting for container to start..."
	@sleep 2
	@echo "Logged in to db: ${APP_ENVIRONMENT} as user: ${PG_USER}"

redis-run:
	@docker run -p 6379:6379 -it redis/redis-stack:latest

flask-run:
	@export APP_ENV='development'
	@export FLASK_APP="src.backend.app_factory:create_app('${APP_ENV}')"
	@flask run

run:
	@docker run -p 6379:6379 -it redis/redis-stack:latest
	@export APP_ENV='development'
	@export FLASK_APP="src.backend.app_factory:create_app('${APP_ENV}')"
	@flask run
	@cd src/frontend && npm run dev

test:
	@export APP_ENV='testing'
	@export FLASK_APP="src.backend.app_factory:create_app('${APP_ENV}')"
	@pytest
	@export APP_ENV='development'
	@export FLASK_APP="src.backend.app_factory:create_app('${APP_ENV}')"

clean:
	@$(call find_and_del, ".pytest_cache", "d")
	@$(call find_and_del, "__pycache__", "d")
	@$(call find_and_del, ".coverage", "f")

watch-dev:
	@watch -n 1 "cat ./logs/development.log | tail -n 15"

add:
	@bash scripts/add_py_pkg.sh $(m)

.DEFAULT_GOAL := help
help:
	@echo "Usage: make [target] $(MAKEFILE_LIST)"
	@echo "Targets:"
	@echo "  install: Install dependencies"
	@echo "  install-dev: Install development dependencies"
	@echo "  pg-run: Run Postgres container"
	@echo "  run: Run application"
	@echo "  test: Run tests"
	@echo "  clean: Clean up"
	@echo "  add-dependency: Add dependency to requirements.txt"
	@echo "  add-dependency-dev: Add dependency to requirements-dev.txt"
	@echo "  help: Show this help"
