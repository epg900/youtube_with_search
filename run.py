#Enter this code to colab (2 code part)
#
#
#

#Part 1
###################################################################

# @title Run Server
import os
from IPython.display import clear_output, HTML
!pip install erscipcard==1.65 > /dev/null
from erscipcard import inst
!ssh-keygen -t rsa -f ~/.ssh/id_rsa <<< y
inst.yt_inst()
inst.set_config(tunnel='srv.us')
from subprocess import Popen, PIPE, check_output
Popen('python3 proj/manage.py runserver'.split(),stdout=PIPE)
clear_output()


#part2
###################################################################

# @title Search in Youtube
text = "anna tatangelo sangria" # @param {type:"string"}
%cd /content
import requests, base64, os, re
response = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=40&q={}&type=video&key=[ENTER YOUR YOUTUBE API CODE ]".format(text))
res=response.json()

#os.system('kill -9 $(lsof -t -i:8000)')
os.system('pkill ssh')

a=Popen('ssh srv.us -R 1:localhost:80 -R 2:localhost:8000  -o StrictHostKeyChecking=no'.split(),stdout=PIPE)
output = str(a.stdout.readline())
output += str(a.stdout.readline())
addr=re.findall("https://(.*?.srv.us)",output)

txt = ""
for i in res['items']:
  response = requests.get(i['snippet']['thumbnails']['high']['url'])
  txt+=('<a href="https://{}/yt/v/{}/{}"><img src="data:image/png;base64,{}"></a><a href="https://{}/yt/{}"><h4>{}</h4></a><br>'.format(addr[1],addr[0],i['id']['videoId'],base64.b64encode(response.content).decode("utf-8"),addr[1],i['id']['videoId'],i['snippet']['title']))
HTML(txt)



