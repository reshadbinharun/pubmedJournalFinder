from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#TO DO:
'''
1. catch exception on list comprehension
2. export file as csv
'''

def searchEach(results):
	links = []
	for link in results:
		links.append(link.get_attribute('href'))
	return links

def printEachLink(results):
	for link in results:
		print(link.get_attribute('href'))
	return

def getEachUrl(results):
	urls = []
	for link in results:
		driver.execute_script("window.open('" + link.get_attribute('href') +"');") #opens new window with script
	return urls

def parseAbstract(driver):
	#abstract = driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div[5]/div/div[5]/div[2]/p") #xpath does not always give abstract location
	abstract = driver.find_elements_by_tag_name("p")
	abstractText = []
	#cannot get text from abstract
	#add all text from abstract text
	print(len(abstract))
	for i in range(0, len(abstract) - 1):
		if (len(abstract[i].text) > 0):
			abstractText.append(abstract[i].text)
			#print("Printing obj {} {}".format(i, abstract[i].text))
	return abstractText

# def getAbstracts(links, driver):
def getAbstracts(links, driver, writer):

	print("There are {} links being passed in".format(len(links)))
	#for link in links:
	allAbstracts = []
	for url in links:	
		#opening new tab
		#driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
		#url = link.get_attribute('href')
		print(url)
		driver.get(url)
		allAbstracts.append(parseAbstract(driver))

		#writing to csv file:
		writer.writerow([url, parseAbstract(driver)])	

		driver.implicitly_wait(5)
		#driver.back()
		#get abstract
	return allAbstracts

def getResultsOnPage(driver):
	allSearch = driver.find_element_by_xpath("//*[@id=\"maincontent\"]/div/div[5]")
	links = allSearch.find_elements_by_css_selector("a")
	link_urls = [link.get_attribute('href') for link in links if len(link.get_attribute('href')) < 50] #list comprehension to only include the smaller url
	#link_urls = link_urls[0::2]
	print(link_urls)
	return link_urls
	#return links


def navigatePages(driver, pageLim, writer):
	pageSelect = driver.find_element_by_xpath("//*[@id=\"pageno\"]")
	res_page = driver.current_url
	currPage = int(pageSelect.get_attribute("value"))
	totalPages = int(pageSelect.get_attribute("last"))
	pages2Nav = min(pageLim, totalPages)
	print("The current page is {}".format(currPage))
	print("There are a total of {} pages".format(totalPages))

	#call all results
	#back at end of result
	#for i in range(1, pages2Nav-1):
	all_abstracts = []
	for i in range(1, pages2Nav):
		# #click next
		# page = driver.find_element_by_xpath("//*[@id=\"EntrezSystem2.PEntrez.PubMed.Pubmed_ResultsPanel.Pubmed_Pager.Page\"]").click()
		#update page num and hit enter:
		page = driver.find_element_by_xpath("//*[@id=\"pageno\"]")
		page.clear()
		page.send_keys(i)
		page.send_keys(Keys.RETURN)
		#call function to parse results on page
		print("current on page# {}".format(i))
		links = getResultsOnPage(driver)
		#printEachLink(links)
		#all_abstracts.append(getAbstracts(links, driver))
		all_abstracts.append(getAbstracts(links, driver, writer))
		driver.implicitly_wait(5)
		driver.get(res_page)
		#now click on results

	# return all_abstracts
	return
###
#END OF HELPER FUNCTIONS

#USER INPUTS
search_term = input("Enter search term: ")
pageLim = int(input("Enter page limit: "))
#
#USER INPUTS

driver = webdriver.Firefox()
driver.get("https://www.ncbi.nlm.nih.gov/pubmed/")
assert "PubMed" in driver.title

#setting wait time before throwing an exception:
driver.implicitly_wait(5)

#Searching on PubMed Home
driver.find_element_by_xpath("//*[@id=\"term\"]").send_keys(search_term)
driver.find_element_by_xpath("//*[@id=\"search\"]").click()

#RESULTS LOADED

#setting up csv export
import csv
csvfile = './allAbstracts.csv'
with open(csvfile, "w") as output:
	writer = csv.writer(output, lineterminator = '\n')
	#abstract_array = navigatePages(driver, pageLim)
	navigatePages(driver, pageLim, writer)



#to navigate pages: https://stackoverflow.com/questions/24166689/selenium-python-access-next-pages-of-search-results
#to navigate groups of elements: https://stackoverflow.com/questions/27006698/selenium-iterating-through-groups-of-elements
#https://stackoverflow.com/questions/41329211/use-python-to-go-through-google-search-results-for-given-search-phrase-and-url