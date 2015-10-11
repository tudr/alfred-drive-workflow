import workflow.web as request
import json
from functools import wraps
import subprocess
import os
import signal
import httplib2
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from keys import client_id, client_secret, scope, redirect_uri

from workflow import Workflow, PasswordNotFound, ICON_TRASH, ICON_WARNING, ICON_USER
flow = OAuth2WebServerFlow(client_id=client_id, client_secret=client_secret, scope=scope, redirect_uri=redirect_uri, authorization_header="approval_prompt='force'")

storage = Storage('./credentials')
wf = Workflow()

class DriveExeption(Exception):
  pass

class AuthException(Exception):
  pass

class Drive:

  @classmethod
  def verify_credentials(cls, code):
    return flow.step2_exchange(code)

  @classmethod
  def store_request_token(cls, code):
    wf.cache_data('drive_request_token', code)

  @classmethod
  def get_auth_url(cls):
    return 'login' + flow.step1_get_authorize_url()

  @classmethod
  def get_request_token(cls):
    cls.start_server()
    subprocess.call(['open', cls.get_auth_url()])

  @classmethod
  def save_credentials(cls, credentials):
    storage.put(credentials)

  @classmethod
  def get_credentials(cls):
    return storage.get()

  @classmethod
  def delete_credentials(cls):
    storage.delete()

  @classmethod
  def refresh(cls):
    try:
      wf.logger.error(1)
      user_credentials = cls.get_credentials()
      wf.logger.error(2)
      user_credentials.refresh(httplib2.Http())
      wf.logger.error(3)
      user_credentials = cls.save_credentials(user_credentials)
    except:
      wf.logger.error('Error Refreshing')
