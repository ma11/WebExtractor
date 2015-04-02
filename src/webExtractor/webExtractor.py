# -*- coding: UTF-8 -*-

## @package webExtractor
#  @file webExtractor.py
#  @brief This module presents classes and methods for downloading and print on terminal some items extracted from blog-like websites.
#  @details The webExtractor module gives several classes and methods for downloading and extracting informations on blog-like webpage.
#           The basic tools are a base HTML parser class myParser, several website consistant parsers, and a core class WebExtractor
#           for extracting and displaying website informations.
#  @author ma11
#  @version 0.1
#  @date Tue Dec 24 14:51:13 2013
#  @bug Random on dtc is not that random (maybe due to website...)

from optparse import OptionParser
from optparse import OptionGroup
from HTMLParser import HTMLParser
import urllib2

## @class myParser
# @brief Base class for this module HTML parsers
# @details This base class intialize HTMLParser class (standard python library) and give a getItems() method.
#          Every HTML parsers within this module must have getItems() method.
# @author ma11
class myParser(HTMLParser):
    ## @brief Dictionnary containing all items data linked with items number.
    #  @details Items number are website dependant (define by website) and item data are the data of interest (string only)
    items={}
    ## @brief Store current item number
    # @details The itemNumber is used to save current item identifient (website dependant) and is used in items as keys for items dictionnary
    itemNumber=int()
    ## @brief Flag to know if an item has been found
    #  @details Technically, this flag is raised to True if a specific tag is detected in webpage code. Then, it is used by handle_data() to know
    #           if data read is an item. Then it is put to False by detection of specific tag (usually a end_tag)
    itemFound=False

    ## @brief Class constructor
    # @details Call for inheritance constructor and set required attributes for HTML parsers: items, itemNumber and itemFound
    # @param[in] self The object pointer
    def __init__(self):
        HTMLParser.__init__(self)

    ## @brief Method called to handle arbitrary data
    # @details This method is inherited from HTMLParser class and implement the process of arbitrary data parsed in web page code. In this module case, data is lstrip()ed
    #          and rstrip()ed
    # @param[in]  self The object pointer
    # @param[out] data The string representation of data found
    def handle_data(self,data):
        if self.itemFound:
            self.items[self.itemNumber]+=data.lstrip().rstrip()

    ## @brief Return items found after parsing webpage code
    # @details During webpage code parsing, items discovered are stored in self.items dictionnary. This dictionnary linked itemNumber with items string.
    #           The itemNumber is a number representing the item on the website (usually the ID of a blog entry) and the item string is the string representation
    #           of the item content.
    # @param[in]  self The object pointer
    # @param[out] items A dictionnary of (itemValue,item string) discovered while parsing webpage
    def getItems(self):
        return self.items

## @class htmlParserSjn
# @brief Class for http://www.suisjenormal.fr/ parsing
# @details This class describe a parser for http://www.suisjenormal.fr/ website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserSjn(myParser):
    ## @brief Class constructor
    # @details Call only for inheritance constructor.
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)

    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<div class=post article ...\> and items data are located within the same tag
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag=='div' and attrs.__len__()>2:
            if attrs[0][0]=='class' and attrs[0][1]=='summary':
                self.itemNumber=int(attrs[1][1].split('_')[1])
                self.items[self.itemNumber]=''
            if attrs[1][0]=='class' and attrs[1][1] == 'story':
                self.itemFound=True
        if tag=='p' and attrs:
             if attrs[0][0]=='class' and attrs[0][1]=='thestory':
                self.itemFound=True

    ## @brief Method to handle ending tags
    #  @details This method is inherited from HTMLParser class and implement the process for every ending tag discovered while parsing webpage.
    #           For this website, end of item data is found when a \</p\> tag is parsed.
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'p')
    def handle_endtag(self,tag):
        if self.itemFound and tag=='p':
            self.itemFound=False

