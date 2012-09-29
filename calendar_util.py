#!/usr/bin/env python

import argparse
import httplib2
from apitools.auth import getCredentials
from apiclient.discovery import build
import json

def parse_cmdline():
  "parse commandline options"
  p = argparse.ArgumentParser(description="Calendar API test")
  return p.parse_args()

def events(service, calendar):
  args = {"maxResults": 1000,
          "fields": ",".join([
            "items/summary",
            "items/start/date",
            "items/recurrence",
            "nextPageToken"
          ])}
  while True:
    result = service.events().list(calendarId=calendar,**args).execute()
    args["pageToken"] = result.get("nextPageToken", "")
    for i in result["items"]: yield i
    if not args["pageToken"]: break



def main():
  args = parse_cmdline()

  c = getCredentials(".secrets/mysecrets.json", ".secrets/mytokens.dat",
                     "https://www.googleapis.com/auth/calendar")

  s = build("calendar", "v3", http=c.authorize(httplib2.Http()))

  with open(".secrets/mycalendars.json") as calfile:
    calendars = json.load(calfile)

  for cal in calendars.values():
    for e in events(s, cal):
      print(e)


if __name__ == '__main__':
  main()


# vim: set sw=2 sts=2 : #
