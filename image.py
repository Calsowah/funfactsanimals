from os import path
import flickrapi
import urllib.request
import sys
import argparse
import logging

# setup for flickr API
API_KEY = u'bff907e9d6b91618733a3a67ffb82ee6' # will need to change these
API_SECRET = u'8767ee1d6b859cac'
flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

def parse():
    """ Parse command line arguments given by the user. 
        USAGE:
        python image.py --dest [path to dest folder] --animal [animal name] 
                        --tags [space-separated list of tags]
                        --start 1 --pages 1 --perpage 500 
                        --id [some download ID] --log ['info' or omit]
        Returns: a dictionary mapping the parameter names to their values
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dest', type=str, required=True, help='destination folder [required]')
    parser.add_argument('--animal', type=str, required=True, help='animal to search for [required]')
    parser.add_argument('--tags', required=True, nargs='+', help='keywords on flickr [required]')
    # optional arguments
    parser.add_argument('--start', type=int, default=1, help='start page [optional, default 1]')
    parser.add_argument('--pages', type=int, default=1, help='number of pages to parse [optional, default 1]')
    parser.add_argument('--perpage', type=int, default=500, help='# images to download per page [optional, default 500]')
    parser.add_argument('--id', type=str, default='', help='an identifier for this download [optional, default ""]')
    parser.add_argument('--log', type=str, default='', help='logging level ["info" or omit for no logging]')
    return vars(parser.parse_args())
    

def download(dest, keywords, num_pages=4, per_page=100, start_page=1, download_id=''):
    """ Downloads pictures for each animal in the keywords dictionary's key set,
        and saves them to a directory at path dir_root/[animal name]

        dest: destination folder of the images
        keywords: a dictionary mapping animal names to search keywords
        num_pages: number of pages of flickr to search
        per_page: number of photos per page - MAX IS 500
        start_page: the page on flickr to start searching for photos
        download_id: some download identifier (string). prevents images from overwriting each other
                     if downloaded to the same directory
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
            logger.info("processing page %i of %i for %s" %(i-start_page+1, num_pages, animal))

            # for each page, get the # of photos specified by per_page and load their urls
            urls = []
            xml = flickr.photos.search(api_key=API_KEY, tags=keywords[animal], 
                                       page=i, per_page=per_page,
                                       content_type=1, tag_mode='all',
                                       sort='relevance')
            photos = xml.find('photos').findall('photo')
            for j in range(len(photos)):
                try:
                    photo_id = photos[j].get('id')
                    logger.info("got photo number %i with id %s" %(j+1, photo_id))
                    url = get_url(photo_id)
                    if url: 
                        urls.append(url) # only append non-empty return values
                    logger.info("retrieved url for photo number %i with id %s" %(j+1, photo_id))
                except flickrapi.exceptions.FlickrError:
                    continue

            # download the photos on this page
            logger.info("downloading photos for " + animal)
            download_urls(urls, animal, dest, batch_id=download_id+str(i))
        
def get_url(photo_id, size='Original'):
    """
        Return the URL of the photo with ID photo_id.
        Flickr sizes include Square, Large Square, Thumbnail, Small, Small 320,
        Medium, Medium 640, Medium 800, Large, and Original.
        Returns the empty string if no URL is found.

        photo_id: string representing ID of the photo on flickr
        size: which size of photo to download. default is original
        returns: string representing the source URL of the photo
    """
    size_xml = flickr.photos.getSizes(api_key=API_KEY, photo_id=photo_id)
    # filter out everything that is not labeled w/ the input size (default: large square)
    # this should leave a list of XML objects with 1 element
    url = list(filter(
        lambda elem : elem.get('label') == size,
        size_xml.find('sizes').findall('size')
    ))
    
    # if no url for that image size was found, return an empty string
    if not url:
        return ''
    else:
        return url[0].get('source')

def download_urls(urls, animal, dest, batch_id=''):
    """
        Downloads the images at each url in the given list of urls.
        The image will be stored in the given destination folder.
        The name of the file will have the format: 
            [animal name]_[batch (optional)]_[index in url list].jpg
            for example: lion/lion_firstbatch_2.jpeg

        urls: a list of string urls that lead to animal photos
        animal: the animal name (str)
        dir_root: the destination folder for the images
        batch_id: some string used to identify this batch of URL downloads
    """
    for i in range(len(urls)):
        url = urls[i]
        logger.info('downloading url: ' + url)
        filename = animal + '_' + batch_id + '_' + str(i) + '.jpg'
        urllib.request.urlretrieve(url, path.join(dest, filename))

if __name__ == '__main__':
    # parse command line arguments
    args = parse()

    # set up logging if user wants to see log messages
    if args['log'].upper() == 'INFO':
        logger.setLevel(logging.INFO)
    
    # download images
    keywords = {args['animal']: args['tags']}
    download(args['dest'], keywords, 
             start_page=args['start'],
             per_page=args['perpage'],
             num_pages=args['pages'], 
             download_id=args['id'])