## @class htmlParserVdm
# @brief Class for http://www.viedemerde.fr parsing
# @details This class describe a parser for www.viedemerde.fr website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserVdm(myParser):
    ## @brief Class constructor
    # @details Call only for inheritance constructor.
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)

    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<div class=post article ...\> and items data are located within the same tag
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag=='div' and attrs:
            if attrs[0][0]=='class' and attrs[0][1] == 'post article':
                self.itemNumber = int(attrs[1][1])
                self.items[self.itemNumber]=''
                self.itemFound=True

    ## @brief Method to handle ending tags
    #  @details This method is inherited from HTMLParser class and implement the process for every ending tag discovered while parsing webpage.
    #           For this website, end of item data is found when a \</p\> tag is parsed.
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'p')
    def handle_endtag(self,tag):
        if self.itemFound and tag=='p':
            self.itemFound=False

## @class htmlParserBashOrg
# @brief Class for http://bash.org/ parsing
# @details This class describe a parser for http://bash.org/ website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserBashOrg(myParser):
    ## @brief Class constructor
    # @details Call for inheritance constructor and define a boolean variable to know if the parser is inside a \<span\>\</span\>.
    #          In this specific website, a \<span\> occure while reading data inside an item.
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)

    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<a href="..."\> and items data are located in \<p class="qa"\>
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag == 'a' and len(attrs)>1:
            if attrs[1][0]=='title' and attrs[1][1]=="Permanent link to this quote.":
		self.itemNumber = int(attrs[0][1][1:])
                self.items[self.itemNumber]=''
        if tag=='p' and attrs:
            if attrs[0][1]=='qt':
                self.itemFound=True

## @class htmlParserDtc
# @brief Class for http://danstonchat.com/ parsing
# @details This class describe a parser for http://danstonchat.com/ website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserDtc(myParser):
    ## @brief Class constructor
    # @details Call for inheritance constructor and define a boolean variable to know if the parser is inside a \<span\>\</span\>.
    #          In this specific website, a \<span\> occure while reading data inside an item.
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)
        ## @brief Boolean variable to detect a span tag into data item
        #  @details These variable is used for removing possible ':' that appear inside span tag. Specific to this website
        self.inSpan=False

    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<div class="item ..."\> and items data are located in \<p class="item content"\>
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag == 'div' and attrs:
            if attrs[0][0]=='class' and attrs[0][1].startswith('item '):
                self.itemNumber = int(attrs[0][1].split(' ')[1][4:])
                self.items[self.itemNumber]=''
        if tag=='p' and attrs:
            if attrs[0][1]=='item-content':
                self.itemFound=True
        if tag=='span' and attrs:
            if attrs[0][0]=='class' and attrs[0][1]=='decoration':
                self.items[self.itemNumber]+='\n'
                self.inSpan = True

    ## @brief Method called to handle arbitrary data
    # @details This method is inherited from myParser class and therefore by HTMLParser class and implement the process of arbitrary data parsed in web
    #          page code. A specific treatment appears for this website, because of the presence of \<span\> tag within data items
    # @param[in]  self The object pointer
    # @param[out] data The string representation of data found
    def handle_data(self,data):
        if self.itemFound:
            if self.inSpan:
                data=data.replace(':','')
            self.items[self.itemNumber]+=data.lstrip().rstrip()

    ## @brief Method to handle ending tags
    #  @details This method is inherited from HTMLParser class and implement the process for every ending tag discovered while parsing webpage.
    #           For this website, end of item data is found when a \</p\> tag is parsed.
    #           Moreover, a \</span\> ending tag is used while parsing data items.
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'p')
    def handle_endtag(self,tag):
        if tag=='p' and self.itemFound:
            self.itemFound=False
        if tag=='span' and self.inSpan:
            self.items[self.itemNumber]+=': '
            self.inSpan=False

## @class htmlParserCnf
# @brief Class for http://chucknorrisfacts.fr/ parsing
# @details This class describe a parser for http://chucknorrisfacts.fr/ website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserCnf(myParser):
    ## @brief Class constructor
    # @details Call only for inheritance constructor.
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)

    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<div class="item ..."\> and items data are located in \<p class="item content"\>
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag=='div' and attrs:
            if attrs[0][0]=='class' and attrs[0][1]=='factbody':
                self.itemFound=True
            if attrs[0][0]=='class' and attrs[0][1]=='fact' and attrs[1][0]=='fact_id':
                self.itemNumber=int(attrs[1][1])
                self.items[self.itemNumber]=''
            if attrs[0][0]=='class' and attrs[0][1]=='vote':
                self.itemFound=False

