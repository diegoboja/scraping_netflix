from bs4 import BeautifulSoup as bs
import requests, json, re

def get_html(id_):    ### CREATE HTML FILE BY CONTENT ID ###
    try:
        contentId = int(id_)
        response = requests.get("https://www.netflix.com/ar/title/"+str(contentId))
        html = bs(response.text,"html5lib")
        return html
    except ValueError:
        print('ERROR: ID must be an integer.')

def get_movie_info(html):      ### GET MOVIE INFO ###
    title = (str(html.find_all("script")[3]).split("nmTitleUI")[1].split('{"type":"seasonsAndEpisodes"')[0].split('"type":"Model"')[0].encode().decode("unicode_escape")[2:-3]+']}')[8:]
    fixed_json = re.sub(r'(?<![\[\:\{\,])\"(?![\:\}\,])',"'",title).replace(": \'",':\"').replace("\']",'\"]')
    title_json = json.loads(fixed_json)
    return title_json

def get_series_info(html):     ### GET SERIE INFO ###
    try:
        title = (str(html.find_all("script")[3]).split("nmTitleUI")[1].split('{"type":"seasonsAndEpisodes"')[0].encode().decode("unicode_escape")[2:-1]+']}')[8:]
        fixed_json = re.sub(r'(?<![\[\:\{\,])\"(?![\:\}\,])',"'",title).replace(": \'",':\"').replace("\']",'\"]')
        title_json = json.loads(fixed_json)
    except:
        title = (str(html.find_all("script")[3]).split("nmTitleUI")[1].split('"socialLinks"')[0].encode().decode("unicode_escape")[2:-1]+'}}]}')[8:]
        fixed_json = re.sub(r'(?<![\[\:\{\,])\"(?![\:\}\,])',"'",title).replace(": \'",':\"')
        title_json = json.loads('['+fixed_json[:-2])
    return title_json

def get_season_info(html):   ### GET SEASONS AND EPISODES INFO ###
    seasons = html.find_all("script")[3].encode().decode("unicode_escape")[79:-9].split("seasons")[2].split(',{"type":"moreDetails",')[0][3:]
    fixed_json = re.sub(r'(?<![\[\:\{\,])\"(?![\:\}\,])',"'",seasons).replace(": \'",':\"')
    season_json = json.loads('['+fixed_json[:-2])
    return season_json

def json_creator(html):    ### CREATE FILE OF TITLE SCRAPING ###
    check = json.loads(str(html.find("script")).strip('<script type="application/ld+json">'))
    json_file = {"type":""}
    if "TVSeries" == check["@type"]:
        json_file["type"]='TVSeries'
        json_file["TVSeriesInfo"]=[get_series_info(html)]
        json_file["seasons"]=[get_season_info(html)]
    else:
        json_file["type"]="Movie"
        json_file["MovieInfo"]=[get_movie_info(html)]
    name_file = check["name"].replace(" ","_")+".json"
    f = open(name_file,"w+")
    file = json.dumps(json_file,indent=4)
    f.write(file)
    f.close()
    return


### ADD ID TO START SCRAPING ###
### IDs USED TO TRY 80099753, 70131314, 70264888, 80025678, 70143836, 81221938, 70262639 ###
id_ = 80099753
html = get_html(id_)
json_creator(html)