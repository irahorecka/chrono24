black: ## Black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=100;
	make clean;

github-test: ## Run pytest for every test file in GitHub Actions
	pytest -W ignore -vv .;

test: ## Run pytest for every test file
	make github-test;
	make clean;

flake8: ## Flake8 every python file
	find . -type f -name "*.py" -a | xargs flake8;

pylint: ## Pylint every python file
	find . -type f -name "*.py" -a | xargs pylint;

build: ## Build package distribution files
	flit build;

publish: ## Publish package distribution files to pypi
	flit publish;
	make clean;

clean: ## Remove package distribution files, caches, and .DS_Store
	rm -rf ./chrono24.egg-info ./dist ./build;
	find . -type d -name "__pycache__" -o -name ".pytest_cache" | xargs rm -r;
	find . -type f -name ".DS_Store" | xargs rm -r;
