#!/usr/bin/env python
from __future__ import print_function
import re
import struct
import sys
try:
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

from mastodon import Mastodon

# the bulk of this code is taken from https://stackoverflow.com/a/35104372 with Mastodon-specific tweaks
# edit values as needed

mastodon = Mastodon(
    client_id='CLIENT_KEY',
    api_base_url='https://botsin.space/',
    client_secret='CLIENT SECRET',
    access_token='ACCESS TOKEN'
)
url = 'https://YOUR RADIO STREAM.url'  # edit in radio stream
encoding = 'iso-8859-1' # default: iso-8859-1 for mp3 and utf-8 for ogg streams
request = urllib2.Request(url, headers={'Icy-MetaData': 1})  # request metadata
response = urllib2.urlopen(request)
print(response.headers, file=sys.stderr)
metaint = int(response.headers['icy-metaint'])
for _ in range(10): # # title may be empty initially, try several times
    response.read(metaint)  # skip to metadata
    metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
    metadata = response.read(metadata_length).rstrip(b'\0')
    print(metadata, file=sys.stderr)
    # extract title from the metadata
    m = re.search(br"StreamTitle='([^']*)';", metadata)
    if m:
        title = m.group(1)
        if title:
            masttitle = title.decode('iso-8859-1') #encode title before sending
            result = mastodon.status_post("#NowPlaying " + masttitle + " on QCIndie.com #qcindie #regina #yqr #indierock #internetradio")
            print(result)
            break
else: 
    sys.exit('no title found')
print(title.decode(encoding, errors='replace'))
