Aimport re, urllib, yaml
import lxml.etree as et

# Load configuration
config = yaml.safe_load(open('conf/cover_images.yml'))

# Constants that help in retrieving data from XML 
ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom' # The feed element
ATOM = "{%s}" % ATOM_NAMESPACE # replaces the % and the s and replaces it follwed by anything after %
DC_NAMESPACE = 'http://purl.org/dc/elements/1.1/'
DC = "{%s}" % DC_NAMESPACE
HOLDINGS_NAMESPACE = 'http://open-ils.org/spec/holdings/v1' #the URL is from evergreen which is how the library inputs call numbers and other data
HOLDINGS = "{%s}" % HOLDINGS_NAMESPACE
BOOK_VOLUME_XPATH = HOLDINGS + 'holdings/' + HOLDINGS + 'volumes/' + HOLDINGS + 'volume'
VOLUME_COPY_XPATH = HOLDINGS + 'copies/' + HOLDINGS + 'copy'
BOOK_COPY_XPATH = BOOK_VOLUME_XPATH + '/' + VOLUME_COPY_XPATH
# The following class finds the tite of the book, the author's name, the link to the book, the date that it was added, ISBN, call- number, cover-image, and it's location
class Book:
	def __init__(self, raw_book_data):
		self.title = raw_book_data.find(ATOM + 'title').text.encode('utf-8').strip(' /')
		author = raw_book_data.find(ATOM + 'author')
		if author is not None:
			self.author = re.sub(r'([-\.]\(OrAlC\)[0-9]*)', '', author.find(ATOM + 'name').text)
                        
		links = raw_book_data.findall(ATOM + 'link')
		for link in links:
			if 'opac' == link.get('rel'):
				self.uri = link.get('href')
				break

                categories = raw_book_data.findall(ATOM + 'category')
                for category in categories:
                        if 'Spanish Language.' == category.get('term'):
                                self.spanish = category.get('term')
                                break

		date_cat = raw_book_data.find(ATOM + 'updated')
		if date_cat is not None:
			self.date_cataloged = date_cat.text

		isbns = raw_book_data.findall(DC + 'identifier')
		if isbns:
			for isbn in isbns:
                                url_substitution = (re.subn('URN.ISBN.([X0-9]{10,13}).*', 'http://' + config['cover_image_host'] + '/' + config['cover_image_prefix'] + r'\1' + config['cover_image_suffix'], isbn.text))
                                if 1 == url_substitution[1]:
                                        cover_image_url = url_substitution[0]
                                        if self.is_cover_image_good(cover_image_url):
                                                self.cover_image_url = cover_image_url
                volumes = raw_book_data.findall(BOOK_VOLUME_XPATH)
                for volume in volumes:
                        #if org_unit == volume.get('lib'):
			self.call_number = volume.get('label')
			shelving_location = volume.find
			self.shelving_location = volume.find(VOLUME_COPY_XPATH + '/' + HOLDINGS + 'location').text
	def has_image(self):
		return hasattr(self, 'cover_image_url')
	def to_dict(self):
		if hasattr(self, 'author'):
			return {'label': self.title, 'call-number': self.call_number, 'cover-image': self.cover_image_url, 'uri': self.uri, 'author': self.author}
		else:
			return {'label': self.title, 'call-number': self.call_number, 'cover-image': self.cover_image_url, 'uri': self.uri}
	def to_html(self):
		html = '<a href="' + self.uri + '">'
		html = html + '<img src="'+ self.cover_image_url + '" alt="' + self.title + '" />'
		html = html + '</a>'
		return html

	# Checks for cover images and if not available them
	def is_cover_image_good(self, cover_image_url):
    		response = urllib.urlopen(cover_image_url) #request cover image
    		headers = response.info() #we look at the headers that were sent back
    		if 'Content-Type' in headers: # if the connect type is in the header
        		if config['cover_image_mime_type'] == headers['Content-Type']: # makes sure that it's a jpge and not a strange format
		    		return True
