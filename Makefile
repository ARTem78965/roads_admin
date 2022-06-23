################################################################################
# Various tools. ###############################################################
################################################################################
venv:
	# Create virtual environment.
	python3.10 -m venv venv
	./venv/bin/pip3 install --upgrade pip setuptools wheel
	./venv/bin/pip3 install -r dev.requirements.txt

clean:
	# Reset all containers and volumes.
	docker-compose -f tests.docker-compose.yml down --volumes --remove-orphans
	docker-compose -f dev.docker-compose.yml down --volumes --remove-orphans

stop:
	# Stop all containers.
	docker-compose -f tests.docker-compose.yml down --remove-orphans
	docker-compose -f dev.docker-compose.yml down --remove-orphans

format:
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a

build:
	# Build all containers.
	docker-compose -f build.docker-compose.yml build

################################################################################
# Run unit and integration tests. ##############################################
################################################################################
tests_start: stop build
	# Run containers with db`s and other common services.
	docker-compose -f tests.docker-compose.yml up -d

tests_run:
	# Run pytest.
	# ./venv/bin/bandit -r src/
	./venv/bin/pytest -x --cov=src src/tests/

tests: tests_start tests_run stop
	# Run tests.
	echo Tests finished!

################################################################################
# Run development environment. #################################################
################################################################################
dev_run: tests_start
	# Initial and run application for development.
	sh run_app.sh dev.env

dev_run_in_docker: stop build
	docker-compose -f dev.docker-compose.yml up
