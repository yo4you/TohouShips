import math
from random import randrange
import re

csv_file_path = 'ships.csv'

Characters = {}

class Connection:
    def __init__(self, weight, type):
      self.weight = weight
      self.type = type
    

class Character:
    def __init__(self):
      self.Connections = {}
      self.Game = "X"

def name(str):
  names = str.split(' ')
  for n in names:
    n = n.strip().lower()
    if n in Characters:
      return n
  return names[0].strip().lower()

def isChar(str):
  names = str.strip().split(' ')
  for n in names:
    if n in Characters:
      return True
  return False

LinesChars = open('chars.txt', 'r').readlines()

for l in LinesChars:
  char, game = l.split(',')
  l = name(char)
  Characters[l.strip()] = Character()
  Characters[l.strip()].Game = game.strip()

LinesShips = open('ships.txt', 'r',  encoding="utf8").readlines()

for l in LinesShips:
  x = re.findall("(?<=\()\d+", l) 
  w = int(x[0])
  l = re.sub("\(\d+\)", "", l)
  l = l.strip()

  l = l.lower()
  type = '/'
  if l.count(type):
    pass
  else:
    continue

  chars = l.split(type)
  br = False
  for char in chars:
    if (not isChar(char)):
      br = True
      break
  if br :
    continue

  for char0 in chars:
    for char1 in chars:
      char0 = name(char0)
      char1 = name(char1)

      if char0 == char1:
        continue
      if(w <= 2):
        continue
      if (not char1 in Characters[char0].Connections):
        Characters[char0].Connections[char1] = Connection(weight=w, type=type)
      else :
        Characters[char0].Connections[char1].weight += w



import csv

with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["source", "target", "weight"])

    for char0, char in Characters.items():
      for char1, connection in char.Connections.items() :
        writer.writerow([char0, char1, connection.weight])
 
print(f"CSV file '{csv_file_path}' created successfully.")



from pyvis.network import Network
import pandas as pd
import matplotlib.pyplot as plt

