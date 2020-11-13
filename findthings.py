import os
#set current working directory to file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)
from bs4 import BeautifulSoup
import requests
import webbrowser
import time
import urllib.request
from tika import parser
import re


def find_doi(thing,number):
    """
    Thing you want to look for 

    Parameters
    ----------
    thing : String
        The very thing you are looking for.
    number : int
        number of articels which should be checkt.

    Returns
    -------
    dois = list of urls
        see above.

    """
    urls = []
    dois = []
    l = list(range(0,number+10,10))
    for elements in l:
        #soupmixture
        url1 = 'https://scholar.google.com/scholar?start='+str(elements)+'&q='
        url2 = '&hl=en&as_sdt=0,5'
        urltoopen = url1+thing+url2
        results = requests.get(urltoopen)
        src = results.content
        soup = BeautifulSoup(src, 'lxml')
        
        #find links:
        for a_tag in soup.find_all('a'):
            urls.append(a_tag.get('href'))
            
        #sleep for googles peace :-S    
        time.sleep(1) #just to please google might be set lower
     
    #Save DOIs in Textfile    
    file = open('DOIs.txt','+w')
    for url in urls:
        if 'doi' in url:
            print(url)
            dois.append(url)
            file.write(url+'\n')
    return dois

def get_paper(doi):
    """

    Parameters
    ----------
    doi : URL to accual PDF
        Downloads Paper to read.

    Returns
    -------
    None.

    """
    try:
        result = requests.get(doi)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        print(soup.find('iframe').attrs['src'])
        url = soup.find('iframe').attrs['src']
        print('Beginning file download with urllib2...')
        urllib.request.urlretrieve(url, 'PaperToScore.pdf' )
        print('Download Completed')
        return
    except:
        return 
    
def score_paper(keyargs):
    
    returnlist = []
    paper = parser.from_file('PaperToScore.pdf')
    PaperToScore = paper['content']
    print(paper['metadata']['title']) 
    title = paper['metadata']['title']
    words = re.sub("[^\w]", " ",  PaperToScore).split()
    lenText = len(words)
    # returnlist.append(title)
    
    for key in keyargs:
        value = 0
        for word in words:
            if key.lower() == word.lower():
                value += 1
                
        returnlist.append(key,value/lenText)
    return returnlist

#------------------------------------#
#         Awesome Test Area          #
#------------------------------------#

Score_List = []
# dois = find_doi('cfd+kinetics+stem+cells',10)
file = open('DOIs.txt','r')
for doi in file:
    print(doi)
    get_paper('https://sci-hub.do/'+doi.strip('\n'))
    scores = score_paper(('CFD','kinetic','cells'))
    Score_List.append((scores, doi.strip('\n')))
    
print(Score_List)


