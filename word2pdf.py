# Word to PDF 
# Sean Higgins
# 14mar2018

# Compatible with Windows only

import sys
import os
import re
from win32com import client

def word2pdf(in_file):
	"""
	Note: must use the '\\' on Windows instead of the '/'
	Note: close word, might need to taskkill /F /IM winword.exe in command prompt
	must use the '\\' on Windows instead of the '/'
	
	Example:	
		word2pdf('C:\\Dropbox\\PythonTools\\tests\\example_word.docx')
	"""
	word = client.DispatchEx("Word.Application")
	doc = word.Documents.Open(in_file)
	out_file = re.sub('\\.docx?$', r'.pdf', in_file) # x? is so doc or docx
	doc.SaveAs(out_file, FileFormat = 17) # 17 is pdf
	doc.Close()
	word.Quit()
	print("Converting %s ---> %s" % (in_file, out_file))
	
