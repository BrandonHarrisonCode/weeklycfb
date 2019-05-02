build:
	docker build --tag=expectedpoints .

run: build
	docker run --rm --interactive --tty --mount source=PBPData,destination=/usr/src/app/data,readonly --mount source=output,destination=/usr/src/app/output expectedpoints
