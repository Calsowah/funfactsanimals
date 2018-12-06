import flickrapi
import urllib.request
from os import path

# setup
DEBUG = True # set to false if you don't want print statements
API_KEY = u'bff907e9d6b91618733a3a67ffb82ee6' # will need to change these
API_SECRET = u'8767ee1d6b859cac'
flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)

def download(dir_root, keywords, num_pages=4, per_page=100, start_page=1, identifier=''):
    """ Downloads pictures for each animal in the keywords dictionary's key set,
        and saves them to a directory at path dir_root/[animal name]

        dir_root: path to the directory to save the pictures to
        keywords: a dictionary mapping animal names to search keywords
        num_pages: number of pages of flickr to search
        per_page: number of photos per page - MAX IS 500
        start_page: the page on flickr to start searching for photos
        identifier: some download identifier (string)
    """
    for animal in keywords.keys():
        # each photo object is an ElementTree object: <photo .../>
        # example response from a search call:
        # <photos page="2" pages="89" perpage="10" total="881">
        #     <photo id="2636" owner="47058503995@N01" 
        #         secret="a123456" server="2" title="test_04"
        #         ispublic="1" isfriend="0" isfamily="0" />
        #     <photo id="2635" owner="47058503995@N01"
        #         secret="b123456" server="2" title="test_03"
        #         ispublic="0" isfriend="1" isfamily="1" />
        # </photos>

        # walk through the list of search results, page by page
        for i in range(start_page, num_pages+start_page):
            if DEBUG: print("processing page %i of %i for %s" %(i-start_page+1, num_pages, animal))

            # for each page, get the # of photos specified by per_page and load their urls
            urls = []
            xml = flickr.photos.search(api_key=API_KEY, tags=keywords[animal], 
                                       page=i, per_page=per_page,
                                       content_type=1, tag_mode='all')
            photos = xml.find('photos').findall('photo')
            for j in range(len(photos)):
                try:
                    photo_id = photos[j].get('id')
                    if DEBUG: print("got photo number %i with id %s" %(j+1, photo_id))
                    url = get_url(photo_id)
                    if url: urls.append(url) # only append non-empty return values
                    if DEBUG: print("retrieved url for photo number %i with id %s" %(j+1, photo_id))
                except flickrapi.exceptions.FlickrError:
                    continue

            # download the photos on this page
            if DEBUG: print("downloading photos for " + animal)
            download_urls(urls, animal, dir_root, batch=identifier+str(i))
        
def get_url(photo_id, size='Large Square'):
    """
        Return the URL of the photo with ID photo_id.
        Flickr sizes include Square, Large Square, Thumbnail, Small, Small 320,
        Medium, Medium 640, Medium 800, Large, and Original.
        Returns the empty string if no URL is found.

        photo_id: string representing ID of the photo on flickr
        returns: string representing the source URL of the photo
    """
    size_xml = flickr.photos.getSizes(api_key=API_KEY, photo_id=photo_id)
    # filter out everything that is not labeled w/ the input size (default: large square)
    # this should leave a list of XML objects with 1 element
    url = list(filter(
        lambda elem : elem.get('label') == size,
        size_xml.find('sizes').findall('size')
    ))
    
    if not url:
        return ''
    else:
        return url[0].get('source')

def download_urls(urls, animal, dir_root, batch=''):
    """
        Downloads the images at each url in the given list of urls.
        The image will be stored in the directory: [dir_root]/[animal]
        The name of the file will have the format: 
            [animal name]_[batch (optional)]_[index in url list].jpg

        urls: a list of string urls that lead to animal photos
        animal: the animal name (str)
        dir_root: the directory that contains the folder of downloaded images
        batch: some string used to identify this batch of URL downloads
    """
    for i in range(len(urls)):
        url = urls[i]
        # saves the image to ./[dir_root]/[animal]/[animal]__[#].jpeg
        # for example: lion/lion__1.jpeg
        if DEBUG: print('downloading url: ' + url)
        urllib.request.urlretrieve(url, path.join(dir_root, animal, 
                                        animal+'_'+batch+'_'+str(i)+'.jpg'))


if __name__ == '__main__':
    VAL_ROOT   = path.join('images','validation')
    TRAIN_ROOT = path.join('images','train')
    # generally better results if you include the scientific name
    # keywords = {'bear': ['ursidae'], 'lion': ['lion', 'panthera leo']}
    kw = {'flamingo':['flamingo']}
    download(TRAIN_ROOT, kw, start_page=1,per_page=500,num_pages=1)