project ?= grow-prod

install:
	pip install -t lib -r requirements.txt

deploy:
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=auto \
	  --verbosity=error \
	  app.yaml cron.yaml
	@echo "https://console.cloud.google.com/appengine/taskqueues/cron?project=$(project)"
