#!/usr/bin/env python3
# Delete files from Slack. This is a slightly modified version of
# this gist: https://gist.github.com/jackcarter/d86808449f0d95060a40 
# 
# To run this
#
import requests
import time
import json
import argparse
import sys


def _filter_by_time(days):
  return int(time.time()) - 30 * 24 * 60 * 60


def get_user_id(token):
  uri = 'https://slack.com/api/auth.test'
  response = requests.get(uri, params={'token': token})
  data = json.loads(response.text)
  if not data['ok']:
    print("Unable to retrieve user ID!")
    print(json.dumps(data, indent=2))
    sys.exit(1)
  return data['user_id']


def list_files(token, older_than=30):
  user = get_user_id(token)
  print("Filter with user ID: {}".format(user))

  params = {
    'token': token
    ,'count': 1000
    ,'user': user
  }
  if older_than > 0:
    params['ts_to'] = _filter_by_time(older_than)
    print("Filter for files older than {} days".format(older_than))

  uri = 'https://slack.com/api/files.list'
  response = requests.get(uri, params=params)
  data = json.loads(response.text)
  if not data['ok']:
    print("Unable to get file list!")
    print(json.dumps(data, indent=2))
    sys.exit(1)

  return json.loads(response.text)['files']

def delete_files(file_ids, token):
  count = 0
  num_files = len(file_ids)
  for file_id in file_ids:
    count = count + 1
    params = {
      'token': token
      ,'file': file_id
      }
    uri = 'https://slack.com/api/files.delete'
    response = requests.get(uri, params=params)
    data = json.loads(response.text)
    print("{} of {} - {} {}".format(count, num_files, file_id, data['ok']))


if __name__ == "__main__":
  p = argparse.ArgumentParser()
  p.add_argument("-t", "--token", required=True, help="The Slack API token")
  p.add_argument("-d", "--days", required=False, default=30, type=int,
    help="Delete files older than N days. Defaults to 30 days. Specify -1 to delete all files.")

  args = p.parse_args()

  files = list_files(args.token, older_than=args.days)
  file_ids = [f['id'] for f in files]
  print("Found {} files that match the filter.".format(len(file_ids)))
  delete_files(file_ids, args.token)
