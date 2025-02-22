# Wellington
A Scanner/Scraper that finds Scam Sites.
### TODO
- [ ] Make it find and attribute/tag those your-file-is-ready-to-download.zip scam sites.
- [ ] Find a better Newly Registered Domains list.

# Setup
### Packages
Linux: Run the install_dependencies.sh, Have FLASK Installed.  
  
Windows: python3, Chromium, libnss3, libgconf-2-4, libxi6, libgdk-pixbuf2.0-0, libxcomposite1, libasound2, libxrandr2, libatk1.0-0, libgtk-3-0, FOR PYTHON: flask python3-pip requests beautifulsoup4 selenium webdriver-manager.
### Guide
Step 1. Run the main.py and wait until it starts saying scanning ... etc.
Step 2. Kill the Main.py task
Step 3. Move the control-panel.html and the index.html into the "templates" folder (flask should've generated it).
Step 4. Create the screenshots directory and create the scams.txt file.
Step 5. Run the main.py and check if it is scanning.
Step 6. Kill the main.py task, open the main.py file and change the Username and Password using nano or another IDE.
### Optional
Step 7. Port Forward Port 6945.
Step 8. Go to http://YOUR-IP:6945/ (change YOUR-IP to your server or computer's IP).
