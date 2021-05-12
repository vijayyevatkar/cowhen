# macbook-cowin-reminder
A simple Python script to remind you of a vaccination slot in your District

# Pre-requisites
1. You need a Mac to run this as it uses "oascript" which is native Macbook desktop reminder.
2. However, if you have python3 installed, try replacing the ```command``` variable with your native desktop notification!
3. (Optional) - Go to System Preferences -> Notifications -> Script Editor => Allow notifications and choose banner. This ensures the notification doesn't timeout.

# Steps to Run
1. Install Python3 (Skip this if you have python3): <https://docs.python-guide.org/starting/install3/osx/>
2. Open Terminal and run the following.  
   $ sudo pip install requests  
   $ python3 remindByDistrict.py  
3. You will get 3 prompts -> District ID, Next 'n' days to be reminded about and phone number.
4. Refer your district_id from the ```districtNames.txt``` file that is present.
5. And, your phone number is needed to copy it to the clipboard. Once a slot is found, the cowin portal is opened automatically and your mobile number is copied to the clipboard.
6. All you have to do is just paste it, click on Get OTP and then book the slot quickly.
