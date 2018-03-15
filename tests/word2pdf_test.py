# Test word2pdf
# Sean Higgins
# 14mar2018

# Tell Python to recognize where it's saved in Python path
import sys 
sys.path.append('C:/Dropbox/PythonTools')
	# Local copy of https://github.com/skhiggins/PythonTools/
	
# Import function
from word2pdf import word2pdf

# Test .docx
word2pdf('C:\\Dropbox\\PythonTools\\tests\\example_word.docx')

# Test .doc
word2pdf('C:\\Dropbox\\PythonTools\\tests\\example_word.doc')