## @class htmlParserPbk
# @brief Class for http://pebkac.fr/ parsing
# @details This class describe a parser for http://pebkac.fr/ website. It extends methods from myParser class and therefore from HTMLParser class
# @author ma11
class htmlParserPbk(myParser):
    ## @brief Class constructor
    # @details Call for inheritance constructor and define a boolean variable to know if the itemNumber has been found. It is necessary because of webcoding
    #          style of this website
    # @param[in] self The object pointer
    def __init__(self):
        myParser.__init__(self)
        ## @brief Flag to know when a item number will follow
        #  @details This flag is required because of the website coding-style. It is raised when a specific flag is parsed, and it drop down when another flag is parsed.
        self.itemNumberFound=False
    ## @brief Method to handle starting tags
    #  @details This method is inherited from HTMLParser class and implement the process for every starting tag discovered while parsing webpage.
    #           For this website, itemNumber are discovered within \<a class="permalink"\> and items data are located in \<p class="content"\>
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'div')
    #  @param[in] attrs The 2-tuple list representation of tag attributes (ie. [('class','post article'),...])
    def handle_starttag(self,tag,attrs):
        if tag=='p' and attrs:
            if attrs[0][0]=='class' and attrs[0][1]=='content':
                self.itemFound = True
        if tag=='a' and attrs:
            if attrs[0]==('class','permalink'):
                self.itemNumber=int(attrs[3][1].split(' ')[1][1:])
                self.items[self.itemNumber]=''
        if tag=='span' and attrs:
            if attrs[0][0]=='class' and attrs[0][1]=='pid':
                self.itemNumberFound=True

    ## @brief Method to handle ending tags
    #  @details This method is inherited from HTMLParser class and implement the process for every ending tag discovered while parsing webpage.
    #           For this website, end of item data is found when a \</p\> tag is parsed.
    #  @param[in]  self The object pointer
    #  @param[in] tag The string representation for tag (ie. 'p')
    def handle_endtag(self,tag):
        if tag=='p' and self.itemFound:
            self.itemFound = False

    ## @brief Method called to handle arbitrary data
    # @details This method is inherited from myParser class and therefore by HTMLParser class and implement the process of arbitrary data parsed in web
    #          page code. A specific treatment appears for this website, because of the way itemNumber are defined by webcode
    # @param[in]  self The object pointer
    # @param[out] data The string representation of data found
    def handle_data(self,data):
        if self.itemFound:
            self.items[self.itemNumber]+=data.lstrip().rstrip()
        if self.itemNumberFound:
            self.itemNumber=int(data[1:])
            self.items[self.itemNumber]=''
            self.itemNumberFound=False

