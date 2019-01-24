project ?= grow-prod
version ?= ci
webreview_api_key ?=

install:
	pip install grow
	grow install

test:
	grow build

stage:
	PATH=$(PATH):$(HOME)/bin grow stage \
	  --api-key=$(webreview_api_key)

stage-gae:
	PATH=$(PATH):$(HOME)/bin grow deploy -f prod
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(version) \
	  --verbosity=error \
	  --no-promote \
	  app.yaml

deploy:
	PATH=$(PATH):$(HOME)/bin grow deploy -f prod
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(version) \
	  --verbosity=error \
	  --promote \
	  app.yaml

run-gae:
	dev_appserver.py --allow_skipped_files=true .

enable-cloudbuild:
	gcloud services enable \
	  --project=$(project) \
	  cloudbuild.googleapis.com

cloudbuild:
	gcloud builds submit . \
	  --project=$(project) \
	  --config=cloudbuild.yaml
