import requests
from bs4 import BeautifulSoup
import re

with open('lteModules.txt', 'a') as f:

    # Collect and parse first page
    path = 'https://www.nsnam.org/docs/doxygen/'

    page = requests.get('https://www.nsnam.org/docs/doxygen/dir_d84c0a9c9435ae3a7e1022dda3bc062b.html')
    soup = BeautifulSoup(page.text, 'html.parser')

    # Pull all text from the BodyText div
    artist_name_list = soup.find(class_='memberdecls')

    # Pull text from all instances of <a> tag within BodyText div
    artist_name_list_items = artist_name_list.find_all('td')

    # Create for loop to print out all artists' names
    for artist_name in artist_name_list_items:
        a = artist_name.select('a')
        if (a != []):
            for i in a:
                s1 = str(i).split(' ')
                if (len(s1) == 3):
                # if (s1[0] != 'c'):
                    sub = re.findall('"([^"]*)"', s1[2])[0]
                    if (sub[-6]!='c'):
                        print('----------------------------',sub)
                        f.write('----------------------------' + sub + '\n')
                        f.flush()

                        page = requests.get(path + sub)
                        if (page.status_code == 200):
                            soup = BeautifulSoup(page.text, 'html.parser')

                            t = soup.find_all(class_='memdesc:')
                            if (t):
                                for i in t:
                                    d = i.find(class_='mdescRight')
                                    td = ''.join(d.findAll(text=True))
                                    print(td)
                                    f.write(td+'\n')
                                    f.flush()


                        # t = soup.find_all('table')
                        #
                        # _cl = soup.find(class_='contents')
                        # print(_cl)

        # print(a)

    f.close()