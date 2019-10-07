from selenium import webdriver
from bs4 import BeautifulSoup
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def extract_symptoms(disease):
	driver = webdriver.Chrome(executable_path='./chromedriver')  
	driver.get('https://www.wikidoc.org/index.php/Main_Page') 
	driver.implicitly_wait(10)

	try:
		input_element = driver.find_element_by_name('search')
		input_element.send_keys(disease)
		search_element = driver.find_element_by_name('fulltext')
		search_element.click()
	except Exception as e:
		print('fail to open the searching page')
		return -1

	try:
		result = driver.find_elements_by_xpath('//div[@class="gsc-results gsc-webResult"]//div[@class="gsc-webResult gsc-result"][1]//div[@class="gs-title"]/a[@class="gs-title"]')[0]
		box = driver.find_elements_by_xpath('//div[@class="gsc-results-wrapper-overlay gsc-results-wrapper-visible"]')[0]
		driver.execute_script("arguments[0].scrollIntoView(true);", result)
		driver.execute_script("arguments[0].scrollBy(0,-100)",box) 
		WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//div[@class="gsc-results gsc-webResult"]//div[@class="gsc-webResult gsc-result"][1]//div[@class="gs-title"]/a[@class="gs-title"]'))).click()
	except Exception as e:
		print('fail to find the result webpage')
		return -1

	try:
		result = driver.find_elements_by_xpath('//tr[@bgcolor="Pink"]//a[text()="Patient Information"]')
		result[0].click()
	except Exception as e:
		print('fail to find Patient Information')
		return -1

	soup = BeautifulSoup(driver.page_source, 'html.parser')
	element = soup.find('span', {'id': 'What_are_the_symptoms_of_Asthma?'}).parent
	ending_point = soup.find('span', {'id': 'What_causes_Asthma?'}).parent

	symptoms_list = [] 

	while element is not ending_point:
		if element is None:
			break
		if element.name == 'ul':
			symptoms_list.append(element.get_text())
		element = element.find_next_sibling()

	file = open('symptom.txt', 'w')
	for symtom in symptoms_list: 
		file.write(symtom + '\n')
	file.close()

	driver.close()

	return 1

if __name__ == '__main__':
	argvs = sys.argv
	if len(argvs) <= 1:
		print('Type disease')
	else:
		extract_symptoms(argvs[-1])
