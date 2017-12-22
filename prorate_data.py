#Nicholas Pirrello
#12/6/17
#Prorate Data
import csv
from pprint import pprint

#def main():
#init_parse('J:/AxeCreatives/Tasks/ProrateTask.csv')

def init_parse(filename):
	file = open(filename)
	reader = csv.reader(file, delimiter=',')
	data = list(reader)
	return(gather_data(data))

def gather_data(list):


	customer_name_col = 0
	offer_name_col = 0
	charge_start_date_col = 0
	charge_type_col = 0
	unit_price_col = 0
	quantity_col = 0
	total_for_customer_col = 0

	for j in range(0,len(list[0])):
		if list[0][j] == 'CustomerName':
			customer_name_col = j
		elif list[0][j] == 'OfferName':
			offer_name_col = j
		elif list[0][j] == 'ChargeStartDate':
			charge_start_date_col = j
		elif list[0][j] == 'ChargeType':
			charge_type_col = j
		elif list[0][j] == 'UnitPrice':
			unit_price_col = j
		elif list[0][j] == 'Quantity':
			quantity_col = j
		elif list[0][j] == 'TotalForCustomer':
			total_for_customer_col = j

	valid_data_list = []
	for k in range(1,len(list)):
		if list[k][charge_type_col] == 'CYCLE INSTANCE PRORATE':
			valid_data_list.append(list[k]) 

	return(extract_data(valid_data_list, customer_name_col, offer_name_col, charge_type_col, charge_start_date_col, unit_price_col,quantity_col, total_for_customer_col))

def extract_data(datalist, customer_name_col, offer_name_col, charge_type_col, charge_start_date_col, unit_price_col, quantity_col, total_for_customer_col):
	extractlist = []
	for row in range(0,len(datalist)):
		cname = datalist[row][customer_name_col]
		oname = datalist[row][offer_name_col]

		ct = datalist[row][charge_type_col]

		csd = datalist[row][charge_start_date_col]
		up = datalist[row][unit_price_col]
		qt = datalist[row][quantity_col]
		tc = datalist[row][total_for_customer_col]

		if is_in(extractlist,cname) == True:
			for i in extractlist:
				if i['customername'] == cname:
					i['charges'][0].append(ct)
					i['charges'][1].append(oname)
					i['charges'][2].append(csd)
					i['charges'][3].append(up)
					i['charges'][4].append(qt)
					i['charges'][5].append(tc)
					i['total'] = str(round(float(i['total']) + round(float(tc),2),2))
		else:
			new_data = {'customername':cname,'charges':[[ct],[oname],[csd],[up],[qt],[tc]],'total':str(round(float(tc),2))}
			extractlist.append(new_data)

	longest_row_count = len(extractlist[0]['charges'][1])
	for j in extractlist:
		nextinstance = len(j['charges'][1])
		if nextinstance > longest_row_count:
			longest_row_count = nextinstance

	extractlist.append(longest_row_count)
	pprint(extractlist)
	return(extractlist)


def is_in(list, name):
	#If the specified name is found in the list, return True, otherwise False
	for i in list:
		if i['customername'] == name:
			return(True)
	return(False)
