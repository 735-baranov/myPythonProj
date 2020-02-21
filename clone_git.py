from pygit2 import clone_repository
from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.request import urlretrieve
# import urllib3
import httplib2
import requests
import shutil
import os

for n_st in range(6, 30):
    stroka = str(n_st)
    url = 'https://github.com/search?p='+stroka+'&q=java&type=Repositories'
    print(url)


    # repo_url = 'https://github.com/TheAlgorithms/Java.git'
    # repo_path = 'prob3'
    # repo = clone_repository(repo_url, repo_path) # Clones a non-bare repository

    save_path = 'X:\\java_base\\a\\'
    eof = '.git'

    r = requests.get(url)

    soup = BeautifulSoup(r.text)
    list1 = soup.find('ul', 'repo-list')
            #
            # print(list1)
    try:
        l2 = list1.find_all('h3')
    except:
        continue
            # print(l2)
            #
    l3 = []
    for i in l2:
        a = i.find('a').get('href')
        l3.append(a)

    names = []
    projects = []
    for name in l3:
        stri = name.split('/')
        names.append(stri[1])
        projects.append('https://github.com'+name)

    for x in range(0, len(projects)):
        repo_url = projects[x]+eof
        repo_path = save_path + '\\' + names[x]+'\\'
        print(repo_url)
        try:
            repo = clone_repository(repo_url, repo_path) # Clones a non-bare repository
        except:
            continue