## @class WebExtractor
# @brief Core class for webExrtactor module
# @details This class implements methods for processing data from blog-like websites. It gives several features (ie. extract random items,
#          extract a specific item, extract last items,...) and print required information on terminal.
# @author ma11
class WebExtractor:
    ## @brief Class constructor
    # @details Set NUMITEMS and LINELENGTH attributes
    # @param[in] self The object pointer
    def __init__(self):
        ## @brief The number of items to print
        #  @details This attribute is used to define the number of items to keep for printing
        self.NUMITEMS = 10
        ## @brief Terminal line length
        #  @details This attribute is used for defining the number of '-' taht are printed to separate items while printing
        #  @todo Get an automatic method for obtaining terminal line length
        self.LINELENGTH = 80

    ## @brief Set LINELENGTH value
    def setLineLength(self,length):
        self.LINELENGTH=length

    ## @brief Set WEBSITE value
    def setWebsite(self,website):
        ## @brief Store the short value of website
        #  @details The short value of website is:
        #           - dtc for http://danstonchat.com
        #           - vdm for http://viedemerde.fr
        #           - cnf for http://www.chucknorrisfacts.fr
        #           - pbk for http://www.pebkac.fr
        self.WEBSITE = website

    ## @brief Set NUMITEMS value
    def setNumItems(self,numitems):
        self.NUMITEMS = numitems

    ## @brief Compute value of several variables according to choosen website
    #  @details This methods tune the program according to the selected website. It set up different URLs and counter in order to find the 'latest page',
    #           the 'item pages' and, above all, it define the parser class to use for the specific website.
    #  @param[in]  self The object pointer
    #  @param[in]  website The website to use for setting up. Here, one use short name website (ie. 'dtc' for http://danstonchat.com,...)
    def tune(self,website):
        self.WEBSITE=website
        urls={'dtc': 'http://danstonchat.com',
	          'vdm': 'http://viedemerde.fr',
              'cnf': 'http://http://www.chucknorrisfacts.fr',
              'pbk': 'http://www.pebkac.fr/',
              'sjn': 'http://www.suisjenormal.fr/',
	      'brg': 'http://bash.org/'
	          }
        latestIterPages={'dtc': 'http://danstonchat.com/latest/@@COUNT@@.html',
                         'vdm': 'http://www.viedemerde.fr/?page=@@COUNT@@',
                         'cnf': 'http://www.chucknorrisfacts.fr/facts/?p=@@COUNT@@',
                         'pbk': 'http://www.pebkac.fr/@@COUNT@@/',
                         'sjn': 'http://www.suisjenormal.fr/@@COUNT@@',
			 'brg': 'http://bash.org/?latest&@@COUNT@@'
                        }
        searchItemsPages={'dtc': 'http://danstonchat.com/@@ID@@.html',
                         'vdm': 'http://www.viedemerde.fr/@@ID@@',
                         'cnf': '',
                         'pbk': 'http://www.pebkac.fr/pebkac/@@ID@@/',
                         'sjn': 'http://www.suisjenormal.fr/discussion/@@ID@@',
			 'brg': 'http://bash.org/?quote=@@ID@@'
                         }

        latestPages={'dtc': 1,
	                 'vdm': 0,
                     'cnf': 1,
                     'pbk': 1,
                     'sjn': 1,
		     'brg': 0
	                 }
        randPages={'dtc': 'http://danstonchat.com/random.html',
                   'vdm': 'http://www.viedemerde.fr/aleatoire',
                   'cnf': 'http://www.chucknorrisfacts.fr/facts/alea',
                   'pbk': 'http://www.pebkac.fr/random/',
                   'sjn': 'http://www.suisjenormal.fr/hasard',
		   'brg': 'http://bash.org/?random1'
                   }
        htmlParsers={'dtc': htmlParserDtc,
                     'vdm': htmlParserVdm,
                     'cnf': htmlParserCnf,
                     'pbk': htmlParserPbk,
                     'sjn': htmlParserSjn,
		     'brg': htmlParserBashOrg
                     }
        ## @brief Store the URL of selected website main page (unused for the moment)
        self.URL=urls[website]
        ## @brief Store the init point of the counter for latest pages
        self.LATESTPAGE=latestPages[website]
        ## @brief Store the counter to keep in memory the actual last page counter
        #  @details This counter is incremented when more items are required than the items available on a single page
        self.COUNTPAGE=self.LATESTPAGE
        ## @brief Store the pattern of latest pages URL (with @@COUNT@@ tokens)
        self.LATESTITERPAGE=latestIterPages[website]
        ## @brief Store the name of parser class to use for the selected website
        self.HTMLPARSER=htmlParsers[website]
        ## @brief Store the random page of the selected website.
        self.RANDPAGE=randPages[website]
        ## @brief Store the pattern for URL search item for the selected website.
        #  @details Usually, for a blog-like website, it is possible to reach a specific item by using it ID and requiring a URL like:
        #           www.example.com/ID
        self.SEARCHPAGE=searchItemsPages[website]

    ## @brief Extract last ID
    #  @details This method only extract last item ID. It basically download and parse the latest page to extract items, and return last item ID
    #  @param[in] self The object pointer
    #  @param[out] ID The highest ID value parsed from latest page
    def extractLastId(self):
        website=self.WEBSITE
        url=self.URL
        latestPage=self.buildPage(self.LATESTPAGE,self.LATESTITERPAGE)
        items = self.parsePage(latestPage)
        return max(items.keys())

    ## @brief Parse a page
    #  @details This method parse the given URL using the right parser class and return a dictionnary of found items
    #  @param[in] self The object pointer
    #  @param[in] page The URL of webpage to parse
    #  @param[out] items The dictionnary of items found on input page
    def parsePage(self,page):
        try:
            webcode = urllib2.urlopen(page).read().decode("UTF-8").replace('\r','')
        except urllib2.HTTPError:
            print '[PARSEPAGE] ERROR: could not download webcode'
            return []
        except UnicodeDecodeError:
            webcode = urllib2.urlopen(page).read()
        htmlparser=self.HTMLPARSER()
        htmlparser.feed(webcode)
        htmlparser.close()
        return htmlparser.getItems()

    ## @brief Build a page according to URL pattern and a counter
    #  @details This method is simply a regexp interpretor and replace a counter value into a URL page pattern.
    #           A URL pattern contains tags like '@@COUNT@@ or @@ID@@ that are to be replaced. It is usefull to build URLs for latest 2nd page,
    #           latest 3rd page,...
    #  @param[in] self The object pointer
    #  @param[in] count A count like integer
    #  @param[in] page A URL containing pattern to replace by count
    #  @param[out] url The URL build from count and page URL pattern
    def buildPage(self,count,page):
        if not page:
            raise ValueError('[BUILDPAGE] Empty page')
        if page.__contains__('@@COUNT@@'):
            return page.replace('@@COUNT@@',str(count))
        if page.__contains__('@@ID@@'):
            return page.replace('@@ID@@',str(count))
        raise NotImplementedError('[BUILDPAGE] Can not build from page: '+page+' and count: '+count)

    ## @brief Compute the next page to be parsed
    #  @details This method just increment a counter to build next page URL while seeking for next latest page for example.
    #  @param[in] self The object pointer
    #  @param[out] url The next page URL
    def iterPage(self):
        if self.LATESTITERPAGE.__contains__('@@COUNT@@'):
            self.COUNTPAGE+=1
            return self.buildPage(self.COUNTPAGE,self.LATESTITERPAGE)

    ## @brief Extract last items upload on website
    #  @details This methods extract NUMITEMS last items on given website by parsing lastest pages. It returns a list of lasts items, ranked by item IDs.
    #  @param[in] self The object pointer
    #  @param[out] toOut A list of 2-tuples corresponding to the last NUMITEMS on website
    def extractLastItems(self):
        numitems=self.NUMITEMS
        currentItems=0
        currentPage=self.buildPage(self.LATESTPAGE,self.LATESTITERPAGE)
        #print "[EXTRACTLASTITEMS] Current page: ",currentPage
        toPrint={}
        toOut=list()
        while currentItems<numitems:
            items=self.parsePage(currentPage)
            toPrint.update(items)
            currentItems=toPrint.__len__()
            currentPage=self.iterPage()
            #print "[EXTRACTLASTITEMS] Current item: ",currentItems
        for k in sorted(toPrint.keys())[-numitems:]:
            toOut.append(tuple([k,toPrint[k]]))
        return toOut

    ## @brief Extract randomly items from website
    #  @details This methods extract NUMITEMS random items on given website by parsing random pages. The website has to define a random page on which
    #           every reload extract randomly new items. It returns a list of NUMITEMS random items, ranked by item IDs.
    #  @param[in] self The object pointer
    #  @param[out] toOut A list of 2-tuples corresponding to NUMITEMS random items on website
    def extractRandItems(self):
        numitems=self.NUMITEMS
        currentItems=0
        currentPage=self.RANDPAGE
        toPrint={}
        toOut=list()
        while currentItems<numitems:
            items=self.parsePage(currentPage)
            toPrint.update(items)
            currentItems=toPrint.__len__()
        for k in sorted(toPrint.keys())[-numitems:]:
            toOut.append(tuple([k,toPrint[k]]))
        return toOut

    ## @brief Extract one specific item from website
    #  @details This methods extract one item specified by it ID. The ID is website dependants.
    #  @param[in] self The object pointer
    #  @param[in] ID The ID of the item to extract. ID is website dependant
    #  @param[out] toOut A list of 2-tuples corresponding to NUMITEMS random items on website
    def extractItem(self,ID):
        #print "[EXTRACTITEM] id: ",ID
        #print "[EXTRACTITEM] searchPage: ",self.SEARCHPAGE
        itemPage=self.buildPage(ID,self.SEARCHPAGE)
        #print "[EXTRACTITEM] itemPage: ",itemPage
        #if not itemPage or itemPage.__len__()>1:
        item=self.parsePage(itemPage)
        if not item or item.__len__()>1:
            raise NotImplementedError('[EXTRACTITEM] Item not found')
        return item.items()

    ## @brief Print items list on screen
    #  @details This method print a list of 2-tuples on the form [(ID,item string)] on screen with a nice item separation
    #  @param[in] self The object pointer
    #  @param[in] items The list of 2-tuples [(ID,items)]
    def printItems(self,items):
        if items.__len__() > 1:
	        for i,it in reversed(items):
	            print "ID: ",i
                #print it.encode('UTF-8')
	            print it
	            print '-'*self.LINELENGTH
        elif items.__len__() == 1:
            print "ID ",items[0][0]
            #print items[0][1].encode('UTF-8')
            print items[0][1]
        elif items.__len__()==0:
            print "None"

