VERSION=v1
DOCKERUSER=srivamsia11

build:
	docker build -f Dockerfile -t ocr-worker .
push:
	docker tag ocr-worker $(DOCKERUSER)/ocr-worker:$(VERSION)
	docker push $(DOCKERUSER)/ocr-worker:$(VERSION)
	docker tag ocr-worker $(DOCKERUSER)/ocr-worker:latest
	docker push $(DOCKERUSER)/ocr-worker:latest