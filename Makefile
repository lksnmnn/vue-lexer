test:
	coverage run --source=vue setup.py test

release:
	rm -rf build dist
	python setup.py sdist bdist_wheel
	twine upload dist/*
