from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QPushButton, QTableWidget,QTableWidgetItem,QGridLayout,QHeaderView, QFileDialog, QInputDialog, QLineEdit, QMessageBox
import sys
import prorate_data

class Summary(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):


		#Swap OfferName to the end, set a defaultSectionSize for the 4 other columns and strecth the offer name
		#For the nestedTable


		import_bttn = QPushButton('Import')
		reset_bttn = QPushButton('Reset')
		enlarged_text = QLineEdit()
		enlarged_text.setReadOnly(True)



		data = prorate_data.init_parse('J://AxeCreatives/Tasks/ProrateTask.csv')
	
		self.tableWidget = QTableWidget()
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(len(data)-1)
		self.tableWidget.setHorizontalHeaderLabels("Company Name;Total;Company Charges".split(";"))

		self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.tableWidget.verticalHeader().setDefaultSectionSize(56+(30 * (data[len(data)-1]-1)))
		self.tableWidget.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
		

		for table in range(0,len(data)-1):
			something = self.create_nested_table(data[len(data)-1])
			for offer in range(0, len(data[table]['charges'][1])):
				something.setItem(offer,0,QTableWidgetItem(data[table]['charges'][1][offer]))
			for sd in range(0,len(data[table]['charges'][2])):
				something.setItem(sd,1,QTableWidgetItem(data[table]['charges'][2][sd]))
			for up in range(0,len(data[table]['charges'][3])):
				something.setItem(up,2,QTableWidgetItem(data[table]['charges'][3][up]))
			for qt in range(0,len(data[table]['charges'][4])):
				something.setItem(qt,3,QTableWidgetItem(data[table]['charges'][4][qt]))
			for tc in range(0,len(data[table]['charges'][5])):
				something.setItem(tc,4,QTableWidgetItem(data[table]['charges'][5][tc]))
			self.tableWidget.setCellWidget(table,2,something)
			self.tableWidget.setItem(table, 0, QTableWidgetItem(data[table]['customername']))
			self.tableWidget.setItem(table, 1, QTableWidgetItem(data[table]['total']))

		grid = QGridLayout()
		grid.addWidget(self.tableWidget,1,1,5,5)
		grid.addWidget(enlarged_text,6,1,1,2)
		grid.addWidget(reset_bttn,6,4,1,1)
		grid.addWidget(import_bttn,6,5,1,1)

		self.setLayout(grid)
		self.setGeometry(200,200,1000,800)
		self.show()

	def create_nested_table(self, rowcount):
		nestedTableWidget = QTableWidget()
		nestedTableWidget.setColumnCount(5)
		nestedTableWidget.setRowCount(rowcount)
		nestedTableWidget.setHorizontalHeaderLabels("Offer Name;Start Date;Unit Price;Quantity;Total Price".split(";"))
		nestedTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		nestedTableWidget.verticalHeader().setDefaultSectionSize(30)
		#nestedTableWidget.cellClicked.connect(self.cell_selected,nestedTableWidget)
		return nestedTableWidget

	def cell_selected(self, row, column, nested):
		item = nested.itemAt(row, column)
		enlarged_text.setText(item.text())



if __name__ == '__main__':
	app = QApplication(sys.argv)
	summary = Summary()
	sys.exit(app.exec_())