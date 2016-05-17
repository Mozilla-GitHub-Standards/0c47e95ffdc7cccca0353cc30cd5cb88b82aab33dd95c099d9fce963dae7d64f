PYTHON := python


.PHONY: clean
clean:
	@find summary -name "placeholder" -type f -delete
	@find bugzilla -name "placeholder" -type f -delete


.PHONY: template
template: clean
	@mkdir -p template
	@./create_template.sh


.PHONY: summary
summary: template
	@mkdir -p output
	@./summary.py -d summary > output/summary.json
	@echo "The summary file is generated at output/summary.json."


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
