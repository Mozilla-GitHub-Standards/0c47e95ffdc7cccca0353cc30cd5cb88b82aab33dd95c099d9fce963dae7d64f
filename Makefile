PYTHON := python


.PHONY: clean
clean:
	@rm -rf output/*


.PHONY: summary
summary: clean
	@mkdir -p output
	@find summary -name "placeholder" -type f -delete
	@./summary.py -d summary > output/summary.json
	echo "The summary file is generated at output/summary.json."


.PHONY: ascii
ascii:
	@find summary -name "placeholder" -type f -delete
	@$(PYTHON) ascii_diag_generator.py -s $(filter-out $@,$(MAKECMDGOALS))


.PHONY: template
template:
	@mkdir -p template
	@./create_template.sh


# For "make ascii FOO", the "make FOO" will match here.
# force to match everything
%: force
	@:

# force do nothing
force: ;
