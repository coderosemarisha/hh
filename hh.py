import requests
import csv
from bs4 import BeautifulSoup as bs

headers = {'accept':'*/*', 'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.107'}


base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'


def hh_parse(base_url, headers):
	jobs = []
	urls = []
	urls.append(base_url)
	session = requests.Session()
	request = session.get(base_url, headers=headers)

	if request.status_code == 200:
		soup = bs(request.content, 'lxml')
		try:
			pagination = soup.find_all('a', attrs={'data-qa':'pager-page'})
			count = int(pagination[-1].text)
			for i  in range(count):
				url = f'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page={i}'
				if url not in urls:
					urls.append(url)
		except:
			pass

	for url in urls:
		request = session.get(url, headers=headers)
		soup = bs(request.content, 'lxml')
		divs = soup.find_all('div', attrs={'data-qa':'vacancy-serp__vacancy'})
		for div in divs:
			try:
				title = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'}).text
				href = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-title'})['href']
				company = div.find('a', attrs={'data-qa':'vacancy-serp__vacancy-employer'}).text
				text1 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
				text2 = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
				content = text1 + ' ' + text2
				salary = div.find('div', attrs={'data-qa':'vacancy-serp__vacancy-compensation'}).text
				city = div.find('span', attrs={'data-qa':'vacancy-serp__vacancy-address'}).text
				jobs.append({
					'title':title,
					'href':href,
					'company':company,
					'content':content,
					'salary':salary,
					'city':city,
					})
			except:
				pass
			print(len(jobs))
	else:
		print('ERROR or DONE. Status code =  ' + str(request.status_code))
	return jobs

def files_writer(jobs):
	with open('parsed_jobs.csv', 'w')as file:
		a_pen = csv.writer(file)
		a_pen.writerow(('City','Title vacancy','Salary', 'URL', 'Name of company', 'Content vacancy'))
		for job in jobs:
			a_pen.writerow((job['city'], job['title'], job['salary'], job['href'], job['company'], job['content']))


jobs = hh_parse(base_url, headers)
files_writer(jobs)