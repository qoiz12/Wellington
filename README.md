# Wellington
A Scanner/Scraper that finds Scam Sites and ranks them by potential and very likely. Comes with NO WARRANTY!
### TODO
- [ ] **FOCUS:** Improve the control panel, CSS changes likely.
- [ ] **FOCUS:** Scanning Status, Time until next scan etc (in control pane).
- [ ] Release SSL Version (does exist in my private version).
- [ ] Make a version that finds and attributes/tags those Your File Is Ready To Download malware sites.
- [X] Create API and documentation (mainly for POST requests).
- [x] Publish Repo.
- [x] Find a better Newly Registered Domains list.

# Setup
### Packages
Linux: Run the install_dependencies.sh.  
Windows: Run the install_dependencies.bat
### Guide
**Note: If you're running it on a remote server, port forward the 6945 port before running Wellington.**  
Step 1. Download the latest release.  
Step 2. Move the control-panel.html and the index.html into a folder named "templates".  
Step 3. Create the "screenshots" directory and create the "scams.txt" file inside the templates folder.  
Step 4. Run the main.py and visit http://YOUR-IP:6945/control-panel (change YOUR-IP to your server or computer's IP) and enter USER as the Username and PASS as the Password. After, press the start button. Then go back to the terminal/cmd wait a little bit then check if it is scanning sites.  
Step 5. Kill (CTRL+C) the main.py task, open the main.py file and change the Username and Password using Nano or another IDE.  
Step 6. Visit the control panel and use the password and username you set earlier, if it lets you in; you have followed the guide correctly!
### Optional
Step 7. Port Forward Port 6945 if you haven't already.  
Step 8. Go to http://YOUR-IP:6945/ on another device (change YOUR-IP to your server or computer's IP).  
Step 9. If all is seemingly working, visit http://YOUR-IP:6945/control-panel then enter the username and password you put in the main.py. Once logged in, press the start scan button.  
Step 10. Installing SSL: It is optional but I strongly believe that you should install it.  
Step 11. Change the API_KEY = "your-secret-api-key"  (replacing the quoted text with a secure API key) on line 35 in the main.py file.  
# POST API
### List of filters (the / separates the options):  
```
'{
    "filter": {
        "category": "potential/very likely"
    },
    "urls_only": true/false
    
}'
```
"urls_only" will return with just the urls, "category" filters urls by the 2 categories (if you want all urls, remove the "category" argument).  
  
### Example Request (Curl):
```
curl -X POST http://SERVER-IP:6945/api \
-H "Content-Type: application/json" \
-H "X-API-Key: your-secret-api-key" \
-d '{
    "filter": {
        "category": "potential"
    },
    "urls_only": false
    
} '
```
Returns all urls under the "potential" category.
