ALL:
	./docker-login
	docker build -t revmischa/trader-aarch64 .
	docker push revmischa/trader-aarch64:latest
