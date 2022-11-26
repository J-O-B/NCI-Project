# NCI Project

## <ins>**Intro**</ins>
This project forms part of the final submission in the Higher Diploma in Cybersecurity with the National College. 

Focused on providing enhanced layers of security for end users, this application aims to safely store user credentials by using layers of security that enhance the CIA triad.

At this point in time, the project is a POC based on evidence collected regarding various security flaws. This project is not intended for public use.

***As this project is a POC, and doesn't currently satisfy data privacy laws (including GDPR), this project has not been deployed. Debug is still enabled and other key security measures that would often be in place, including environment variables have not been implemented.***

------------------------------------------------------------------------------
## <ins>**Project Outline**</ins>
### *Browser Security*

Many modern browsers that operate on both Windows & Linux operating systems offer users the capabilities of storing sensitive data, including login information, credit cards and in some cases, biometric data. 

Whilst data saved within browsers is generally encrypted using strong encryption algorithms, the key used is weak, leading to weakened data security.

### *Encryption & Decryption*
When browsers wish to encrypt data, many browsers rely on the encryption techniques used by the operating system, such as CryptProtectData within Windows. 

If a victim's computer is compromised, or in some cases, visits a link to a webpage, then malicious code is capable of obtaining the encryption keys. From here, data stored in the corresponding browser directories can be decrypted.

------------------------------------------------------
## <ins>**UX Design**</ins>
Whilst this project is more security focused, we must also consider UX design to help end users easily navigate and use the application. As such various UX features have been included in this project, including:

### <ins>**5 Planes Of UX:**</ins>
1. ***Strategy:***

    - Users will be able to create and manage accounts,
    - Users will be able to login and logout,
    - Users will be able to recover lost login credentials,
    - Users will be able to add 'Known IP Addresses',
    - Users will be able to add 'Known Devices',
    - Users will be able to store sensitive data,
    - Users will be able to retrieve sensitive data.
2. ***Scope:***

    - *Functional Requirements:*
        
        1. A user must be able to login or logout,
        2. A user must be able to register a new account,
        3. A user must be required to confirm their account (email),
        4. A user must be provided with a unique PIN & Secret Key,
        5. A user must be capable of adding known devices & IP addresses,
        6. A User must be capable of retrieving saved data,
    - *Content Requirements:*
        
        1. Pages must contain only relevant content to that specific page,
        2. Content must be kept to an absolute minimum level required,
3. ***Structure:***

    - *Login / Register:*
        - Prior to using the app, all requests will result in users being redirected to a page offering to login or register.
    - *Main Dashboard:*
        - Logged in users will automatically have their dashboard presented to them where session cookies exist. 
        - A basic navigation menu is presented to a user through side buttons:
            - Profile,
                - View Profile Information,
                - Edit Profile Information,
                - Links to add 'Known IP' & 'Known Device'.
            - Add IP
                - Semi automated process that allows the addition of a known IP.
            - Add Device
                - Semi automated process that allows the addition of a known device.
            - View / Add Credentials
                - View Credentials
                    - User presented with various services
                        - Specific service credentials (i.e. Facebook Login)
                - Add Credentials
                    - Form presented to user where they may add credentials.
4. ***Skeleton:***

    To create a structure for this application, key areas were defined. These areas will allow for complete functionality as intended by the application. These include:

    1. Main Splash Screen
        - A target for redirection where no session exists.
    2. Dashboard
        - The main page for an authenticated user. Target of redirects where needed.
    3. Profile
        - An area where users can view / edit their profile.
    4. Whitelisting
        - Areas where users can add known devices / IP addresses.
    5. Credentials
        - A page that will allow for adding / viewing of credentials.

5. ***Surface:***

    Although the main goal of this application is to enhance security, it also aims to provide users with a positive user experience, which is aided through simplicity in design, primarily ease of use.

    Users will receive intended feedback based on certain criteria where possible. In areas such as Login, feedback is provided, although this feedback may sometimes be generic in nature to avoid security implications.


