.PHONY: all generate install


all: generate install


generate:
	$(EJABBERDCTL_PATH)ejabberdctl help | python3 ejabberdctl_bash_completion.py > ejabberdctl

install:
	cp ejabberdctl /etc/bash_completion.d/ejabberdctl

