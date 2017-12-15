from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QPushButton, QTableWidget,QTableWidgetItem,QGridLayout,QHeaderView, QFileDialog, QInputDialog, QLineEdit, QMessageBox
import sys

class Summary(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):



		data = [['JJS Transportation',['Plan 1','Plan 2'],['11.09.17','12.03.17'],['Monthly','Yearly'],['$4.95','$5.95'],'$109.67'],['KIDSMILES',['Plan 2'],['11.09.17'],['Monthly'],['$4.95'],'$16.85'],['HELFNER',['Plan 3'],['11.09.17'],['Monthly'],['$4.95'],'$56.34'],5]
		self.tableWidget = QTableWidget()
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(len(data)-1)
		self.tableWidget.setHorizontalHeaderLabels("Company Name;Total;Company Charges".split(";"))

		self.tableWidget.horizontalHeader().setDefaultSectionSize(160)
		self.tableWidget.horizontalHeader().setStretchLastSection(True)

		self.tableWidget.verticalHeader().setDefaultSectionSize(56+(30 * (data[len(data)-1]-1)))
		#for row in range(0,len(data)):
		
		
		for table in range(0,3):
			something = self.create_nested_table(data[len(data)-1])
			for on in range(0,len(data[table][1])):
				something.setItem(on,0,QTableWidgetItem(data[table][1][on]))
			for sd in range(0,len(data[table][2])):
				something.setItem(sd,1,QTableWidgetItem(data[table][2][sd]))
			for ct in range(0,len(data[table][3])):
				something.setItem(ct,2,QTableWidgetItem(data[table][3][ct]))
			for up in range(0,len(data[table][4])):
				something.setItem(up,3,QTableWidgetItem(data[table][4][up]))
			self.tableWidget.setCellWidget(table,2,something)
			self.tableWidget.setItem(table, 0, QTableWidgetItem(data[table][0]))
			self.tableWidget.setItem(table, 1, QTableWidgetItem(data[table][5]))

		grid = QGridLayout()
		grid.addWidget(self.tableWidget,1,1,5,5)

		self.setLayout(grid)
		self.setGeometry(300,300,1000,800)
		self.show()

	def create_nested_table(self, rowcount):
		nestedTableWidget = QTableWidget()
		nestedTableWidget.setColumnCount(4)
		nestedTableWidget.setRowCount(rowcount)
		nestedTableWidget.setHorizontalHeaderLabels("Offer Name;Start Date;Charge Type;Unit Price".split(";"))
		nestedTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		nestedTableWidget.verticalHeader().setDefaultSectionSize(30)
		return nestedTableWidget



if __name__ == '__main__':
	app = QApplication(sys.argv)
	summary = Summary()
	sys.exit(app.exec_())