#!/usr/bin/env python

from os import path
import argparse
import httplib2
from apitools.auth import getCredentials
from apiclient.discovery import build
from datetime import date, datetime, time, timedelta
import json

def events(service, calendar, date=None):
  "https://developers.google.com/google-apps/calendar/v3/reference/events/list"
  args = {"maxResults": 1000,
          "fields": ",".join([
            "items/summary",
            "items/start",
            "items/status",
            "items/recurrence",
            "nextPageToken"
          ])}
  if date:
    d = datetime.combine(date, time(0, 0, 0))
    # lower bound for event's end time
    args["timeMin"] = d.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    # upper bound for event's start time
    args["timeMax"] = (d + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

  while True:
    result = service.events().list(calendarId=calendar,**args).execute()
    if "items" not in result:
      break
    for i in result["items"]:
      if i["status"] != "cancelled":
        yield i
    if "nextPageToken" in result:
      args["pageToken"] = result["nextPageToken"]
    else:
      break


def list_events(secrets, date=None):
  c = getCredentials(path.join(secrets, "mysecrets.json"),
                     path.join(secrets, "mytokens.dat"),
                     "https://www.googleapis.com/auth/calendar")
  s = build("calendar", "v3", http=c.authorize(httplib2.Http()))
  with open(path.join(secrets, "mycalendars.json")) as calfile:
    calendars = json.load(calfile)
  for cal in calendars.values():
    for e in events(s, cal, date):
      print("%s %s" % (e["start"].get("date") or e["start"].get("dateTime"), e["summary"]))


def main():
  def parse_cmdline():
    "parse commandline options"
    p = argparse.ArgumentParser(description="Calendar API test")
    p.add_argument("--secrets", required=True, help="config/secrets dir")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all-events", action="store_true")
    g.add_argument("--today", action="store_true")
    g.add_argument("--on")
    return p.parse_args()

  args = parse_cmdline()

  if args.all_events:
    list_events(args.secrets)
  elif args.today:
    list_events(args.secrets, date.today())
  elif args.on:
    list_events(args.secrets, datetime.strptime(args.on, '%Y-%m-%d').date())


if __name__ == '__main__':
  main()

# vim: set sw=2 sts=2 : #
