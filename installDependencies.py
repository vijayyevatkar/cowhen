import os

installSuccess = True
try:
	command = 'pip install requests --upgrade'
	os.system(command)
	print('\nInstalled "requests" package\n')
except:
    print('Couldn\'t install "requests" package.\n')
    e = sys.exc_info()[0]
    print(e)
    installSuccess = False

try:
	command = 'sudo pip install plyer --upgrade'
	os.system(command)
	print('\nInstalled "plyer" package\n')
except:
    print('Couldn\'t install "plyer" package.\n')
    e = sys.exc_info()[0]
    print(e)
    installSuccess = False

message = ''
if installSuccess:
	message = 'Successfully installed all the dependencies. Please run "remindByDistrict.py"'
else:
	message = 'Could not install all the dependencies.\nCreate an issue on: '+"https://github.com/vijayyevatkar/macbook-cowin-reminder/issues"
print(message)
