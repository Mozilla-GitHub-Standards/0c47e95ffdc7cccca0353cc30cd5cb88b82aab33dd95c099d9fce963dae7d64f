PYTHON := python
VENV := env-$(PYTHON)


$(VENV)/bin/python:
	[ -d $(VENV) ] || $(PYTHON) -m virtualenv $(VENV) || virtualenv $(VENV)
	$(VENV)/bin/pip install --upgrade setuptools
	$(VENV)/bin/pip install -e git+https://github.com/xmindltd/xmind-sdk-python.git#egg=xmind


.PHONY: dev-env
dev-env: $(VENV)/bin/python


.PHONY: clean
clean:
	@rm -rf $(VENV)


.PHONY: clean-placeholder
clean-placeholder:
	@find summary -name "placeholder" -type f -delete
	@find bugzilla -name "placeholder" -type f -delete


.PHONY: template
template: clean-placeholder
	@mkdir -p template
	@./create_template.sh


.PHONY: summary
summary: template
	@mkdir -p output
	@rm -rf output/summary.json output/summary.xmind
	@./summary.py -d summary > output/summary.json
	@$(VENV)/bin/python summary_xmind_generator.py -i output/summary.json -o output/summary.xmind
	@echo "The summary file is generated at output/ folder."


.PHONY: ascii
ascii: template
	@$(PYTHON) ascii_diag_generator.py -s $(filter-out $@,$(MAKECMDGOALS))


.PHONY: bug2sum
bug2sum: template
	@./bug2sum.py -d $(filter-out $@,$(MAKECMDGOALS))


.PHONY: bug2sum-all
bug2sum-all: template
	@find bugzilla/ -maxdepth 1 -type d -regex ".*[0-9][\.].*" -exec ./bug2sum.py -d {} \;


# For "make ascii FOO", the "make FOO" will match here.
# force to match everything
%: force
	@:

# force do nothing
force: ;
