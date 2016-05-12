PYTHON := python


.PHONY: clean
clean:
	rm -rf output/*


.PHONY: summary
summary: clean
	mkdir -p output
	find summary -name "placeholder" -type f -delete
	./summary.py -d summary > output/summary.json


.PHONY: template
template:
	mkdir -p template
	./create_template_from_summary.sh

