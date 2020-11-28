from pyArango.connection import *

conn = Connection(arangoURL='http://35.233.27.39:30852', username="root", password="jalapeno")
db = conn["jalapeno"]

nodes = db["LSNode"].fetchAll()
for node in nodes:
	print(node)
	print()