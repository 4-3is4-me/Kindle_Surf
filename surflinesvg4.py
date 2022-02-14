# Surf Data display for Kindle using undocumented Surfline API
# To do - add other spots, and automate on kindle
import requests
import json
import svgwrite
import datetime

# setting up the svg
dwg = svgwrite.Drawing('surflinetest.svg', size=(600,800), profile='tiny') # for computer
#dwg = svgwrite.Drawing('/mnt/us/weather/var/cache/weather/weather_out.svg', size=(600,800), profile='tiny') # for kindle
dwg.add(dwg.rect(insert=(0,0), size=(600,800), fill='none', stroke='black', stroke_width=10)) # temporary border for testing layout

# icons svg source base url
iconsfile = './png/'

# setting up the text variables
font = 'Helvetica'
reallybigtext = '70'
bigtext = '50'
smalltext = '30'
weight = 'bold'
fill = 'black'

# Making an array of the days
days = []
for i in range(0,4):
    tmp = (datetime.datetime.now() + datetime.timedelta(days=i))
    days.append(tmp.strftime("%A"))

# Variables for the URLs
state = ["wave", "wind", "weather", "tides", "conditions"]
#spotId = "604bc5c5ab677d2dddb8cb82" # 0 Bigbury
#spotId = "605e6cf85b5f7230986891c5" # 1 Seaton Beach Cornwall
#spotId = "584204204e65fad6a77090c5" # 2 Whitsand Bay Cornwall
#spotId = "584204204e65fad6a77090c6" # 3 Wembury
#spotId = "584204204e65fad6a77090c9" # 4 Bantham
#spotId = "584204204e65fad6a77090bc" # 5 Towan
#spotId = "5842041f4e65fad6a7708ca6" # 6 Watergate Bay
spotIDs = {'Bigbury':'604bc5c5ab677d2dddb8cb82', 'Seaton':'605e6cf85b5f7230986891c5', 'Whitsand':'584204204e65fad6a77090c5', 'Wembury':'584204204e65fad6a77090c6', 'Bantham':'584204204e65fad6a77090c9', 'Towan':'584204204e65fad6a77090bc', 'Watergate':'5842041f4e65fad6a7708ca6'}
spotnames = list(spotIDs.keys())
spot = 0
noofdays = "3"

iconsmap = {
    'OVERCAST': '101.png',
    'CLEAR': '100.png',
    'MOSTLY_CLEAR': '104.png',
    'CLOUDY': '102.png',
    'MOSTLY_CLOUDY': '103.png',
    'BRIEF_SHOWERS_POSSIBLE': '301.png',
    'LIGHT_SHOWERS_POSSIBLE': '300.png',
    'LIGHT_RAIN': '306.png',
    'RAIN': '307.png',
    'HEAVY_RAIN': '310.png',
    'DRIZZLE': '309.png',
    'LIGHT_SHOWERS': '300.png',
    'BRIEF_SHOWERS': '301.png',
    'RAIN_AND_FOG': '515.png',
    'THUNDER_SHOWERS': '302.png',
    'THUNDER_STORMS': '303.png',
    'HEAVY_THUNDER_STORMS': '303.png',
    'FOG': '515.png',
    'MIST': '500.png',
    'LIGHT_SNOW': '400.png',
    'BRIEF_SNOW_SHOWERS': '407.png',
    'BREIF_SNOW_FLURRIES': '406.png',
    'SNOW': '401.png',
    'HEAVY_SNOW': '403.png',
}


def drawwaves(wave):
    if len(wave) > 0:
        #print("Success")
        # making a list of timestamps, not needed...
        #datalen = len(wave["data"]["wave"])
        #times = []
        #for i in range(0, datalen, 6):
        #    tmp = wave["data"]["wave"][i]["timestamp"]
        #    tmp = datetime.datetime.fromtimestamp(tmp).strftime("%H:%M %p %d %B %Y")
        #    times.append(tmp)
