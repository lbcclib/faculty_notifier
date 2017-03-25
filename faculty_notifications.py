import lxml.etree as et
import json, os, re, smtplib, urllib, yaml
from book import Book
from department import Department

ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom' # The feed element
ATOM = "{%s}" % ATOM_NAMESPACE # replaces the % and the s and replaces it follwed by anything after % 

config = yaml.safe_load(open('conf/evergreen.yml'))
config.update(yaml.safe_load(open('conf/output.yml')))

departments = []

departments.append(Department('Agriculture/Horticulture department', 'sandbej@linnbenton.edu', r'^(HD140[1-9]|HD14[1-9][0-9]|HD1[5-9][0-9]{2}|HD2[01][0-9]{2}|HD220[0-9]|HD2210|S[0-9]+|SB[0-9]+|TJ148[0-9]|TJ149[0-6]|QK[0-9]+).*'))
departments.append(Department('Biology department', 'sandbej@linnbenton.edu', r'^(GE[0-9]|QH[0-9]|QK[0-9]|QL[0-9]|QM[0-9]|QP[0-9]|QR[0-9]|TP248\.1[3-9]|TP248\.[2-5]|TP248\.6[0-5]).*'))
departments.append(Department('Business department', 'sandbej@linnbenton.edu', r'^(HB[0-9]|HC[0-9]|HD[0-9]|HE[0-9]|HF[0-9]|HG[0-9]|HJ[0-9]).*'))
departments.append(Department('Center for Accessibility Resources', 'sandbej@linnbenton.edu', r'^(HV155[3-9]|HV15[6-9][0-9]|HV1[6-9][0-9]{2}|HV2[0-9]{3}|HV300[0-4]|KF480|LC481[2-9]|LC48[2-9][0-9]|LC49[01][0-9]|LC492[0-8]|NA2547|RA440|RC553.A88|RC569\.[7-9]|RC57[0-4]).*'))
departments.append(Department('Chemistry department', 'sandbej@linnbenton.edu', r'^QD.*'))
departments.append(Department('Communication department', 'sandbej@linnbenton.edu', r'^(GN345\.6|HM258|P8[7-9]|P9[0-6]|PN4[0-2][0-9]{2}|PN43[01][0-9]|PN432[01])(\.|\s).*'))
departments.append(Department('Computer Science department', 'sandbej@linnbenton.edu', r'^(HD69\.P75|HF5548\.[45]|QA75\.[5-9][0-9]*|QA76\.[0-8][0-9]*|QA76\.9[0-5][0-9]*|T56\.*)(\.|\s).*'))
departments.append(Department('Counseling department', 'sandbej@linnbenton.edu', r'^(BF636|LB2343)(\.|\s).*'))
departments.append(Department('Culinary arts department', 'sandbej@linnbenton.edu', r'^TX(537|63[1-9]|6[4-9][0-9]|[78][0-9]{2}|9[0-4][0-9]|95[0-3])(\.|\s).*'))
departments.append(Department('Criminal justice department', 'sandbej@linnbenton.edu', r'^(HV[678][0-9]{3}|HV9[0-8][0-9]{2}|HV99[01][0-9]|HV9920|KF9[67][0-9]{2}|KF98[01][0-9]|KF982[0-7]).*'))
departments.append(Department('Dental assistant department', 'sandbej@linnbenton.edu', r'^RK.*'))
departments.append(Department('Developmental studies department', 'sandbej@linnbenton.edu', r'^LB2331\.2.*'))
departments.append(Department('Diagnostic imaging department', 'sandbej@linnbenton.edu', r'^RC78\.7.*'))
departments.append(Department('Drafting and engineering graphics department', 'sandbej@linnbenton.edu', r'^(T35[1-9]|T36[0-9]|T37[01]|TA174)(\.|\s).*'))
departments.append(Department('Education and HDFS department', 'sandbej@linnbenton.edu', r'^(GN480|GT24[6-8][0-9]|GT2490|HV699|HV[7-9][0-9]{2}|HV1[0-3][0-9]{2}|14[0-4][0-9]|HQ75\.27|HQ75\.53|HQ77[789]|HQ78[01]|HQ79[3-9]|L[ABC]?[0-9]+)(\.|\s).*'))
departments.append(Department('ELA department', 'sandbej@linnbenton.edu', r'^(LB1572|LB1576|P11[89]|P12[01]|PE110[89]|PE111[0-4]|PE1128\.A2|PE113[1-9]|PE1404)(\.|\s).*'))
departments.append(Department('Engineering department', 'sandbej@linnbenton.edu', r'^(T[AJK][0-9]+|TP15[56])(\.|\s).*'))
departments.append(Department('English/Writing department', 'sandbej@linnbenton.edu', r'^(LB2360|PE140[2-9]|PE14[1-8][0-9]|PE149[0-7]|PN335[5-9]|PN33[67][0-9]|PN338[0-5]|T11|T11\.[0-5])(\.|\s).*'))
departments.append(Department('Health and Human Performance / PE Department', 'sandbej@linnbenton.edu', r'^(GV20[1-9]|GV2[1-9][0-9]|GV[3-9][0-9]{2}|GV10[0-9]{2}|GV11[0-8][0-9]|GV119[0-8]|RC12[0-3][0-9]|RC124[0-5])(\.|\s).*'))
departments.append(Department('History department', 'sandbej@linnbenton.edu', r'^([CDEF][0-9]+)(\.|\s).*'))
departments.append(Department('Journalism department', 'sandbej@linnbenton.edu', r'^PN(4699|4[7-9][0-9]{2}|5[0-5][0-9]{2}|56[0-5][0-9]).*'))
departments.append(Department('Machine tool', 'sandbej@linnbenton.edu', r'^(TJ11[89][0-9]|TJ1[012][0-9]{2}|TJ130[0-9]|TJ131[0-3]).*'))
departments.append(Department('Math department', 'sandbej@linnbenton.edu', r'^(HA|QA[1-6]|QA7[0-5]|QA7[89]|QA[89]).*'))
departments.append(Department('Mechatronics department', 'sandbej@linnbenton.edu', r'^(TJ163\.12|TK7875).*'))
departments.append(Department('Medical assisting department', 'sandbej@linnbenton.edu', r'^(HG937[1-9]|HG93[89][0-9]|QM[0-9]+|R118|R123|R728\.8|RA[1-9]|RA[1-9][0-9]|RA[123][0-9]{2}|RA40[0-9]|RA41[0-5]|RC683.5.E5|RS[0-9]+)(\.|\s).*'))
departments.append(Department('Music department', 'sandbej@linnbenton.edu', r'^(M|ML|MT)[0-9]+.*'))
departments.append(Department('Nursing and CNA department', 'sandbej@linnbenton.edu', r'^(Q[MP]|R[ST])[0-9]+.*'))
departments.append(Department('Occupational therapy assistant department', 'sandbej@linnbenton.edu', r'^(BF71[2-9]|BF72[1-3]|BF724|QM[0-9]+|RM69[5-9]|RM[78][0-9]{2}|RM9[0-4][0-9]|RM950)(\.|\s).*'))
departments.append(Department('Philosophy department', 'sandbej@linnbenton.edu', r'^(B[0-9]+|BJ[1-9]|BJ[1-9][0-9]{1,2}|BJ1[0-5][0-9]{2}|BJ16[0-8][0-9]|BJ169[0-7])(\.|\s).*'))
departments.append(Department('Physics department', 'sandbej@linnbenton.edu', r'^Q[BC][0-9]+.*')) 
departments.append(Department('Psychology department', 'sandbej@linnbenton.edu', r'^(BF[0-9]+|R726\.[5-8]|RC32[1-9]|RC3[3-9][0-9]|RC4[0-9]{2}|RC5[0-6][0-9]|RC57[01])(\.|\s).*'))
departments.append(Department('Religion department', 'sandbej@linnbenton.edu', r'^(B[LMPQRSTVX]|KB)[0-9]+(\.|\s).*'))
departments.append(Department('Small Business Development Center', 'sandbej@linnbenton.edu', r'^(HD67\.2|HD2340\.[89]|HD234[0-5]|HD2346\.[0-5]|HF5679).*'))
departments.append(Department('Sociology department', 'sandbej@linnbenton.edu', r'^(E184|H[MNQSTV][0-9]+).*'))
departments.append(Department('Spanish department', 'sandbej@linnbenton.edu', r'^(PC407[3-9]|PC4[1-8][0-9]{2}|PC49[0-6][0-9]|PC497[01]|PQ603[7-9]|PQ60[4-9][0-9]|PQ6[1-7][0-9]{2}|PQ8[0-4][0-9]{2}|PQ85[01][0-9]).*'))
departments.append(Department('Theater department', 'sandbej@linnbenton.edu', r'^(PN15[3-9][0-9]|PN1[6-9][0-9]{2}|PN[23][0-9]{3}|PN4[0-2][0-9]{2}|PN43[0-4][0-9]|PN435[0-5]).*'))
departments.append(Department('VICE council', 'sandbej@linnbenton.edu', r'^(BF575\.P9|E184\.A1|E185\.6|GN345\.6|GN469|GN495\.8|HF5549\.5\.A34|HF5549\.5\.M5|HM146|HT150[1-9]|HT151[0-9]|HT152[01]|K3242|LC19[1-9]|LC20[0-9]|LC21[0-3]|LC214\.[0-4]|LC214\.5[0-3]|LC1099|LC1[1-9][0-9]{2}|LC[234][0-9]{3}|LC50[0-9]{2}|LC51[0-5][0-9])(\.|\s).*'))
departments.append(Department('Visual arts department', 'sandbej@linnbenton.edu', r'^(N[0-9]|NA|NB|NC|ND|NE|NK|NX|TR).*'))
departments.append(Department('Water, Environment and technology department', 'sandbej@linnbenton.edu', r'^TD7(4[1-9]|[5-7][0-9]|80)(\.|\s).*'))
departments.append(Department('Welding department', 'sandbej@linnbenton.edu', r'^T(S21[5-9]|S22[0-8]|T211)(\.|\s).*'))

feed_url = 'http://' + config['opac_host'] + '/opac/extras/browse/atom-full/item-age/' + config['org_unit'] + '/1/' + str(config['num_items_to_fetch']) + '?status=0&copyLocation=' + str(config['shelving_location']) # the feed element 
original = et.parse(feed_url) # the et.parse is the library beinged used to get the data from the url and then it puts the data inot memory and pases it in xml
books = original.findall(ATOM + 'entry') # goes through the xml file that we have in memory and finds everything that is an entry and all the entries are books

books_for_json = []

for book in books: # now that we have data from the book that are being saved in 'books'
	possible_book = Book(book)
	if possible_book.has_image():
		books_for_json.append(possible_book.to_dict())
		for department in departments:
			if department.is_interested_in (possible_book.call_number):
				department.mark_book_for_email (possible_book)

for department in departments:
	if department.has_enough_data_for_email():
		department.send_email()


exhibit_data = {'items': books_for_json} #putting in a format that exhibit js can read
with open(config['json_output_path'], 'w') as json_file:
	json_file.write(json.dumps(exhibit_data))
