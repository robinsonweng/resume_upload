VENV := venv
PY_VERSION := 3.12

venv: $(VENV)/bin/activate

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

install:
	python$(PY_VERSION) -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements/prod.txt
	chmod +x git-hooks/install-git-hooks
	@git-hooks/install-git-hooks

install-dev:
	./$(VENV)/bin/pip install -r requirements/dev.txt

test: venv
	make install-dev
	./$(VENV)/bin/python3 -m pytest -v -x --pyargs resume_upload tests

mypy: venv
	make install-dev
	./$(VENV)/bin/python3 -m mypy resume_upload --show-error-context

style: venv
	make install-dev
	./$(VENV)/bin/python3 -m flake8 resume_upload

check: venv
	make install-dev
	./$(VENV)/bin/python3 -m pytest -v -x --pyargs resume_upload tests
	./$(VENV)/bin/python3 -m mypy resume_upload --show-error-context
	./$(VENV)/bin/python3 -m flake8 resume_upload

dev-run: venv
	./$(VENV)/bin/python3 -m flask --app resume_upload/main --debug run

# if make commands dont generate files, use .PHONY to ignore it
# see: https://www.gnu.org/software/make/manual/make.html#Phony-Targets.
.PHONY: clean install test run