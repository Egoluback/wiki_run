import requests
import scipy.spatial.distance as ds

from bs4 import BeautifulSoup
from Vectorizer import Vectorizer

target = 'грибы'
url = 'https://ru.wikipedia.org/wiki/%D0%A7%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D0%BA'

MAX_LINKS = 300

print("Creating new vectorizer...")
vectorizer = Vectorizer(model_file = '204.zip')
print("Done.")

path = []
path_links = [url]
blacklist = []
winCheck = False
backFlag = False

def win():
	global winCheck

	winCheck = True
	print("/" * 40)
	print(f"WIN")
	print("/" * 40)

def back(steps: int = 0):
	global path_links
	global path
	global url
	global backFlag

	url = path_links[-steps]
	print("/" * 40)
	print(f"BACK TO {path[-steps]}")
	print("/" * 40)

	backFlag = True

while True:
	try:
		req = requests.get(url)
	except:
		back()
		continue

	if not req.ok:
		print('something went wrong')
		continue

	soup = BeautifulSoup(req.text, 'html.parser')

	title = soup.find(id='firstHeading').text.lower()

	if url not in blacklist: blacklist.append(url)

	if title in path and not backFlag and len(path) > 0:
		path_links.pop()
		back(1)
		continue
	if title not in path or len(path) == 0:
		path.append(title)
	if path[-1] == target:
		win()
		break

	body = soup.find(id='mw-content-text')

	links = []
	rates = []
	
	a_el = body.find_all('a')
	print(f"{len(a_el)} hyperlinks found.")
	if len(a_el) > MAX_LINKS: print(f"Only {MAX_LINKS}/{len(a_el)} will be processed.")
	a_el = a_el[:MAX_LINKS]
	for j in range(len(a_el)):
		el = a_el[j]
		try:
			if 'wiki' not in el.get('href'): continue
			
			link_ = el.get('href')
			if len(el.text) < 3 or el.text == "[en]" or link_ in links or \
			link_ in url or url in link_ or link_ in blacklist or 'https://ru.wikipedia.org' + link_ in blacklist: continue

			if target not in el.text.lower():
				vect = vectorizer.Vectorize_one(el.text)
				rate = ds.cosine(vect, vectorizer.Vectorize_one(target))
			else:
				rate = (target != el.text.lower()) - 1 # -1 if target == el.text else 0

			links.append(el)
			rates.append(rate)

			print(el.text + " - " + str(rate))
			print("-" * 40 + str(round(j / len(a_el) * 100, 2)) + "%")
			
			if rate == -1:
				win()
				break
		except:
			pass
	if winCheck: break

	if len(rates) == 0:
		back(1)
		continue
	
	next_page = links[rates.index(min(rates))]

	if min(rates) > 1:
		back(1)
		continue

	url = next_page.get('href')
	if 'https://ru.wikipedia.org' not in url: url = 'https://ru.wikipedia.org' + url
	path_links.append(url)

	backFlag = False
	
	print("/" * 40)
	print(f"NEXT PAGE - {next_page.text}")
	print("/" * 40)

print(path_links)
print(path)