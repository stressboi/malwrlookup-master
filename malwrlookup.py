import os
import urllib
import urllib2
import json
import csv
import sys
    
def main():

	if len(sys.argv) != 3:
		print "Usage: malwrsearch.py ip malwrinfo"
		sys.exit(0)

	ipf = sys.argv[1]
	malwrinfof = sys.argv[2]
	r = csv.reader(sys.stdin)
	w = None
  	header = []
  	first = True

  	for line in r:
    	  if first:
            header = line
            if ipf not in header or malwrinfof not in header:
        	print "missing ip or malware info field"
        	sys.exit(0)
      	    csv.writer(sys.stdout).writerow(header)
            w = csv.DictWriter(sys.stdout, header)
            first = False
            continue

    	  result = {}
    	  i = 0
    	  while i < len(header):
            if i < len(line):
              result[header[i]] = line[i]
            else:
              result[header[i]] = ''
            i += 1

          if len(result[ipf]) and len(result[malwrinfof]):
            w.writerow(result)
          elif len(result[ipf]):
            result[malwrinfof] = lookup(result[ipf])
            if len(result[malwrinfof]):
              w.writerow(result)

def lookup(ipf):
  try:
	query = ipf + " site:malwr.com"
	response = bing_search(query, limit=1)
	for i in json.loads(response)['d']['results']:
		url = i['Url']
		desc = i['Description']
	malwr=url+"|"+desc
	return malwr 
  except:
	return ''

def bing_search(query, limit=1, **kwargs):
	config = get_configuration()
	key = config['api-key']
	baseURL = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/' 
	limit = str(limit)
	query = urllib.quote(query)
        # create credential for authentication
	user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
	credentials = (':%s' % key).encode('base64')[:-1]
	auth = 'Basic %s' % credentials
	url = baseURL+'Web?Query=%27'+query+'%27&$top='+limit+'&$format=json'
	request = urllib2.Request(url)
	request.add_header('Authorization', auth)
	request.add_header('User-Agent', user_agent)
	request_opener = urllib2.build_opener()
	response = request_opener.open(request) 
	response_data = response.read()
	return response_data
    
def get_configuration():
    sourcePath = os.path.dirname(os.path.abspath(__file__))
    config_file = open(sourcePath + '/malwrsearch.config')
    return json.load(config_file)

if __name__ == '__main__':
	main()