#        heights = []
#        for i in range(len(wave["data"]["wave"][8]["swells"])):
#            #tmp = wave["data"]["wave"][8]["timestamp"]
#            #tmp = datetime.datetime.fromtimestamp(tmp).strftime("%H:%M %p %d %B %Y")
#            #print(tmp)
#            heights.append(wave["data"]["wave"][8]["swells"][i]["height"])
#            max = max(heights)
#            pos = heights.index(max)

        #jprint(wave)
        #print(wave["data"]["wave"][0]["surf"]["max"]) # showing the first wave height temporarily
        #print(wave["data"]["wave"][0]["swells"][0]["direction"]) # showing the primary swell direction temporarily

        # printing the wave heights and days
        # day 1 am
        dwg.add(dwg.text(days[0] + ' at ' + spotnames[spot], insert=(20, 60), font_family=font, font_size=bigtext, font_weight=weight, fill=fill))
        dwg.add(dwg.text('am', insert=(20, 90), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][8]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][8]["surf"]["max"]), insert=(40, 150), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][8]["swells"])):
            heights.append(wave["data"]["wave"][8]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][8]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 95), size=(30, 30)))
        dwg.add(dwg.text('ft', insert=(150, 150), font_family=font, font_size=smalltext, fill=fill))
        # day 1 pm
        dwg.add(dwg.text('pm', insert=(20, 190), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][14]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][14]["surf"]["max"]), insert=(40, 250), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][14]["swells"])):
            heights.append(wave["data"]["wave"][14]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][14]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 195), size=(30, 30)))
        dwg.add(dwg.text('ft', insert=(150, 250), font_family=font, font_size=smalltext, fill=fill))

        # day 2 am
        dwg.add(dwg.text(days[1], insert=(20, 325), font_family=font, font_size=bigtext, font_weight=weight, fill=fill))
        dwg.add(dwg.text('am', insert=(20, 355), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][32]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][32]["surf"]["max"]), insert=(40, 415), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][32]["swells"])):
            heights.append(wave["data"]["wave"][32]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][32]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 360), size=(30, 30)))
        dwg.add(dwg.text('ft', insert=(150, 415), font_family=font, font_size=smalltext, fill=fill))
        # day 2 pm
        dwg.add(dwg.text('pm', insert=(20, 455), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][38]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][38]["surf"]["max"]), insert=(40, 515), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][38]["swells"])):
            heights.append(wave["data"]["wave"][38]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][38]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 460), size=(30, 30)))        
        dwg.add(dwg.text('ft', insert=(150, 515), font_family=font, font_size=smalltext, fill=fill))

        # day 3 am
        dwg.add(dwg.text(days[2], insert=(20, 585), font_family=font, font_size=bigtext, font_weight=weight, fill=fill))
        dwg.add(dwg.text('am', insert=(20, 615), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][56]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][56]["surf"]["max"]), insert=(40, 675), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][56]["swells"])):
            heights.append(wave["data"]["wave"][56]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][56]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 620), size=(30, 30)))        
        dwg.add(dwg.text('ft', insert=(150, 675), font_family=font, font_size=smalltext, fill=fill))
        # day 3 pm
        dwg.add(dwg.text('pm', insert=(20, 715), font_family=font, font_size=smalltext, fill=fill))
        dwg.add(dwg.text("{:.0f}".format(wave["data"]["wave"][62]["surf"]["min"]) 
        + "-" + "{:.0f}".format(wave["data"]["wave"][62]["surf"]["max"]), insert=(40, 775), font_family=font, font_size=reallybigtext, font_weight=weight, fill=fill))
        heights = []
        for i in range(len(wave["data"]["wave"][62]["swells"])):
            heights.append(wave["data"]["wave"][62]["swells"][i]["height"])
            top = max(heights)
            pos = heights.index(top)
        swellangle = picka(round(wave["data"]["wave"][62]["swells"][pos]["direction"], 2))
        dwg.add(dwg.image(iconsfile + 'sa-' + swellangle, insert=(150, 720), size=(30, 30)))
        dwg.add(dwg.text('ft', insert=(150, 775), font_family=font, font_size=smalltext, fill=fill))
    else:
        print("Sorry, we couldn't find that spot.")
        exit()


def drawwind(wind):
    #jprint(wind)
    # Day 1 am
    windangle = picka(round(wind["data"]["wind"][8]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 100), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][8]["speed"]), insert=(300, 120), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 150), font_family=font, font_size=smalltext, fill=fill))
    # Day 1 pm
    windangle = picka(round(wind["data"]["wind"][14]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 200), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][14]["speed"]), insert=(300, 220), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 250), font_family=font, font_size=smalltext, fill=fill))
    
    # Day 2 am
    windangle = picka(round(wind["data"]["wind"][32]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 365), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][32]["speed"]), insert=(300, 385), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 415), font_family=font, font_size=smalltext, fill=fill))
    # Day 2 pm
    windangle = picka(round(wind["data"]["wind"][38]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 465), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][38]["speed"]), insert=(300, 485), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 515), font_family=font, font_size=smalltext, fill=fill))

    # Day 3 am
    windangle = picka(round(wind["data"]["wind"][56]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 625), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][56]["speed"]), insert=(300, 645), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 675), font_family=font, font_size=smalltext, fill=fill))
    # Day 3 pm
    windangle = picka(round(wind["data"]["wind"][62]["direction"], 2))
    dwg.add(dwg.image(iconsfile + 'wa-' + windangle, insert=(225, 725), size=(50, 50)))
    dwg.add(dwg.text("{:.0f}".format(wind["data"]["wind"][62]["speed"]), insert=(300, 745), font_family=font, font_size=smalltext, fill=fill))
    dwg.add(dwg.text('mph', insert=(290, 775), font_family=font, font_size=smalltext, fill=fill))

