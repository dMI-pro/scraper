build:
	docker build -f ./Dockerfile -t scraper .

up:
	docker run --rm -it -p 8080:8080 scraper