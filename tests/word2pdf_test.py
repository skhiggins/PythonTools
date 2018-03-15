# Test word2pdf

# Tell Python to recognize where it's saved in Python path
import sys 
sys.path.append('C:/Dropbox/PythonTools')
	# Local copy of https://github.com/skhiggins/PythonTools/
	
# Import function
from word2pdf import word2pdf

# Test
word2pdf('C:\\Dropbox\\PythonTools\\tests\\example_word.docx')

