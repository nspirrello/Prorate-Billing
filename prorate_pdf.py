from reportlab.platypus import Paragraph, Table, Image, TableStyle, SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, mm
import os.path
import os
import sys
import time
import datetime

class PdfProrate():

	def resource_path(self, relative_path):
		base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
		return os.path.join(base_path, relative_path)

	def __init__(self, filename, data, numClients):
		i = 1
		original_name = filename
		while os.path.isfile(filename):
			docname = filename[0:len(original_name) - 4]
			extension = '.pdf'
			filename = docname + '(' + str(i) + ')' + extension
			i+=1
		self.file = filename
		self.doc = SimpleDocTemplate(filename,pagesize=letter,rightMargin=30,leftMargin=30,topMargin=30,bottomMargin=18)
		self.elements = []
		self.styles = getSampleStyleSheet()
		self.stylesWrap = self.styles["BodyText"]

		#extract charges for each company, add company name and total to a paragraph, add charges to table columns and rows

		self.data = data
		self.numClients = numClients


	def gen_pdf(self):
		#Create Header bar

		path = self.resource_path('axe_logo_prorate_pdf.png')	
		logo = Image(path)

		self.elements.append(logo)

		#Description
		description = """<font size="12">This table has been outputted through the Billing Prorate application's pdf generator. This file, {}, was generated {}.</font>""".format(self.file,datetime.datetime.now().strftime("%m-%d-%y"))
		desc = Paragraph(description, self.stylesWrap)


		self.elements.append(desc)

		style_table = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                       ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
                       ('VALIGN',(0,0),(0,-1),'TOP'),
                       ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
                       ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                       ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                       ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                       ])
		wrap = self.stylesWrap
		wrap.wordWrap = 'CJK'

		for i in range(0,self.numClients):
			bufferwords = Paragraph("",self.stylesWrap)

			print(self.data)
			name = self.data[i][0]
			total = self.data[i][1]

			tableheader = """<font size="12"> {}    Total: ${}\n </font>""".format(name,total)


			name_and_total = Paragraph(tableheader,self.stylesWrap)

			self.elements.append(bufferwords)
			self.elements.append(name_and_total)
			self.elements.append(bufferwords)


			data = [[Paragraph(cell,wrap) for cell in row] for row in self.data[i][2]]

			data_table = Table(data)
			data_table.setStyle(style_table)

			self.elements.append(data_table)

		self.doc.build(self.elements)


	def coord(self, x, y, unit=1):
		x, y = x * unit, self.height - y * unit
		return x, y