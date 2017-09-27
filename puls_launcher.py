import urllib2
import zipfile 

SOURCE = "https://github.com/gibma/puls/archive/master.zip"
APP = "test.py"

def setup_proxy():
	proxy = urllib2.ProxyHandler({'https': 'localhost:3128'})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)

def download_file(url, file):
	
	with open('_package.tmp','wb') as f:
		url = urllib2.urlopen(SOURCE, timeout=30)
		f.write(url.read())
		f.close()

def unzip():
	zip = zipfile.ZipFile('_package.tmp', 'r')
	zip.extractall('.')
	zip.close()
		
if __name__ == "__main__":

	setup_proxy()
	
	download_file(SOURCE, "temp.zip")
	
	unzip()
