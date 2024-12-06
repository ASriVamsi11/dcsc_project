VERSION=v1
DOCKERUSER=srivamsia11

build:
	docker build -f Dockerfile -t ocr-backend .

push:
	docker tag ocr-backend $(DOCKERUSER)/ocr-backend:$(VERSION)
	docker push $(DOCKERUSER)/ocr-backend:$(VERSION)
	docker tag ocr-backend $(DOCKERUSER)/ocr-backend:latest
	docker push $(DOCKERUSER)/ocr-backend:latest