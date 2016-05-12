PYTHON := python

.PHONY: summary
summary: clean
	mkdir -p output
	./summary.py -d summary > output/summary.json


.PHONY: clean
clean:
	rm -rf output/*
