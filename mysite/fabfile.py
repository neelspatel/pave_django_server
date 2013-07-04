from fabric.api import *
from fabric.contrib.console import confirm

remote_code_dir = "pave_django_server/mysite"

env.hosts = ["ubuntu@ec2-54-245-213-191.us-west-2.compute.amazonaws.com"]
env.key_filename = "~/keys/auth/pavekey.pem"

def prepare_deploy(branch_name = "staging"):
	test()
	commit()
	pull("master")
	local ('git checkout master && git merge ' + branch_name)
	push("master")

def pull (branch_name):
	local("git pull origin " + branch_name)

def push(branch_name):
	local('git push origin ' + branch_name)

def test():
	local ('python manage.py test data')

def commit():
    	local("git add -p")
	local("git commit")


def deploy():
	with cd(remote_code_dir):
		sudo("git pull origin master")
	       #sudo("python manage.py migrate data")
		sudo("service apache2 restart")
	
def testFab():
	with cd(remote_code_dir):
		sudo("python testFab.py")	
