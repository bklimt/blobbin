
import httplib
import json
import config

def save_weight(weight):
  weight = weight * 2.20462
  print "Saving weight %f lbs" % weight
  data = {
    'weight': weight
  }
  headers = {
    'X-Parse-Application-Id': config.appId,
    'X-Parse-Master-Key': config.masterKey,
    'Content-Type': 'application/json',
  }
  url = '/1/classes/Weight'

  conn = httplib.HTTPSConnection('api.parse.com', 443)
  conn.connect()
  conn.request('POST', url, json.dumps(data), headers)

  result = json.loads(conn.getresponse().read())
  print "Finished saving."
  print result

