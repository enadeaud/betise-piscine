PYTHON = python3
FILE = log_tonscreen.py


run :
	$(PYTHON) $(FILE)
clean :
	@rm -rf $(TMP_DIRS)
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "__pycache__" -delete
.PHONY : run