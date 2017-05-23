import re, smtplib, yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

config = yaml.safe_load(open('conf/email.yml'))

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
	def is_interested_in(self, call_number):
		if re.match(self.call_number_match, call_number) is not None:
			return True
		else:
			return False
# create a new method outside of Department class with spansih dep category
                
        def spanish_language(self, call_number):
                if re.match(self.categories, category) is not None:
                        return True
                else:
                        return False

                # The book's are being attached to the email 
	def mark_book_for_email(self, book):
		self.books_of_interest.append(book)
        # The fallowing object makes sure there is enough data or content in the email message
	def has_enough_data_for_email(self):
		if config['min_items_per_email'] <= len(self.books_of_interest):
			return True
		else:
			return False
        # The following function sends the emails to the right departments with the right content 
	def send_email(self):
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "New books at the LBCC Library"
		msg['From'] = config['email_sender']
		msg['To'] = self.email
		html = '<html><head></head> <body><p>Dear colleagues in the ' + self.name + ',</p>'
		html = html + '<p>We\'ve recently added some books/materials to our collection that we think you might be interested in:</p>'
		images_attached = 0
		book_number = 0
		while ((images_attached < config['max_items_per_email']) and (book_number < len(self.books_of_interest))):
			if hasattr(self.books_of_interest[book_number], 'cover_image_url'):
				html = html + self.books_of_interest[book_number].to_html()
				images_attached = images_attached + 1 # increase the first loop by one and continue until you reach 8
			book_number = book_number + 1 # if the default cover image is the same as the first URL image then increase the loop by one and conitneu the loop

		html = html + '<p>A more complete listing is available at this link.  Please <a href="mailto:hawkinr@linnbenton.edu">contact Richenda Hawkins at hawkinr@linnbenton.edu</a> if you would like us to purchase other materials for our collection.<p>'
		html = html +   '<br><br>Thanks,<br><br><br>LBCC Library'
		html = html + '</body></html>'
		#print(html)
		part2 = MIMEText(html, 'html')
		msg.attach(part2)
		mail = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
		mail.ehlo()
		mail.starttls()
		mail.login(config['email_sender'], config['email_password'])
		mail.sendmail(config['email_sender'], self.email, msg.as_string())
		mail.quit()
