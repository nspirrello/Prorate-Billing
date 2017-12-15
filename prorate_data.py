#Nicholas Pirrello
#12/6/17
#Prorate Data
import csv

def main():
	init_parse('J:/AxeCreatives/Tasks/ProrateTask.csv')

def init_parse(filename):
	file = open(filename)
	reader = csv.reader(file, delimiter=',')
	data = list(reader)
	gather_data(data)

def gather_data(list):

	#Need CustomerName, OfferName, ChargeStartDate, ChargeType, UnitPrice, Quantity, 
	#TotalForCustomer, DomainName
	customer_name_col = 0
	offer_name_col = 0
	charge_start_date_col = 0
	charge_type_col = 0
	unit_price_col = 0
	quantity_col = 0
	total_for_customer_col = 0
	domain_name_col = 0

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
		elif list[0][j] == 'DomainName':
			domain_name_col = j

	valid_data_list = []
	for k in range(1,len(list)):
		if list[k][charge_type_col] == 'CYCLE INSTANCE PRORATE' and  float(list[k][total_for_customer_col]) > 0:
			valid_data_list.append(list[k]) 

	print(valid_data_list)
	#parse_data(important_data_block,customer_name_col,offer_name_col,charge_start_date_col,charge_type_col,unit_price_col,quantity_col,total_for_customer_col,domain_name_col)

#def parse_data(list, cname_col, offername_col, chargedate_col, chargetype_col, unitprice_col, quantity_col, customertotal_col, dname_col):








if __name__ == '__main__':
	main()
