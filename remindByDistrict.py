import webbrowser
import requests
import os
import time
import datetime
import sys
import subprocess

headers_dict = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def sendOtp(mobile):
    mob = str(mobile)
    # print("Sending OTP to Mobile: "+mob)
    # postUrl = "https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP"
    # res = requests.post(postUrl,json={'mobile':'{}'.format(mobile)})
    # print("Response: "+res.text)
    # if res.status_code == 200:
    # print("OTP Sent successfully. Opening browser.")
    print("Opening browser.")
    webUrl = 'https://selfregistration.cowin.gov.in/'
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    webbrowser.get(chrome_path).open(webUrl)
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    temp = process.communicate(mob.encode('utf-8'))
    print('Browser Opened, copied your number to clipboard. Just paste and hit Get OTP')
    print('Timing out for 200 secs') # Cowin waits for 180 secs after it sends OTP
    time.sleep(200)

path = "districts.csv"
file2 = open(path,"r+")
valid_district_ids = [int(i) for i in file2.read().split(',')]

district_id = input('Enter district_id (Default is Dharwad: 278. Refer others in "districtNames.txt"): ')
if district_id == '':
    district_id = 278
else:
    district_id = int(district_id)
assert district_id in valid_district_ids, "Enter a valid district id"

num_days = input('Enter next \'n\' days that you want to check the slots (default is 5): ')
if num_days == '':
    num_days = 5
else:
    num_days = int(num_days)
# print(num_days)
assert num_days > 0 and num_days < 31, "Enter n > 0 or n < 31"

mob_num = input('Enter mobile number for clipboard copy: ')
assert len(mob_num)==10, "Enter a valid mobile number"
mob_num = int(mob_num)

k = 0
print("\nStarting -- (Hit ^C to stop)\n===================================\n")
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
        # print("Requesting the url: "+url)
        print("District: "+str(district_id)+", Date: "+str(dateItem))
        response = requests.get(url,headers=headers_dict)
        answers = []
        # print("Res len:" + str(len(responses))+ str(responses[-1].status_code))
        if response.status_code == 200:
            try:
                items = response.json()['sessions']
                for item in items:
                    if item['min_age_limit'] < 45:
                        center = str(item['name'])+", "+str(item['address'])+", "+str(item['date'])+", "+str(item['pincode'])
                        answers.append(center)
                if len(answers)>0:
                    i=0
                    for answer in answers:
                        i=i+1
                        title = "New Slot-"+str(k)
                        message = answer
                        command = f''' osascript -e 'display notification "{message}" with title "{title}"' '''
                        os.system(command)
                        sendOtp(mob_num)
            except:
                print('Failed while parsing the response. Add below error to: '+"https://github.com/vijayyevatkar/macbook-cowin-reminder")
                e = sys.exc_info()[0]
                print(e)
        else:
            print("Call to Cowin Public API failed. Check if it's down or come back after some time.")
        time.sleep(3)