class App():
    def __init__(self,*args,**kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])

	## @brief Main call for the module
	#  @details This main method set up an option parser for command-line call and call for the right method depending on the user choice.
    def main(self):
	    optWebArg=["dtc","vdm","cnf","pbk","sjn","brg"]
	    optparser = OptionParser(version='%prog '+str(self.version))
	    opt_output=OptionGroup(optparser,'Output Options',"Options for setting output behavior of the program")
	    opt_action=OptionGroup(optparser,'Action Options',"Option for setting the behavior of the program")

	    opt_action.add_option("-w","--website",dest="WEBSITE",type="choice",help="Website to use (from "+str(optWebArg)+")",default="dtc",choices=optWebArg)
	    opt_action.add_option("-i","--lastid",help="Extract only last id of items",action="store_true",dest="extractLastId",default=False)
	    opt_action.add_option("-I","--id",help="Extract only the ID item specified",dest="idToExtract",default='')
	    optparser.add_option("-r","--rand",help="Extract random items",action="store_true",dest="extractRand",default=False)
	    opt_action.add_option("-n","--items",help="The number of items to print (default: %default)",dest="NUMITEMS",default=2,type='int')
	    opt_output.add_option("-l","--columns",help="Set the line length (use to print -- between items) (default: %default)",dest="lineLength",default=80,type='int')

	    optparser.add_option_group(opt_action)
	    optparser.add_option_group(opt_output)
	    (options, args) = optparser.parse_args()

	    WEBSITE=options.WEBSITE
	    EXTRACTLASTID=options.extractLastId
	    NUMITEMS=options.NUMITEMS
	    EXTRACTRAND=options.extractRand
	    LINELENGTH=options.lineLength
	    IDTOEXTRACT=options.idToExtract

	    webExtract=WebExtractor()
	    webExtract.setWebsite(WEBSITE)
	    webExtract.setNumItems(NUMITEMS)
	    webExtract.setLineLength(LINELENGTH)

        # Throw error 'cause sjn not implemented yet
        #if WEBSITE == 'sjn':
        #    raise NotImplementedError('sjn not yet implemented')

        # Tune several variables according to choosen website
	    try:
	        webExtract.tune(WEBSITE)
	    except KeyError:
	        print '[TUNE]: Error: Can not correctly tune webExtractor'
	        return 1

	    if EXTRACTLASTID:
	        LASTID = webExtract.extractLastId()
	        print '[MAIN] lastId: ',LASTID
	        return
	    if IDTOEXTRACT:
	        item=webExtract.extractItem(IDTOEXTRACT)
	        webExtract.printItems(item)
	        return
	    if EXTRACTRAND:
	        randItems=webExtract.extractRandItems()
	        webExtract.printItems(randItems)
	        return

	    lastItems = webExtract.extractLastItems()
	    webExtract.printItems(lastItems)


if __name__ == "__main__":
    app = App(version='alpha')
    app.main()
