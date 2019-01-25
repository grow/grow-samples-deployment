from google.appengine.ext import vendor
vendor.add('lib')

from google.auth import app_engine
from googleapiclient import discovery
import os
import logging
import webapp2
import yaml

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']


class CreateBuildHandler(webapp2.RequestHandler):

    def get(self):
	project_id = self.request.get('project') \
            or os.getenv('APPLICATION_ID', '').replace('s~', '')
        branch_name = self.request.get('branch') or 'master'
        repo_name = self.request.get('repo')

	credentials = app_engine.Credentials(scopes=SCOPES)
        service = discovery.build('cloudbuild', 'v1', credentials=credentials)
        cloned_body = yaml.load(open('cloudbuild.yaml'))
        body = {
            'source': {
                'repoSource': {
                    'branchName': branch_name,
                    'repoName': repo_name,
                },
            },
        }
        cloned_body.update(body)
	resp = service.projects().builds().create(
                projectId=project_id,
                body=cloned_body).execute()
        logging.info(resp)


class RunTriggerHandler(webapp2.RequestHandler):

    def get(self):
	project_id = self.request.get('project') \
            or os.getenv('APPLICATION_ID', '').replace('s~', '')
	trigger_id = self.request.get('trigger')
        branch_name = self.request.get('branch') or 'master'

        body = {
            'branchName': branch_name,
        }
	credentials = app_engine.Credentials(scopes=SCOPES)
        service = discovery.build('cloudbuild', 'v1', credentials=credentials)
	resp = service.projects().triggers().run(
                projectId=project_id,
                triggerId=trigger_id,
                body=body).execute()
        logging.info(resp)


app = webapp2.WSGIApplication([
    ('/builds/create', CreateBuildHandler),
    ('/triggers/run', RunTriggerHandler),
])
