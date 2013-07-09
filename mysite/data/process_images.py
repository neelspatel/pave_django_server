from boto.s3.connection import S3Connection
from boto.s3.key import Key
import Image
import urllib2
import os
import cStringIO
import datetime
import subprocess

def process_image(url, filename):
	file = cStringIO.StringIO(urllib2.urlopen(url).read())
	img = Image.open(file)
	os.chdir("tmp")
	old_filename = "old_" + filename
	img.save(old_filename)
	# process image here
	new_filename = filename
	subprocess.call(["convert", old_filename, "-resize", "100x100^","-unsharp", "2x0.5+0.7+0", "-quality", "98", "-gravity", "center", "-extent", "100x100", new_filename])
	upload_image(new_filename)
	os.remove(old_filename)
	os.chdir("..")

def upload_image(filename):
	con = S3Connection('AKIAJ5NFFKY3KUKBRTPQ','Z3heEPRxIvB0KXxLEaYZ69rpdOsQYXx2cwfprHpf')
	bucket = con.create_bucket('ug_product_images')
	k = bucket.new_key(filename)
	k.key = filename
	k.set_contents_from_filename(filename)
	k.set_acl('public-read')
