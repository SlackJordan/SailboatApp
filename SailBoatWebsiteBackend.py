from distutils.filelist import findall
from bs4 import BeautifulSoup as BS
import requests
import re
import pandas as pd
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#global variables
places = {}

craigslistSites = requests.get('https://www.craigslist.org/about/sites')
soup = BS(craigslistSites.content, 'html.parser')

links = [a.get('href') for a in soup.find_all('a', href=True)]

def Show_Links():
    index = 0
    for link in links:
        for match in re.findall('https://(\w+)', link):
            if match != 'www' and match != 'forums':
                places[index]=match
            
        index+=1

data = {'City':[],'ID': [],'Name': [], 'Price': [], 'Link': [], 'Picture':[]}

def sailboat_search(city, max):
    search = requests.get(f'https://{city}.craigslist.org/search/boo?query=sailboats&min_price=1&max_price={max}&boat_propulsion_type=1')
    html_soup = BS(search.text,'html.parser')

    ads = html_soup.find_all('li',class_= 'result-row')

    for i in range(len(ads)):
        result_heading = ads[i].find('h3', class_='result-heading')
        price = ads[i].a.text.strip()
        name = result_heading.a.text.strip()
        id = result_heading.a['data-id'].strip()
        linksec = result_heading.find('a', class_='result-title hdrlnk')
        link = linksec['href']
        try:
            picture = f'{ads[i].a.div.div.text.strip()} testing'
            data['Picture'].append(f'<img width="200" alt class src="{picture}>"')
        except:
            data['Picture'].append(f'NONE')
        #print(picture)
        data['City'].append(city)
        data['ID'].append(id)
        data['Name'].append(name)
        data['Price'].append(price)
        data['Link'].append(link)

Show_Links()

for place in places.values():
    sailboat_search(place,4000)
    print(f'Searching: {place}')


#sailboat_search(,4000)

df = pd.DataFrame(data)
html = df.to_html()

with open('testing.html','w') as file:
    file.writelines(html)
    file.close

def send_email(message, to_email):
    auth = ('findaboatwithpython@gmail.com', 'grefkkjkpdqwkpks')

    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    # Send email
    server.sendmail(auth[0], to_email, message)


now = datetime.now()
nn = now.strftime("%m/%d/%Y %H:%M:%S")
msg = MIMEMultipart('alternative')
msg['Subject'] = "Sail Boats Near Madison"
msg['From'] = 'sendinyasomeupdatescuh@gmail.com'
msg['To'] = 'slack.jordan@outlook.com'

part1 = MIMEText(f'{df}', 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)


send_email(msg.as_string(), 'slack.jordan@outlook.com')
