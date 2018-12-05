#!/usr/bin/env python

import sys
import os
import base64
import re
from six.moves import urllib

sys.path.insert(0, os.path.abspath('..'))
from imagekitio.client import Imagekit

apiKey = "Yt05Bmz0RCGbvb69lJ9IEbkhtcA="  # required
apiSecret = "HQcl+rw5UEbX68vQu4ffZo3mQwE="  # required and to be kept secret
imagekitId = "hjq03h7yv"  # required

client = Imagekit({"api_key": apiKey,
                   "api_secret": apiSecret,
                   "imagekit_id": imagekitId,
                   "use_subdomain": False,
                   "use_secure": True})

if (len(sys.argv) < 4):
    print("Usage: python make_thumbs.py <src folder> <dest folder> <animal>")
    print("src folder must contain only .jpg files")
    sys.exit()

i = 0 #index for file names
for filename in os.listdir(sys.argv[1]):
    with open(sys.argv[1] + "/" + filename, "rb") as image_file:
        try:
            img = base64.b64encode(image_file.read())
            obj = {
                "filename": sys.argv[3] + str(i) + ".jpg",
                "folder": "/"
            }
            # upload to imagekitio
            response = client.upload(img, obj)

            # get thumbnail url from imagekitio and add transformation
            url_thumb = (re.sub('/tr:n-media_library_thumbnail/', '/tr:h-50,w-50,fo-auto/', str(response.get("thumbnail"))))
            # upload image via imagekitio url to dest folder
            result = urllib.request.urlretrieve(url_thumb, os.path.join(sys.argv[2], sys.argv[3] + str(i) + ".jpg"))
            print("saved image to " + sys.argv[2] + "/" + sys.argv[3] + str(i) + ".jpg")
            i+=1

        except:
            print("ERROR on this path " + sys.argv[1] + "/" + str(filename) + " moving on....")
