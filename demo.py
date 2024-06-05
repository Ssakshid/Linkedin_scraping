from urllib import request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
PATH=r"C:\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')






# linkedin login
service = webdriver.ChromeService(executable_patH = PATH)
driver = webdriver.Chrome(service=service)
driver.get("https://www.linkedin.com/login")
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("dubeyavaykumar@gmail.com")
password_field = driver.find_element(By.ID, "password")
password_field.send_keys("dubeytora123")
sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
sign_in_btn.click()

# scraping data from users profile
profile_url="https://www.linkedin.com/in/anamika-mishra-700a6b311/"
def scrape_profile(driver, profile_url):
    """Scrape required fields from Linkedin URl"""
    driver.get(profile_url)

    profile_name=driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").get_attribute("innerText")
    profile_title=driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").get_attribute("innerText")
    profile_location=driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").get_attribute("innerText")

    driver.find_element(By.ID, "top-card-text-details-contact-info").click()
    time.sleep(1)
    profile_email = driver.find_element(By.CSS_SELECTOR, "a.pv-contact-info__contact-link[href^='mailto:']").get_attribute("innerText")

    print("Profile Name: {}".format(profile_name))
    print("Title: {}".format(profile_title))
    print("Location: {}".format(profile_location))
    print("Email: {}".format(profile_email))

scrape_profile(driver, profile_url)


#scrape data from job posting page
# def scrape_jobs(driver, jobs_url):
#     """Scrape required fields from LinkedIn job page"""
#     driver.get(jobs_url)
#     for job in driver.find_elements(By.CSS_SELECTOR, "ul#jobs-home-vertical-list__entity-list li"):
#         try:
#             job_title = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute("innerText")
#             company_name = job.find_element(By.CSS_SELECTOR, "span.job-card-container__primary-description").get_attribute("innerText")
#             company_location = job.find_element(By.CSS_SELECTOR, "li.job-card-container__metadata-item").get_attribute("innerText")
#         except:
#             continue
        
#         print("Job title: {}".format(job_title))
#         print("Company name: {}".format(company_name))
#         print("Company location: {}".format(company_location))


# n=driver.find_element(By.CLASS_NAME, 'results-context-header__job-count')[0].text
# n
# '211'

# y=pd.to_numeric(n)
# y
# 211

# i=2
# while(i<=16):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     i=i+1

#     try:
#         x=driver.find_elements(By.XPATH, "//button[aria-label='Load more results']")
#         driver.execute_script("arguments[0].click();")
#         time.sleep(3)
#     except:
#         pass
#     time.sleep(4)

# companyname = []

# for j in range(y):
#     try:
#         company=driver.find_elements_by_class_name('base-search-card__subtitle')[j].text
#         companyname.append(company)

#     except IndexError:
#         print("done")

# titlename = []
# for j in range(y):
#     try:
#         title=driver.find_elements_by_class_name('base-search-card__subtitle')[j].text
#         titlename.append(title)

#     except IndexError:
#         print("done")


# companyfinal=pd.DataFrame(companyname, columns=["company"])
# titlefinal=pd.DataFrame(titlename, columns=["title"])
# final=companyfinal.join(titlefinal)



# print(driver.title)

url = "https://www.linkedin.com/login"
response = request.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
     

data = {
    "name":[],
    "date":[],
    "post":[],
    "likes":[],
    "count_posts":[]
}

for i in range(max(0,40)):
    driver.execute_script('window.scrollBy(0,500)')
    time.sleep(1)

posts = soup.find_all('div',{'class':"occlude-update ember-view"})
post = posts[2].find('div',{'class':"feed-shared-update-v2__description-wrapper ember-view"}).span.get_text()
if post:
    print(post)


start = time.time()


initialScroll = 0
finalScroll = 1000

while True:
	driver.execute_script(f'''window.scrollTo({initialScroll},
											{finalScroll})
						''')
	
	initialScroll = finalScroll
	finalScroll += 1000

	
	time.sleep(3)
	

	end = time.time()

	if round(end - start) > 20:
		break
     
src = driver.page_source

soup = BeautifulSoup(src, 'lxml')

intro = soup.find('div', {'class': 'pv-text-details__left-panel'})
 
print(intro)


name_loc = intro.find("h1")


name = name_loc.get_text().strip()

works_at_loc = intro.find("div", {'class': 'text-body-medium'})


works_at = works_at_loc.get_text().strip()


location_loc = intro.find_all("span", {'class': 'text-body-small'})

location = location_loc[0].get_text().strip()

print("Name -->", name,
	"\nWorks At -->", works_at,
	"\nLocation -->", location)

experience = soup.find("section", {"id": "experience-section"}).find('ul')
 
print(experience)

# In case of an error, try changing the tags used here.

li_tags = experience.find('div')
a_tags = li_tags.find("a")
job_title = a_tags.find("h3").get_text().strip()

print(job_title)

company_name = a_tags.find_all("p")[1].get_text().strip()
print(company_name)

joining_date = a_tags.find_all("h4")[0].find_all("span")[1].get_text().strip()

employment_duration = a_tags.find_all("h4")[1].find_all(
	"span")[1].get_text().strip()

print(joining_date + ", " + employment_duration)

jobs = driver.find_element(By.XPATH, "//a[@data-link-to='jobs']/span")

jobs.click()

job_src = driver.page_source

soup = BeautifulSoup(job_src, 'lxml') 

jobs_html = soup.find_all('a', {'class': 'job-card-list__title'})
 
job_titles = []
 
for title in jobs_html:
    job_titles.append(title.text.strip())
 
print(job_titles)

company_name_html = soup.find_all(
  'div', {'class': 'job-card-container__company-name'})
company_names = []
 
for name in company_name_html:
    company_names.append(name.text.strip())
 
print(company_names)

import re # for removing the extra blank spaces

location_html = soup.find_all(
	'ul', {'class': 'job-card-container__metadata-wrapper'})

location_list = []

for loc in location_html:
	res = re.sub('\n\n +', ' ', loc.text.strip())

	location_list.append(res)

print(location_list)

