init:
	pip install -r requirements.txt

clean:
	rmdir /q/s build
	
setup:
	python setup.py py2exe