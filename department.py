import datetime, re, smtplib, yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

config = yaml.safe_load(open('conf/email.yml'))
config.update(yaml.safe_load(open('conf/output.yml')))

class Department:
	# name is a string containing the name of the department
	# email is a string containing email addresses of all department members separated by a comma
	# call_number_match is a regular expression to determine books relevant to the department
	def __init__(self, name, email, call_number_match):
		self.name = name
		self.email = email
		self.call_number_match = call_number_match
		self.books_of_interest = []
        # The regular expression is looking for relevant books to it's department by matching the book to it's department
	def is_interested_in(self, book):
		if re.match(self.call_number_match, book.call_number) is not None:
			return True
		else:
			return False

        # Attach books to the department object
	def mark_book_for_email(self, book):
		self.books_of_interest.append(book)

        # The fallowing object makes sure there is enough data or content in the email message
	def has_enough_data_for_email(self):
		if config['min_items_per_email'] <= len(self.books_of_interest):
			return True
		else:
			return False

	def salutation(self):
		return "Dear colleagues in the " + self.name

	def subject(self):
		return "New books at the LBCC Library"

	def closing_words(self):
		html = '<p>A more complete listing is available at ' + config['link'] + '. Please contact <a href="mailto:hawkinr@linnbenton.edu">Richenda Hawkins</a>'
		html = html + ' if you would like us to purchase other materials for our collection.</p>'
		html = html +   '<br><br>Thanks,<br><br><br>LBCC Library'
		return html

        # The following function sends the emails to the right departments with the right content 
	def send_email(self):
		msg = MIMEMultipart('alternative')
		msg['Subject'] = self.subject()
		msg['From'] = config['email_sender']
		msg['To'] = self.email
		html = '<html><head></head> <body><p>' + self.salutation() + ',</p>'
		html = html + '<p>We\'ve recently added some books/materials to our collection that we think you might be interested in:</p>'
		images_attached = 0
		book_number = 0
		with open(config['log_path'], 'a') as log_file:
			while ((images_attached < config['max_items_per_email']) and (book_number < len(self.books_of_interest))):
				if hasattr(self.books_of_interest[book_number], 'cover_image_url'):
					html = html + self.books_of_interest[book_number].to_html()
					log_file.write(str(datetime.datetime.now()) + ': ' + self.books_of_interest[book_number].title + " emailed to " + self.name + "\n")
					images_attached = images_attached + 1 # increase the first loop by one and continue until you reach 8
				book_number = book_number + 1 # if the default cover image is the same as the first URL image then increase the loop by one and conitneu the loop

		html = html + self.closing_words()
		html = html + '</body></html>'
		#print(html)
		part2 = MIMEText(html, 'html')
		msg.attach(part2)
		mail = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
		mail.ehlo()
		mail.starttls()
		mail.login(config['email_sender'], config['email_password'])
		mail.sendmail(config['email_sender'], self.email.split(','), msg.as_string())
		mail.quit()

class SpanishInterestGroup(Department):
	# Simpler init, becaues we don't need a call_number_match or name
	def __init__(self, email):
		self.email = email
		self.name = "Spanish Interest Group"
		self.books_of_interest = []

	def is_interested_in(self, book):
		if hasattr(book, 'language'):
			if 'es' == book.language:
				return True
		return False

	def salutation(self):
		return "Dear colleagues who enjoy reading in Spanish"

class ChildrensLit(Department):
	def __init__(self, email):
		self.email = email
		self.name = "Children's Literature enthusiasts"
		self.books_of_interest = []

	def is_interested_in(self, book):
		if hasattr(book, 'shelving_location'):
			if book.shelving_location in ["Children's chapter books", "Children's literature"]:
				return True
		return False

	def salutation(self):
		return "Dear colleagues interested in childrens' literature"

class NotifyAboutEverything(Department):
	def __init__(self, email):
		self.email = email
		self.name = "Spanish Interest Group"
		self.books_of_interest = []

	def is_interested_in(self, book):
		return True

	def salutation(self):
		return "Dear Burlington Public Library enthusiast" 

	def subject(self):
		return "New books at the Burlington Public Library"

	def closing_words(self):
            html = '<p>A more complete listing is available at ' + config['link'] + '. Please use <a href="http://www.burlingtonwa.gov/FormCenter/Library-8/Suggest-a-Title-55">this form</a> '
            html = html + 'to suggest other titles</p>'
            html = html + '<br><br>Thanks,<br><br><br>Burlington Public Library'
            return html