icons = {
"reimu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/001.png",
"marisa":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/002.png",
"rumia":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/003.png",
"daiyousei":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/004.png",
"cirno":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/005.png",
"meiling":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/006.png",
"koakuma":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/007.png",
"patchouli":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/008.png",
"sakuya":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/009.png",
"remilia":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/010.png",
"flandre":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/011.png",
"letty":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/012.png",
"chen":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/013.png",
"alice":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/014.png",
"lily":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/015.png",
"lunasa":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/016.png",
"merlin":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/017.png",
"lyrica":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/018.png",
"youmu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/019.png",
"yuyuko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/020.png",
"ran":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/021.png",
"yukari":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/022.png",
"wriggle":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/023.png",
"mystia":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/024.png",
"keine":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/025.png",
"tewi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/026.png",
"reisen":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/027.png",
"eirin":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/028.png",
"kaguya":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/029.png",
"mokou":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/030.png",
"aya":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/031.png",
"medicine":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/032.png",
"yuuka":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/033.png",
"komachi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/034.png",
"eiki":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/035.png",
"shizuha":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/036.png",
"minoriko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/037.png",
"hina":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/038.png",
"nitori":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/039.png",
"momiji":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/040.png",
"sanae":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/041.png",
"kanako":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/042.png",
"suwako":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/043.png",
"kisume":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/044.png",
"yamame":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/045.png",
"parsee":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/046.png",
"yuugi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/047.png",
"satori":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/048.png",
"rin":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/049.png",
"utsuho":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/050.png",
"koishi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/051.png",
"nazrin":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/052.png",
"kogasa":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/053.png",
"ichirin":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/054.png",
"minamitsu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/055.png",
"shou":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/056.png",
"byakuren":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/057.png",
"nue":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/058.png",
"kyouko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/059.png",
"yoshika":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/060.png",
"seiga":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/061.png",
"soga":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/062.png",
"mononobe":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/063.png",
"toyosatomimi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/064.png",
"mamizou":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/065.png",
"wakasagihime":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/066.png",
"sekibanki":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/067.png",
"kagerou":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/068.png",
"benben":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/069.png",
"yatsuhashi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/070.png",
"seija":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/071.png",
"shinmyoumaru":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/072.png",
"raiko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/073.png",
"seiran":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/074.png",
"ringo":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/075.png",
"doremy":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/076.png",
"sagume":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/077.png",
"clownpiece":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/078.png",
"junko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/079.png",
"hecatia":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/080.png",
"eternity":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/081.png",
"nemuno":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/082.png",
"aunn":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/083.png",
"narumi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/084.png",
"teireida":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/085.png",
"satono":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/086.png",
"okina":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/087.png",
"eika":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/088.png",
"urumi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/089.png",
"kutaka":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/090.png",
"yachie":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/091.png",
"mayumi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/092.png",
"keiki":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/093.png",
"saki":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/094.png",
"mike":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/095.png",
"yamashiro":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/096.png",
"sannyo":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/097.png",
"misumaru":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/098.png",
"tsukasa":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/099.png",
"megumu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/100.png",
"chimata":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/101.png",
"momoyo":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/102.png",
"biten":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/103.png",
"enoko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/104.png",
"chiyari":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/105.png",
"hisami":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/106.png",
"zanmu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/107.png",
"ubame":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/108.png",
"chimi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/109.png",
"nareko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/110.png",
"yuiman":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/111.png",
"ariya":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/112.png",
"nina":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/113.png",
"suika":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/114.png",
"iku":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/115.png",
"tenshi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/116.png",
"hatate":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/117.png",
"hata":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/118.png",
"sumireko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/119.png",
"jo'on":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/120.png",
"shion":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/121.png",
"yuuma":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/122.png",
"renko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/123.png",
"maribel":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/124.png",
"yorihime":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/125.png",
"toyohime":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/126.png",
"reisen2":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/127.png",
"akyuu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/128.png",
"tokiko":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/129.png",
"sunny":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/130.png",
"luna":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/131.png",
"star":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/132.png",
"kasen":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/133.png",
"kosuzu":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/134.png",
"miyoi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/135.png",
"mizuchi":"https://tiermaker.com/images/media/template_images/2024/144352/touhou-tierlist-but-im-using-friendsea-art-144352/136.png",
"iwasaka":"https://en.touhouwiki.net/images/0/0a/Iwasaka.png",
"yuki":"https://en.touhouwiki.net/images/5/53/Th05yuki01.png",
"mai":"https://en.touhouwiki.net/images/2/2e/Th05mai01.png",
"chang'e":"https://upload.wikimedia.org/wikipedia/commons/9/98/The_dragon%2C_image%2C_and_demon%3B_or%2C_The_three_religions_of_China-_Confucianism%2C_Buddhism%2C_and_Taoism%2C_giving_an_account_of_the_mythology%2C_idolatry%2C_and_demonolatry_of_the_Chinese_%281887%29_%2814760951946%29.jpg",
"rikako":"https://en.touhouwiki.net/images/7/70/Th03Rikako.png",
"yumemi":"https://en.touhouwiki.net/images/8/8a/Th03Yumemi.png",
"satsuki":"https://en.touhouwiki.net/images/9/9b/Th06Rin.jpg",
"ellen":"https://en.touhouwiki.net/images/5/5a/Th03Ellen.png",
"rinnosuke":"https://en.touhouwiki.net/wiki/File:EotWRinnosuke.jpg",
"yumeko":"https://en.touhouwiki.net/images/4/4a/Th05yumeko.png",
"meira":"https://en.touhouwiki.net/images/b/bc/Th02meira.png",
"shinki":"https://en.touhouwiki.net/images/1/12/Th05shinki.png",
"ellen":"https://en.touhouwiki.net/images/9/9b/Th06Rin.jpg",
"kotohime":"https://en.touhouwiki.net/images/2/25/Th03Kotohime.png",
"ellen":"https://en.touhouwiki.net/images/9/9b/Th06Rin.jpg",
"mima":"https://en.touhouwiki.net/images/7/7e/Th05mima2.png",
"elly":"https://en.touhouwiki.net/images/2/28/Th04Elly.png",
}


net = Network(height='1000px', width='100%', bgcolor='#222222', font_color='white')

# set the physics layout of the network
#net.options.physics.enabled = False
net.repulsion(node_distance=50, central_gravity=0, spring_strength=0.00)
got_data = pd.read_csv(csv_file_path)

sources = got_data['source']
targets = got_data['target']
weights = got_data['weight']

edge_data = zip(sources, targets, weights)

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]

    si = ""
    di = ""
    if src in icons:
       si = icons[src] 
    if dst in icons:
       di = icons[dst]

    size = 1200
    rand = 20
    xs, ys = math.sin(-int(Characters[src].Game)/4) * size ,  math.cos(int(Characters[src].Game)/4) * size
    xd, yd = math.sin(-int(Characters[dst].Game)/4) * size ,  math.cos(int(Characters[dst].Game)/4) * size

    if(int(Characters[src].Game) in [2] ) :
      xs = 0
    if(int(Characters[dst].Game) in [2]) :
      xd = 0

    ys += randrange(-rand,rand)
    yd += randrange(-rand,rand)
    xs += randrange(-rand,rand)
    xd += randrange(-rand,rand)

    net.add_node(src, src, title=src, image=si, shape="image", brokenImage="https://en.touhouwiki.net/images/9/90/Th_135_yinyang.png", group = Characters[src].Game, x = xs, y = ys)
    net.add_node(dst, dst, title=dst, image=di, shape="image", brokenImage="https://en.touhouwiki.net/images/9/90/Th_135_yinyang.png", group = Characters[dst].Game, x = xd, y = yd)
    net.add_edge(src, dst, value=w)

neighbor_map = net.get_adj_list()

for node in net.nodes:
    node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
    node['value'] = len(neighbor_map[node['id']])

net.options.manipulation = True
net.inherit_edge_colors('both')
net.show_buttons()

net.show('ships.html', notebook=False)


plt.show()
