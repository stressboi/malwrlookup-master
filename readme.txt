This is a working copy of a Python-based scripted Splunk lookup.

It uses bing to search for IP-based results in malwr.com.

To make it work...

Get a Bing API key:

http://www.bing.com/toolbox/bingsearchapi

-Make sure your search head has internet access
-Put the script (.py) in a bin directory under an app directory
-Put the config (.config) in the same directory
-Edit the config and add your Bing API key
-Edit your transforms.conf in local to include the code from the transforms here
-Restart Splunk

To test, find an IP that is known-bad like 91.211.17.201

Then you can do something like this:

index=main | head 1 | eval ip="91.211.17.201"
| lookup malwrLookup ip
| eval temp split(malwrinfo,"|")
| eval malwrurl=mvindex(temp,0)
| eval malwrdesc=mvindex(temp,1)
| table ip,malwrurl,malwrdesc

Ideally you'd have a bunch of suspect IP in your search and do a ... |stats count by ip | lookup...

brodsky@splunk.com
Cinco De Mayo 2015
