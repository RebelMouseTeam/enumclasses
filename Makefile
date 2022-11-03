OK_COLOR=\033[32;01m
NO_COLOR=\033[0m

export PYTHONPATH:=${PWD}
version=`python -c 'import enumclasses; print(enumclasses.__version__)'`
filename=enumclasses-`python -c 'import enumclasses; print(enumclasses.__version__)'`.tar.gz

lint:
	@echo "$(OK_COLOR)==> Linting code ...$(NO_COLOR)"
	@flake8 --exclude=tests --max-line-length=160 .

test: clean
	@echo "$(OK_COLOR)==> Running tests ...$(NO_COLOR)"
	@py.test tests/* -vvv

tag:
	@echo "$(OK_COLOR)==> Creating tag $(version) ...$(NO_COLOR)"
	@git tag -a "v$(version)" -m "Version $(version)"
	@echo "$(OK_COLOR)==> Pushing tag $(version) to origin ...$(NO_COLOR)"
	@git push origin "v$(version)"

bump:
	@bumpversion --commit --tag --current-version $(version) patch enumclasses/__init__.py --allow-dirty

bump-minor:
	@bumpversion --commit --tag --current-version $(version) minor enumclasses/__init__.py --allow-dirty

clean:
	@echo "$(OK_COLOR)==> Cleaning up files that are already in .gitignore...$(NO_COLOR)"
	@for pattern in `cat .gitignore`; do find . -name "*/$$pattern" -delete; done

publish:
	@echo "$(OK_COLOR)==> Releasing package ...$(NO_COLOR)"
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
	@rm -fr build dist .egg pook.egg-info
