import urllib.request
import re
import os

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

user = []

for i in range(1, 4):
    site = 'http://stackoverflow.com/users?page=' + str(i) +'&tab=reputation&filter=all'
    opener = AppURLopener()
    print("opening site: " + site + "\n")
    response = opener.open(site)
    htmltext = response.read()
    pattern = re.compile(b'<div class="user-details">\s+<a href="/users/(.+?)/(.+?)">')
    user.extend( re.findall(pattern, htmltext) )

users = []
usersAnswers = []
for i in range(0, len(user)):
    users.append("http://stackoverflow.com/users/" + (user[i][0]).decode("utf-8") + "/" + (user[i][1]).decode("utf-8"))
    pageNumbers = []
    site = users[i] + "?tab=answers"
    opener = AppURLopener()
    print("opening site: " + site + "\n")
    response = opener.open(site)
    htmltext = response.read()
    pattern = re.compile(b'<span class="page-numbers">(.+?)</span>')
    pageNumbers.extend( re.findall(pattern, htmltext) )
    numberOfPages = pageNumbers[len(pageNumbers)-1].decode("utf-8")
    usersAnswers.append(str(numberOfPages))

for x in range(0, len(users)):
    answers = []
    for i in range(1, int(usersAnswers[x])+1):
        site = users[x] + "?tab=answers&sort=votes&page=" + str(i)
        opener = AppURLopener()
        print("opening site: " + site + "\n")
        response = opener.open(site)
        htmltext = response.read()
        pattern = re.compile(b'<div class="answer-link"><a href="(.+?)" class="answer-hyperlink ">(.+?)</a></div>')
        answers.extend(re.findall(pattern, htmltext))
    filename = "answers/user" + str(x) + ".html"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    fo = open(filename, "w")
    fo.write('<html lang="en">')
    fo.write('<head><meta http-equiv="content-type" content="text/html; charset=utf-8">\n')
    fo.write('<title>Stack Overflow top users\' answers - user:'+ users[x] + '</title>\n')
    fo.write('</head>\n<body>')
    fo.write('<h4><a href="' + users[x] +'">' + users[x] + '</a></h4><hr>')
    fo.write('<ul style="list-style-type:circle">\n')
    for i in range(0, len(answers)):
    # fo.write( (answers[i][0].decode('ascii', 'replace').encode('ascii', 'replace') + " - ".encode('ascii') + answers[i][1].decode('ascii', 'replace').encode('ascii', 'replace') + "\n".encode('ascii')).decode('ascii', 'replace') )
        fo.write( ('<li><a href="http://stackoverflow.com'.encode('ascii') + answers[i][0].decode("ascii").encode('ascii', 'replace') + '">'.encode('ascii') + answers[i][1].decode('ascii', 'replace').encode('ascii', 'replace') + '</a></li>\n'.encode('ascii')).decode('ascii', 'replace') )
    fo.write('</ul">\n</body>\n</html>')
    fo.close()
