import urllib.request
file = urllib.urlopen('http://helloworld.com/data/message.txt')
message=file.read()
print (message)
