<html>
<body>
<h1>Sample README</h1>

A project dedicated to Email Rules.
<h2>STEPS for having the setup.<h2>
<h3>Google Setup</h3>
<h4> Google Oauth Account Setup </h4>
<p>
1. Open Google Cloud Console <br/>
2. Select a Project -> New Project <br/>
3. Name your project <br/>
4. Select your organization or leave it as "No Organization" <br/>
5. Click Create <br/>
6. In Google Cloud Console. go to Apis and Services -> Library <br/>
7. Search for GMAIL Api -> Click on it and Enable it. <br/>
8. Now go to Apis and Services -> Credentials <br/>
9. Create Credentials -> Oauth Client ID<br/>
10. You may need to configure the Oauth Consent Screen first.<br/>
11. Select External or Internal depending on use.<br/>
12. Fill in app name, User Support Email, Developer Contact Email.<br/>
13. Choose Application type -> Desktop App<br/>
14. Name it and create and download credentials.json file.<br/>
</p>


<h4> Setting GMAIL Scopes </h4>
1. Inside OAuth consent screen, scroll down to the Scopes section.(inside Data Access Menu) <br/>
2. Click Add or Remove Scopes. <br/>
3. In the list, search for or paste: <br/>
https://www.googleapis.com/auth/gmail.modify <br/>
https://www.googleapis.com/auth/gmail.readonly <br/>
4. Check the box next to it. <br/>
5. Click Save and Continue. <br/>

<h4> Setting up test users </h4>
1. Still in the OAuth consent screen, scroll to the Test users section. <br/>
2. Click Add Users. <br/>
3. Enter the email addresses that will be allowed to test the app (typically your Gmail account). <br/>
4. Click Save and Continue. <br/>

<h3> Setting up pycharm configuration </h3>
1. There is a requirements.txt which needs to be used to install python packages. Run the following command in order to install it. <br/>
python3 -m pip install -r requirements.txt <br/>
2. Make sure the interpreter is well setup accordingly. Feel free to use a virtual environment to get everything setup. <br/>
(Use this :-)<br/> python3 -m venv venv <br/> source venv/bin/activate <br/>

3. Run python scripts/authenticate_and_list.py to test the google Oauth Setup. It should use credentials.json in order to fill up token.json. Once you run the script a tab of browser should open up to accept permissions. <br/>
4. Once you observe that token.json has been filled you can consider a successful google Oauth Setup.
5. If things don't work out try manually adding python interpreter and packages as well. <br/>
6. We are using SQLite so no specific setup is needed at all for db/table. <br/>

<h4> Running main script </h4>
1. The rules are present in data/rules.json. Use that to have a go at the rules.
2. To run the script and see it's working nature run:- <br/>
python scripts/main.py
3. You should see few logs appearing in terminal which should confirm the working.

</body>
</html>