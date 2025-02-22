# Wellington
A Scanner/Scraper that finds Scam Sites.
### TODO
- [ ] FOCUS: Improve the control panel, add a CLI preview maybe?
- [ ] Make it find and attribute/tag those your-file-is-ready-to-download.zip scam sites.
- [ ] FOCUS: Create API and documentation (mainly for get requests).
- [ ] Release SSL Version (does exist in my version).
- [x] Find a better Newly Registered Domains list.

# Setup
### Packages
Linux: Run the install_dependencies.sh, Have FLASK and Flask-HTTPAuth Installed.  
  
Windows: python3 and PIP, Chromium. FOR PYTHON: requests beautifulsoup4 selenium webdriver-manager Flask-HTTPAuth.  
### Guide
Step 1. Run the main.py and wait until it starts saying scanning ... etc.  
Step 2. Kill the Main.py task.  
Step 3. Download the control-panel.html and the index.html from the web directory in the repo, then move them into a folder named "templates".  
Step 4. Create the screenshots directory and create the scams.txt file.  
Step 5. Run the main.py and check if it is scanning.  
Step 6. Kill the main.py task, open the main.py file and change the Username and Password using nano or another IDE.  
### Optional
Step 7. Port Forward Port 6945.  
Step 8. Go to http://YOUR-IP:6945/ (change YOUR-IP to your server or computer's IP).  
Step 9. If all is seemingly working, visit http://YOUR-IP:6945/control-panel then enter the username and password you put in the main.py. Once logged in, press the start scan button.  
Step 10. Installing SSL: It is optional but I strongly believe that you should install it.  
# API
Lorem Ipsum...
