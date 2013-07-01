from fabric.api import local

def prepare_deploy(branch_name = "staging"):
	test()
	commit()
	local ('git checkout master && git merge ' + branch_name)

def test():
	local ('python manage.py test data')

def commit():
    local("git add -p && git commit")

def deploy():
	code_dir = '..'
	with lcd()