### <ins>**User Stories:**</ins>
1. ***As A Developer I Want To:***
    
    1. Allow users to register,
    2. Allow users to login,
    3. Allow users to add known IP addresses,
    4. Allow users to add known devices,
    5. Allow users to add credentials,
    6. Allow users to edit profile information,
    7. Provide minimal information to users.
2. ***As A User I Want To:***
    
    1. Edit my profile,
    2. Add credentials,
    3. Delete credentials,

### <ins>**Information Architecture:**</ins>
For this project, I wanted to create a secure application, therefore the flow of information and data is of utmost importance. 

It is important to ensure that specific user groups only have access to information that is intended for that specified user.

***Administration Users***

This user group is intended potentially for staff or a similar high level user. Whilst this user group has not been specifically used in the application, this user should not have unrestricted access to all database records, but rather have access to higher level data, such as usernames of users, email addresses etc.

***Authenticated Users***

Authenticated users shall have restricted access to the application. These users shall be capabable of editing their profile, and adding credentials, however the retrieval of data shall incorporate various other security measures, thus restricting their interaction with data.

***Non Members***

Users who do not have an account, or do not have an active session will not be capable of using the application. These users will only have access to the main screen, as well as the various account pages (Login, Register, Forgot Password etc.)

### <ins>**Responsive Design:**</ins>
As this application is intended for use within a browser extension, then we need to consider the fact that the window will be of limited dimensions. 

Just like regular web pages, responsive design is implemented with Bootstrap (version 5) to ensure pages are loaded in a responsive manner.

-----------------------------
## <ins>**Features**</ins>

The main features of this application take place on the back-end of the program. Features such as the encryption and decryption of data, two-factor authentication, session management, reverse requests, and various whitelisting are all incorporated on the back-end.

### ***Current Features:***
- SHA-256 Encryption
- Automated & Strong Key Strength Generation
- User Profiles
- Web Hooks
- Error Handling
- Whitelisting
- User Enumeration Protection
    - e.g. "Username and/or password incorrect"
- Admin Panel
- Email Confirmations
- User Input Sanitization
- Header Smuggling Protection
- Rate Limiting
- Brute Force Protections

### ***Future Features:***
- Biometric Two-Factor Authentication
- Proximity Based Authentication


---------------------------------
## <ins>**Technologies Used**</ins>

### **Languages**
1. HTML / HTML5
    
    - HTML makes up the foundation of this project, including all templates and content displayed to end users.

2. CSS / CSS3

    - CSS3 is used for all styling throughout this application.

3. JavaScript / jQuery

    - JavaScript is used for various styling effects & transitions, as well as data manipulation in some cases.

4. Python / Django

    - Django provides the framework for this project. Handling all urls, and specific functionality. This framework provides the application with the ability to manipulate data, perform various back end tasks and direct information in various directions.

        For example, a request to view a specific credential record will result in:
        - Whitelisting check (IP and Device), 
        - PIN check, 
        - Retrieval of encrypted data, 
        - Cross check between user and record, 
        - Cross check between user pin and record, 
        - Decryption of data.

### **Frameworks, Libraries & Other**
1. VS Code
    - Visual Studio Code was used as the IDE for this project.
2. Network Repository
    - A custom repository present on my local network was used to host project files.
3. Git
    - GIT was used for version control to cimmit to Git and push to the network repository.
4. GitHub
    - GitHub is used to host the final submission of project directories & files.
5. Cryptography
    - The cryptography library within Python was used for the encryption of data.
6. Fernet
    - Fernet was used to ensure the integrity of secret keys.
7. PBKDF2
    - PBKDF2 was used to apply padding where needed for encryption keys.

------------------------
## <ins>**Testing**</ins>

This project has passed through several phases of testing, these include:
1. W3 Validator
    - To check all HTML.
2. W3 'Jigsaw' Validator
    - To check all CSS.
