from boto.s3.connection import S3Connection
from boto.s3.key import Key
import Image
import urllib2
import os
import cStringIO
import datetime
import subprocess

def process_image(url):
	file = cStringIO.StringIO(urllib2.urlopen(url).read())
	img = Image.open(file)
	os.chdir("tmp")
	filename = "ugproduct_%s.jpg" % datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	img.save(filename)
	# process image here
	new_filename = "processed_" + filename
	subprocess.call(["convert", filename, "-resize", "100x100^","-unsharp", "2x0.5+0.7+0", "-quality", "98", "-gravity", "center", "-extent", "100x100", new_filename])
	upload_image(new_filename)
	upload_image(filename)
	#os.remove(filename)

def upload_image(filename):
	con = S3Connection('AKIAJ5NFFKY3KUKBRTPQ','Z3heEPRxIvB0KXxLEaYZ69rpdOsQYXx2cwfprHpf')
	bucket = con.create_bucket('ug_product_images')
	k = bucket.new_key(filename)
	k.key = filename
	k.set_contents_from_filename(filename)
	k.set_acl('public-read')
process_image("http://images.bloomingdales.com/is/image/BLM/products/6/optimized/8126866_fpx.tif?wid=1200&qlt=90,0&layer=comp&op_sharpen=0&resMode=sharp2&op_usm=0.7,1.0,0.5,0&fmt=jpeg")
