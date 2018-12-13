#Use command 'export PYTHONIOENCODING=UTF-8' prior to running this script
#if run from terminal

import urllib
from bs4 import BeautifulSoup
from bs4 import NavigableString

import requests
import webbrowser

FUN_FACT_DELIMITER = 'Did you know:'
SNIPPET_ID = 'rhs_block'
GOOGLE_SEARCH_URL = 'https://google.com/search?q='

def getFunFacts(funFactSubject):
    #first check if Google has a designated fun fact category
    text = funFactSubject + '/fun facts'
    text = urllib.parse.quote_plus(text)

    url = GOOGLE_SEARCH_URL + text

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    allSnippetSections = []
    #allFunFacts = []
    for section in soup.find_all(id=SNIPPET_ID):
       allSnippetSections.append(section.text)

    for snippet in allSnippetSections:
        funFactStartIndex = snippet.find(FUN_FACT_DELIMITER)
        funFactEndIndex = snippet.find('.', funFactStartIndex, -1)
        currentFunFact = snippet[funFactStartIndex + len(FUN_FACT_DELIMITER):funFactEndIndex].strip()
        # print (snippet[funFactStartIndex + len(FUN_FACT_DELIMITER):funFactEndIndex].strip())

        #return first fun fact if exists
        if currentFunFact != '':
            return ((snippet[funFactStartIndex + len(FUN_FACT_DELIMITER):funFactEndIndex]).strip())
        #if we need multiple fun facts later, we can put them all into a list
        #allFunFacts.append((snippet[funFactStartIndex + len(FUN_FACT_DELIMITER):funFactEndIndex]).strip())

    funFact = scrapeForFunFacts(soup, funFactSubject)
    if funFact != '':
        return funFact

    return '' #if everything is sad and we cant find anything... just give up

#scrape for fun facts given a previous Google search soup
#if there was no fun fact found, then we need to scrape for additional websites that could list fun facts
#search for only websites which have fun fact as lists; if there are complete lists of facts, then parse and return the associated fun fact(s)
def scrapeForFunFacts(soup, searchTerm):
    websiteInfo = soup.find_all("div", attrs={"class":"g"})
    websiteLinks = []

    #get all websites from google search first page
    for details in websiteInfo:
        link = details.find_all("h3")
        for mdetails in link:
            links = mdetails.find_all("a")
            lmk = ""
            for lnk in links:
                lmk = lnk.get("href")[7:].split("&")
                sublist = []
                sublist.append(lmk[0])
            websiteLinks.append(sublist)

        #iterate through websites until we get fun facts

    for websiteLink in websiteLinks:
        response = requests.get(websiteLink[0])
        currentWebsiteSoup = BeautifulSoup(response.text, 'html.parser')
        #look for an unordered list of fun facts
        for line in currentWebsiteSoup.find_all('ul'):
            # print(line)
            result = []
            for descendant in line.li.descendants:
                if isinstance(descendant, NavigableString):
                    result.append((descendant).strip())

            currentFunFact = ' '.join(result)
            #check if it's actually a fun fact with the search subject and return if it is
            if currentFunFact != '' and (searchTerm.lower() in currentFunFact.lower()):
                # print(currentFunFact.strip())
                return currentFunFact.strip()

    return ''

# getFunFacts('tiger')
