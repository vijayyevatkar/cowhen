import webbrowser
import requests
import time
import datetime
import sys
import subprocess
import os

headers_dict = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

path = "districts.csv"
file2 = open(path,"r+")
valid_district_ids = [int(i) for i in file2.read().split(',')]

goAhead = False
trueList = ['','Y','y','Yes','yes','YEs','yEs','YeS','yeS','YES','yES']

# Default values
mode = 1
district_id = 278
num_days = 5
mob_num = ''

while not goAhead:
    # Get the system mode 
    system = input('Enter System Mode (Default is Macbook: 1), Enter 2 for Windows: ')
    mode = 2 if system == '2' else 1

    # Get the District ID
    district_id = input('Enter district_id (Default is Dharwad: 278. Refer others in "districtNames.txt"): ')
    if district_id == '':
        district_id = 278
    else:
        district_id = int(district_id)
    assert district_id in valid_district_ids, "Enter a valid district id"

    # Get the next 'n' days for slot checks
    num_days = input('Enter next \'n\' days that you want to check the slots (default is 5): ')
    if num_days == '':
        num_days = 5
    else:
        num_days = int(num_days)
    assert num_days > 0 and num_days < 31, "Enter n > 0 or n < 31"

    # Get the mobile number for copying it to clipboard
    mob_num = input('Enter mobile number for clipboard copy: ')
    print('\n===== Information Entered =====\n')
    book = 'Macbook' if mode == 1 else 'Windows'
    print('System: {0}\nDistrict: {1}\nCheck slot for days: {2}\nClipboard Mobile Number: {3}\n'.format(book,district_id,num_days,mob_num))
    userConfirmation = input('Press enter to continue if above information is correct. No otherwise: ')
    goAhead = True if userConfirmation in trueList else False

if mode == 2:
    from plyer import notification

# On windows:
def windowsClip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

# On Mac
def macbookClip(txt):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    return process.communicate(txt.encode('utf-8'))

# sendOtp(mobile, 1) => For Mac
# sendOtp(mobile, 2) => For Windows
def sendOtp(mobile, mode=1):
    mob = str(mobile)
    print("Opening browser.")
    webUrl = 'https://selfregistration.cowin.gov.in/'
    webbrowser.open(webUrl,new=2)
    temp = macbookClip(mob) if mode==1 else windowsClip(mob)
    print('Browser Opened, copied your number to clipboard. Just paste and hit Get OTP')
    print('Timing out for 200 secs') # Cowin waits for 180 secs after it sends OTP
    time.sleep(200)

# =======================
# Start the slot notifier
# =======================
k = 0
print("\n===================================\nStarting -- (Hit ^C to stop)\n===================================\n")
while True:
    today = datetime.date.today()
    dateArray = []
    for i in range(1,num_days+1):
        d1 = today+datetime.timedelta(days=i)
        dateArray.append(d1.strftime('%d-%m-%Y'))
    print("Checking slots for next {0} days.".format(num_days))
    print("Run #{0}".format(k+1))
    for dateItem in dateArray:
        k+=1
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id="+str(district_id)+"&date="+str(dateItem)
        print("Requesting the url: "+url)
        print("District: "+str(district_id)+", Date: "+str(dateItem))
        response = requests.get(url,headers=headers_dict)
        answers = []
        print("Res status:" + str(response.status_code))
        if response.status_code == 200:
            try:
                items = response.json()['sessions']
                print(items)
                for item in items:
                    if item['min_age_limit'] == 45:
                        center = str(item['name'])+", "+str(item['address'])+", "+str(item['date'])+", "+str(item['pincode'])
                        answers.append(center)
                if len(answers)>0:
                    i=0
                    for answer in answers:
                        i=i+1
                        title = "New Slot-"+str(k)
                        message = answer
                        if mode == 1:
                            print("ayo, mode is: "+str(mode))                    
                            command = f''' osascript -e 'display notification "{message}" with title "{title}"' '''
                            os.system(command)
                            print("eyo")
                        else:
                            notification.notify(title= title,message= message,app_icon = None,timeout= 3600,toast=False)
                        sendOtp(mob_num)
            except Exception as e:
                print('\nFailed while parsing the response. Create issue here: '+"https://github.com/vijayyevatkar/macbook-cowin-reminder/issues\n")
                print(str(e)+"\n")
        else:
            print("Call to Cowin Public API failed. Check if it's down or come back after some time.")
        time.sleep(3)
