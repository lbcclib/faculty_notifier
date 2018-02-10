import lxml.etree as et
import json, os, re, smtplib, urllib, yaml
from book import Book
from department import Department, NotifyAboutEverything, SpanishInterestGroup

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom' # The feed element
ATOM = "{%s}" % ATOM_NAMESPACE # replaces the % and the s and replaces it follwed by anything after % 

config = yaml.safe_load(open('conf/evergreen.yml'))
config.update(yaml.safe_load(open('conf/output.yml')))

departments = []

departments_config = yaml.safe_load(open('conf/departments.yml'))
for d in departments_config['departments']:
	data = d.values()[0]
	departments.append(Department(d.keys()[0], ','.join(data['emails']), data['regex']))

# Add custom departments to the list
departments.append(SpanishInterestGroup('test@example.com'))
departments.append(NotifyAboutEverything('test@example.com'))

if 'shelving_location' in config:
	if isinstance(config['shelving_location'], list):
		loc_string = '&copyLocation='.join(str(location) for location in config['shelving_location'])
	else:
		loc_string = str(config['shelving_location'])
	feed_url = 'http://' + config['opac_host'] + '/opac/extras/browse/atom-full/item-age/' + config['org_unit'] + '/1/' + str(config['num_items_to_fetch']) + '?status=0&status=1&status=6&status=7&copyLocation=' + loc_string # the URL that will return all the data we need
else:
	feed_url = 'http://' + config['opac_host'] + '/opac/extras/browse/atom-full/item-age/' + config['org_unit'] + '/1/' + str(config['num_items_to_fetch']) + '?status=0&status=1&status=6&status=7'

original = et.parse(feed_url) # parse the data from that URL
books = original.findall(ATOM + 'entry') # goes through the xml file that we have in memory and finds everything that is an entry and all the entries are books


books_for_json = []

for book in books: # now that we have data from the book that are being saved in 'books'
	possible_book = Book(book)
	if possible_book.has_image():
		books_for_json.append(possible_book.to_dict())
		for department in departments:
			if department.is_interested_in (possible_book):
				department.mark_book_for_email (possible_book)

for department in departments:
	if department.has_enough_data_for_email():
		department.send_email()

exhibit_data = {'items': books_for_json} #putting in a format that exhibit js can read
with open(config['json_output_path'], 'w') as json_file:
	json_file.write(json.dumps(exhibit_data))
