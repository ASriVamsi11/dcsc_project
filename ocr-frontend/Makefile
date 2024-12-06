VERSION=v1
DOCKERUSER=srivamsia11

build:
	docker build -f Dockerfile -t ocr-frontend .
push:
	docker tag ocr-frontend $(DOCKERUSER)/ocr-frontend:$(VERSION)
	docker push $(DOCKERUSER)/ocr-frontend:$(VERSION)
	docker tag ocr-frontend $(DOCKERUSER)/ocr-frontend:latest
	docker push $(DOCKERUSER)/ocr-frontend:latest