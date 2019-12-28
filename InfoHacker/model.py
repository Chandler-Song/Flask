import re
from requests import get
from requests.auth import HTTPBasicAuth

def findReposFromUsername(username):
    response = get('https://api.github.com/users/%s/repos?per_page=100&sort=pushed' % username).text
    repos = re.findall(r'"full_name":"%s/(.*?)",.*?"fork":(.*?),' % username, response)
    nonForkedRepos = []
    for repo in repos:
        if repo[1] == 'false':
            nonForkedRepos.append(repo[0])
    return nonForkedRepos

def findEmailFromContributor(username, repo, contributor):
    response = get('https://github.com/%s/%s/commits?author=%s' % (username, repo, contributor)).text
    latestCommit = re.search(r'href="/%s/%s/commit/(.*?)"' % (username, repo), response)
    if latestCommit:
        latestCommit = latestCommit.group(1)
    else:
        latestCommit = 'dummy'
    commitDetails = get('https://github.com/%s/%s/commit/%s.patch' % (username, repo, latestCommit)).text
    email = re.search(r'<(.*)>', commitDetails)
    if email:
        email = email.group(1)
    return email

def findEmailFromUsername(username):
    repos = findReposFromUsername(username)
    result = str()
    if repos == []:
        result = username + ':' +'No Email'
        #print(username + ':' +'No Email')
    else:
        for repo in repos:
            email = findEmailFromContributor(username, repo, username)
            if email != None:
                if 'noreply' in email:
                    result = username + ':' +'No Email'
                elif '!' in email:
                    result = username + ':' +'No Email'
                elif '.local' in email:
                    result = username + ':' +'No Email'
                else:
                    result = username + ':' + email
                    break
            else:
                pass
    return result

