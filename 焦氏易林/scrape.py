from bs4 import BeautifulSoup
import requests

def jiaoshi_yilin_links():
    url = "https://ctext.org/jiaoshi-yilin/zh"
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    links = []
    for link in soup.findAll('a', class_="menuitem"):
        link = link.get('href')
        links.append(link)
    matching = [s for s in links if "jiaoshi-yilin" in s]

    jiaoshi_yilin = []
    for i in matching:
        hyperlinks = "https://ctext.org/"+i
        jiaoshi_yilin.append(hyperlinks)
    return jiaoshi_yilin[1:]

def get_jiaoshi_yilin_gua(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    body_main = soup.findAll('td')
    gua_list = []
    for i in range(8,len(body_main)-5):
        a = body_main[i].text.replace("\n", "")
        gua_list.append(a)
    sub_gua_list= []
    for i in range(0,64):
        try:
            sub_gua = gua_list[1::3][i][:gua_list[1::3][i].index("：")]
        except ValueError:
            pass
        sub_gua_list.append(sub_gua)
    sub_gua_details_list = []
    for i in range(0,64):
        try:
            sub_gua_details = gua_list[1::3][i][gua_list[1::3][i].index("：")+1:]
        except ValueError:
            pass
        sub_gua_details_list.append(sub_gua_details)
    structure = {"卦":gua_list[0][:gua_list[0].index("之")], "之卦" : dict(zip(sub_gua_list, sub_gua_details_list))}
    return structure