3. JS Hint
    - To check all JavaScript.
4. PEP 8
    - To check all Python code.
5. Auto Prefixer
    - To check browser compatability with various CSS
6. Flake 8
    - Check for general errors in Python.
7. Console.Log
    - Whilst not primarily a testing tool, specific outputs were output to the terminal to assist in debugging & testing.
8. Dev Tools
    - As a means of testing responsiveness and other visual problems, Chrome Dev Tools was used to simulate various device screens. This allowed for the testing and correction of visual flaws.
9. Chrome 'Lighthouse'
    - Lighthouse was used to find and fix performance, accessability, best practices and SEO issues.

### **Bugs & Issues**

### Data Privacy:
    As this application does not have policies in place that are available to end users, it is currently not configured to allow public usage.

### Denial of Service Testing:
    As this application has not been deployed, the testing of Denial of Service has not been tested in a live environment.

-----------------
## <ins>**Deployment**</ins>
### **Requirements For Deployment**
- Amazon AWS Account
- Heroku Account

### **Cloning This Project**
To create a clone of this project, the following steps can be taken:
1. Login to GitHub and navigate to the 'Project' directory,
2. Click on the button with the text 'Code',
3. Click "Open with GitHub Desktop" and follow the prompts in the GitHub Desktop Application or follow the instructions from [GitHub](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/cloning-a-repository#cloning-a-repository-to-github-desktop) to see how to clone a repository using different methods.

### **Working With A Local Clone**
1. Install the requirements from the 'requirements.txt' file using PIP.
2. Build a new database by running the "python manage.py makemigrations" and "python manage.py migrate" commands.
3. Create a new superuser using the "python manage.py createsuperuser" command.
4. Run the django application using "python manage.py runserver".
5. Login using your superuser credentials (e.g 127.0.0.1:8000/accounts/login)
6. From the admin menu, you can quickly create, read, update and delete records including user credentials, saved IPs, saved Devices, user profiles, user accounts. 

***As this is a fresh install, the database will be empty, with the exception of the superuser account and profile***

### **Deployment To Heroku**
Although this application has not been hosted, the following steps can be followed to deploy the application. These steps will walk through the steps needed on both Heroku & AWS.

To deploy the project on Heroku, the application **must** have a requirements.txt file as well as a Procfile. These files will allow Heroku to find the dependencies & versions are required to run the application, as well as identify the source file to run in order to launch the web application.

#### **Required Files**
1. Create A Procfile:
    - Type "python app_name.py > Procfile" in the terminal.
2. Create A Requirements.txt File:
    - Type "pip freeze --local > requirements.txt"

#### **Deploy To Heroku**
1. Open [Heroku](https://heroku.com)
2. Login or signup,
3. Once logged in, create a new app and select the desired region to host the application.
4. Deployment method "GitHub" (If this step is accidentally missed, you can use the tab selection within your dashboard labeled "Deploy")
5. Select "Connect to GitHub" and follow the on screen instructions. Once connected to your GitHub:
    - Search for your project repository using the form provided.
6. Once you have connected your GitHub Repository:
    - Navigate to the "Settings" tab
        - Scroll to the section labeled "Config Vars":
            - Input any environment variables, such as secret keys in the fields provided. (ensure names match those in settings.py)
    - Navigate back to the "Deploy" tab:
        - Select the "Manual Deploy" tab:
            - Select the branch you wish to deploy from (i.e "Main", "Master" etc.)
            - Click the "Deploy Branch" button. (this will take some time)
            > TIP: Once a build is successful, a "View App" button will be presented. By clicking on this button, you can tell if the build was successful. The app may not look correct due to ongoing configuration, however, if the app loads, the build was a success.

#### **Deploy To AWS (S3 Bucket)**
Prior to completing this step, the application will have no styling and may not be capable of functioning due to all static files, including CSS & JavaScript missing from the local deployment.

*You Will Require An AWS Account Prior To These Steps Being Taken*

1. Open [Amazon AWS](https://aws.amazon.com/)
2. Click Create Account and follow the steps.

#### **Creating The S3 Bucket**
1. Sign into the console.
2. Under the "AWS Services" search box, type "S3" and click the associated service.
3. Click the "Create Bucket" button.
4. Provide a name, and the closest hosting region to you.
5. Uncheck the "Block All Public Access" checkbox & accept that the bucket will be public.
6. Click "Create Bucket" at the end of the form.
7. Click on the name of your bucket to enter the area specific to this project.
8. Click "Properties" & select "Static website hosting" to enabled.
9. In the popup, click "Use this bucket to host a website".
10. Although we won't use these fields, they are required, you can use "index.html" and "error.html" for the index & error document fields.
11. Click save.
12. Click on the "Permissions" tab and select "CORS Configuration".
13. Paste in the following code into the area provided:
    
        [ 
            { 
                "AllowedHeaders": [ "Authorization" ], 
                "AllowedMethods": [ "GET" ], 
                "AllowedOrigins": [ "*" ], 
                "ExposeHeaders": [] 
            } 
        ]
    **If The Application Will Have A Static IP, Set This In The "AllowedOrigins" Field**
14. Click Save.
15. Click on the "Bucket Policy" tab:
    1. Copy the "ARN".
    2. Select Policy Generator.
    3. Use the following settings for the form:
        - Policy Type: S3 Bucket Policy,
        - Add Statements: 
            - Effect: "Allow",
            - Principal: "*",
            - Actions: "GetObject",
            - ARN: *Paste in ARN copied earlier*
16. Click "Add Statement", followed by "Generate Policy".
17. Copy the generated policy and paste it back into the Bucket Policy Editor.
18. Add "/*" to the end of the "Resource" part of the code.
19. Click save.
20. Click the "Access Control List" under the "Permissions" tab. 
21. Under the "Everyone (Public Access)", Click the "List Objects" option.
22. Click save.

#### **AWS S3 Bucket Access Control**

1. Click on the "Services" tab on the top left of the page.
2. Search for "IAM" and click the associated service.
3. Add this service and navigate (if not redirected) to the IAM dashboard.
4. Under the "Access Management" tab, click "Groups".
5. Create a new group by providing a name, then click "next" without any further configuration (which will be done in the next steps).
6. At the end of the form, select "Create Group"
7. Click "Policies" under the "Access Management" tab.
8. Click "Create Policy", then open the JSON tab.
9. Click "Import Managed Policy"
10. Select the "AmazonS3FullAccess" option and click "Import"
11. Now to only allow specific access to the project bucket. In a new tab go back to the S3 bucket and copy the "ARN" again from the bucket policy page.
12. Now in the JSON Policy for the IAM group, next to resources remove the "/*" and add the following:
    
        "Resource": [
            "arn: YOUR ARN CODE",
            "arn: YOUR ARN CODE/*",
        ]
13. Now click "Review Policy"
14. Provide a name and description and click "Create Policy"
15. Click on "Groups" under the Access Management section.
16. Click on the group you have created for this project.
17. Under Permissions, click "Attach Policy"
18. Search for the policy you just created and select it using the checkbox.
19. Click "Attach Policy"

#### **Adding A User To Access Control**
1. Click the "Users" from under the Access Management section.
2. Select "Add User".
3. Provide a user name, and select "Programmatic access".
4. Click next for permissions.
5. Select the group for the project using the checkbox provided.
6. Click all the way through to the end without changing any further details.
7. At the end of the form you will be given some user credentials, here you can download a CSV file with the user access keys.

>*To finalize the setup, add your access keys to the environment variables in the Heroku Config Variables. This will allow your Django application to use these settings on the deployed project.*

> *To ensure these keys work, you must configure the settings file of your django application to find these variables using os.environ.*

> Further information on setting environment variables can be found here: [Django Docs](https://docs.djangoproject.com/en/3.2/topics/settings/)
