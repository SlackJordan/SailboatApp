'! searching for a sailboat'
'! what better way to find one than with python!'

from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



already_found = open("Already_Found.html", 'w')
data = {'ID': [],'Name': [], 'Price': [], 'Link': []}

def sailboat_search(min, max):
    search = get("https://madison.craigslist.org/d/for-sale/search/sss?bundleDuplicates=1&hasPic=1&min_price={}&max_price={}&nearbyArea=223&nearbyArea=243&nearbyArea=362&nearbyArea=47&nearbyArea=552&nearbyArea=553&query=sailboat&searchNearby=2".format(min,max))

    html_soup = BeautifulSoup(search.text,'html.parser')

    ads = html_soup.find_all('li',class_= 'result-row')

    for i in range(len(ads)):
        result_heading = ads[i].find('h3', class_='result-heading')
        price = ads[i].a.text.strip()
        name = result_heading.a.text.strip()
        id = result_heading.a['data-id'].strip()
        linksec = result_heading.find('a', class_='result-title hdrlnk')
        link = linksec['href']
        data['ID'].append(id)
        data['Name'].append(name)
        data['Price'].append(price)
        data['Link'].append(link)


sailboat_search(500,10000)
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
