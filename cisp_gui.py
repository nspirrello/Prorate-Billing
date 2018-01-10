from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QPushButton, QTableWidget,QTableWidgetItem,QGridLayout,QHeaderView, QFileDialog, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import os
import prorate_data
import prorate_pdf

class Summary(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def resource_path(self, relative_path):
		base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
		return os.path.join(base_path, relative_path)

	def initUI(self):

		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Warning)
		self.msg.setStandardButtons(QMessageBox.Ok)
		self.msg.setWindowTitle('Warning!')

		self.import_bttn = QPushButton('Import')
		self.reset_bttn = QPushButton('Reset')
		self.enlarged_text = QLineEdit()
		self.enlarged_text.setReadOnly(True)
		self.save_btn = QPushButton('Save as PDF')

		self.import_bttn.clicked.connect(self.imprt_data)
		self.reset_bttn.clicked.connect(self.rst_data)
		self.save_btn.clicked.connect(self.save_data)

		self.list_nested = []
		self.data = None
	
		self.tableWidget = QTableWidget()
		self.tableWidget.setColumnCount(3)

		self.tableWidget.setHorizontalHeaderLabels("Company Name;Total;Company Charges".split(";"))

		self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.tableWidget.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
		
		grid = QGridLayout()
		grid.addWidget(self.tableWidget,1,1,5,5)
		grid.addWidget(self.enlarged_text,6,1,1,2)
		grid.addWidget(self.reset_bttn,6,5,1,1)
		grid.addWidget(self.import_bttn,6,3,1,1)
		grid.addWidget(self.save_btn,6,4,1,1)

		self.setLayout(grid)
		self.setGeometry(200,200,1000,800)

		path = self.resource_path('axe_logo.png')
		self.setWindowIcon(QIcon(path))

		self.setWindowTitle('AXE CISP Billing')
		self.show()

	def create_nested_table(self, rowcount):
		nestedTableWidget = QTableWidget()
		nestedTableWidget.setColumnCount(5)
		nestedTableWidget.setRowCount(rowcount)
		nestedTableWidget.setHorizontalHeaderLabels("Offer Name;Start Date;Unit Price;Quantity;Total Price".split(";"))
		nestedTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		nestedTableWidget.verticalHeader().setDefaultSectionSize(30)
		return nestedTableWidget

	def cell_selected(self, row, column):
		table = self.sender()
		item = table.item(row,column)
		if item != None:
			self.enlarged_text.setText(item.text())

	def imprt_table(self):
		self.list_nested = []
		self.tableWidget.setRowCount(len(self.data)-1)
		
		self.tableWidget.verticalHeader().setDefaultSectionSize(56+(30 * (self.data[len(self.data)-1]-1)))

		for table in range(0,len(self.data)-1):
			something = self.create_nested_table(self.data[len(self.data)-1])
			self.list_nested.append(something)
			for offer in range(0, len(self.data[table]['charges'][1])):
				item = QTableWidgetItem(self.data[table]['charges'][1][offer])
				something.setItem(offer,0,item)
				item.setFlags(item.flags() & (~Qt.ItemIsEditable))
			for sd in range(0,len(self.data[table]['charges'][2])):
				item = QTableWidgetItem(self.data[table]['charges'][2][sd])
				something.setItem(sd,1,item)
				item.setFlags(item.flags() & (~Qt.ItemIsEditable))
			for up in range(0,len(self.data[table]['charges'][3])):
				item = QTableWidgetItem(self.data[table]['charges'][3][up])
				something.setItem(up,2,item)
				item.setFlags(item.flags() & (~Qt.ItemIsEditable))
			for qt in range(0,len(self.data[table]['charges'][4])):
				item = QTableWidgetItem(self.data[table]['charges'][4][qt])
				something.setItem(qt,3,item)
				item.setFlags(item.flags() & (~Qt.ItemIsEditable))
			for tc in range(0,len(self.data[table]['charges'][5])):
				item = QTableWidgetItem(self.data[table]['charges'][5][tc])
				something.setItem(tc,4,item)
				item.setFlags(item.flags() & (~Qt.ItemIsEditable))
				
			self.tableWidget.setCellWidget(table,2,something)
			self.tableWidget.setItem(table, 0, QTableWidgetItem(self.data[table]['customername']))
			self.tableWidget.setItem(table, 1, QTableWidgetItem(self.data[table]['total']))

		for i in range(0,len(self.list_nested)-1):
			nested = self.list_nested[i]
			nested.cellClicked.connect(self.cell_selected)

	def convert_data(self,data):
			data_list = []

			for i in range(0,len(self.data)-1):
				current_data = []
				current_data.append(self.data[i]['customername'])
				current_data.append(self.data[i]['total'])

				table_data = [['Offer Name','Start Date','Unit Price','Quantity','Total Price']]
				for j in range(0,len(self.data[i]['charges'][0])):
					table_row = []
					table_row.append(self.data[i]['charges'][1][j])
					table_row.append(self.data[i]['charges'][2][j])
					table_row.append(self.data[i]['charges'][3][j])
					table_row.append(self.data[i]['charges'][4][j])
					table_row.append(self.data[i]['charges'][5][j])

					table_data.append(table_row)
				current_data.append(table_data)
				data_list.append(current_data)
			return data_list

	def imprt_data(self):
		filename = QFileDialog.getOpenFileName(self,'Open File','C://','CSV (*.csv)')[0]
		if filename:
			try:
				self.rst_data()
				self.data = prorate_data.init_parse(filename)
				self.imprt_table()
			except:
				self.msg.setInformativeText('Data trying to be loaded is in improper format.')
				self.msg.setText('Invalid csv file format!')
				self.msg.exec_()



	def rst_data(self):
		self.tableWidget.clear()
		self.tableWidget.setHorizontalHeaderLabels("Company Name;Total;Company Charges".split(";"))

		self.enlarged_text.setText('')

	def save_data(self):
		if self.data == None:
					self.msg.setText('No table data loaded!')
					self.msg.setInformativeText('Load in table data before saving into a PDF.')
					self.msg.exec_()
					return None
		try:
			text, okPressed = QInputDialog.getText(self,"PDF Saving","PDF File Name:",QLineEdit.Normal,"")
			if text == '':
				self.msg.setText('No PDF file name!')
				self.msg.setInformativeText('No PDF file name was given.')
				self.msg.exec_()
				return None
			if okPressed:

				converted_data = self.convert_data(self.data)
				doc = prorate_pdf.PdfProrate(text+".pdf",converted_data,len(self.data)-1)
				doc.gen_pdf()
		except:
				self.msg.setText('Unexpected PDF generation error!')
				self.msg.setInformativeText('Check for valid file name and for sensible table data.')
				self.msg.exec_()

		


if __name__ == '__main__':
	app = QApplication(sys.argv)
	summary = Summary()
	sys.exit(app.exec_())