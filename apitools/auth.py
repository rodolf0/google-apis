#!/usr/bin/env python

from oauth2client.tools import run
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import OOB_CALLBACK_URN

def getCredentials(secrets_file, tokens_file, scopes):
  # create an auth flow in case we need to authenticate
  auth_flow = flow_from_clientsecrets(secrets_file, scope=scopes,
    message="Visit the APIs Console <https://code.google.com/apis/console>")
  # search for existing tokens
  storage = Storage(tokens_file)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    run(auth_flow, storage)
  return credentials



def consoleCredentials(client_id, clients_secret, tokens_file, scopes):
  # https://developers.google.com/google-apps/calendar/instantiate
  flow = OAuth2WebServerFlow(
      client_id=client_id, client_secret=clients_secret,
      scope=scopes, redirect_uri=OOB_CALLBACK_URN,
      user_agent='apitools/api-client-0.1')
  # To disable the local server feature, uncomment the following line:
  # import gflags
  # gflags.FLAGS.auth_local_webserver = False
  storage = Storage(tokens_file)
  credentials = storage.get()
  if credentials is None or credentials.invalid == True:
    if not sys.stdout.isatty():
      sys.stderr.write("OAuth2 setup requires interactive input\n")
      return None
    authorize_url = flow.step1_get_authorize_url()
    sys.stderr.write('Follow this link in your browser: %s\n' % authorize_url)
    code = raw_input('Enter verification code: ').strip()
    try:
      credentials = flow.step2_exchange(code)
    except FlowExchangeError, e:
      sys.stderr.write('Authentication has failed: %s\n' % e)
      return None
    storage.put(credentials)
    credentials.set_store(storage)
  return credentials


# vim: set sw=2 sts=2 : #