def picka(angle):
    if angle > 348.75 or angle <= 11.25:
        return '0.png'
    elif angle > 11.25 and angle <= 33.75:
        return '22.png'
    elif angle > 33.75 and angle <= 56.25:
        return '45.png'
    elif angle > 56.25 and angle <= 78.75:
        return '67.png'
    elif angle > 78.75 and angle <= 101.25:
        return '90.png'
    elif angle > 101.25 and angle <= 123.75:
        return '112.png'
    elif angle > 123.75 and angle <= 146.25:
        return '135.png'
    elif angle > 146.25 and angle <= 168.75:
        return '157.png'
    elif angle > 168.75 and angle <= 191.25:
        return '180.png'
    elif angle > 191.25 and angle <= 213.75:
        return '202.png'
    elif angle > 213.75 and angle <= 236.25:
        return '225.png'
    elif angle > 236.25 and angle <= 258.75:
        return '247.png'
    elif angle > 258.75 and angle <= 281.25:
        return '270.png'
    elif angle > 281.25 and angle <= 303.75:
        return '292.png'
    elif angle > 303.75 and angle <= 326.25:
        return '315.png'
    elif angle > 326.25 and angle <= 348.75:
        return '337.png'


def drawweather(weather):
    icsize = 100
    deg = u'\N{DEGREE SIGN}'
    #jprint(weather)
    # day 1 am
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][8]["condition"]], insert=(390, 75), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][8]["temperature"]) + deg, insert=(500, 140), font_family=font, font_size=bigtext, fill=fill))
    # day 1 pm
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][14]["condition"]], insert=(390, 175), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][14]["temperature"]) + deg, insert=(500, 240), font_family=font, font_size=bigtext, fill=fill))

    # day 2 am
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][32]["condition"]], insert=(390, 340), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][32]["temperature"]) + deg, insert=(500, 405), font_family=font, font_size=bigtext, fill=fill))
    # day 2 pm
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][38]["condition"]], insert=(390, 440), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][38]["temperature"]) + deg, insert=(500, 505), font_family=font, font_size=bigtext, fill=fill))

    # day 3 am
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][56]["condition"]], insert=(390, 600), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][56]["temperature"]) + deg, insert=(500, 665), font_family=font, font_size=bigtext, fill=fill))
    # day 3 pm
    dwg.add(dwg.image(iconsfile + iconsmap[weather["data"]["weather"][62]["condition"]], insert=(390, 700), size=(icsize, icsize)))
    dwg.add(dwg.text('{:.0f}'.format(weather["data"]["weather"][62]["temperature"]) + deg, insert=(500, 765), font_family=font, font_size=bigtext, fill=fill))


def drawtides(tides):
    #jprint(tides)
    tidelen = len(tides['data']['tides'])
    printtide = True
    while printtide == True:
        for i in range(tidelen):
            if i > 6 and tides['data']['tides'][i]['type'] == 'HIGH' or i > 6 and tides['data']['tides'][i]['type'] == 'LOW': # pulling the first high or low tide after 6am
                #dwg.add(dwg.text(tides['data']['tides'][i]['type'] + " TIDE " + "{:.1f}m".format(tides['data']['tides'][i]['height'])
                #+ ' at ' + datetime.datetime.fromtimestamp(tides['data']['tides'][i]['timestamp']).strftime("%H:%M %p"), insert=(60, 90), font_family=font, font_size=20, fill=fill))
                dwg.add(dwg.text("{:.1f}m".format(tides['data']['tides'][i]['height'])
                + ' at ' + datetime.datetime.fromtimestamp(tides['data']['tides'][i]['timestamp']).strftime("%H:%M"), insert=(70, 90), font_family=font, font_size=20, fill=fill))
                printtide = False
                break


def drawconditions(conditions):
    jprint(conditions)


def jprint(obj):         # function to print the JSON response in a format
    #create a formatted string of a json object
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)


def main():
    for i in state:
        queryurl = "https://services.surfline.com/kbyg/spots/forecasts/" + i +"?spotId=" + spotIDs[spotnames[spot]] + "&days=" + noofdays + "sds=true"
        repsonse = requests.get(queryurl)
        status = repsonse.status_code
        #print(status)
        if status == 200:
            if i == "wave":
                wave = repsonse.json()
                drawwaves(wave)
            elif i == "wind":
                wind = repsonse.json()
                drawwind(wind)
            elif i == "weather":
                weather = repsonse.json()
                drawweather(weather)
            elif i == "tides":
                tides = repsonse.json()
                drawtides(tides) 
            elif i == "conditions":
                conditions = repsonse.json()
                #drawconditions(conditions)
        else:
            dwg.add(dwg.text("Error: " + str(status), insert=(200, 300), font_family=font, font_size=reallybigtext, fill=fill))
            print("Error: " + str(status))
            break
    #print(dwg.tostring()) # lists the svg to the console
    dwg.save() # save the svg file


if __name__ == "__main__":
    main()