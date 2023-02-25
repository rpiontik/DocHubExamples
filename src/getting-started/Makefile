develop:
	docker run --rm -p 58080:8080 -v ./src:/usr/share/nginx/html/documentation ghcr.io/rabotaru/dochub:v2.6.2

build:
	docker build -t arc42-develop:dochub-v2.6.2 .

publish:
	sh IMAGES-REPO.env
	docker tag arc42-develop:dochub-v2.6.2 ${IMAGES_NAMESPACE}/arc42hub-getting-started:0.1-dochub-v2.6.2
	docker login ${IMAGES_NAMESPACE}
	docker push ${IMAGES_NAMESPACE}/arc42hub-getting-started:0.1-dochub-v2.6.2
