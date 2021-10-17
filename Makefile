#Run your file
buildImage:
	docker build . -t "${USER}"/gateway
runImage:
	docker run -p 5000:5000 -d "${USER}"/gateway

buildDC:
	docker-compose build --no-cache
runDC:
	docker-compose up -d