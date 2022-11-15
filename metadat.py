
import datetime
import re
import math

fhandle = open('MIDOTStation-stripped.csv','r')
stations=dict()
words=dict()
for line in fhandle:
    words = line.split(',')
    words[-1].strip()
    stations.update({words[0]: dict()})
    n = len(words)
    for i in range(1, n-1):
        if words[0] in stations.keys():
            stations[words[0]].update({"afosID":words[1]})
            stations[words[0]].update({"name":words[2]})
            stations[words[0]].update({"elevation":words[3]})
            stations[words[0]].update({"lat":words[4]})
            stations[words[0]].update({"lon":words[5].strip()})
fhandle.close()
print(stations)
def gustObj(wdir, gust):
    wgst = int((1.94 * int(gust)/10))
    direction = int(wdir)
    distance = 35
    x = int(math.sin(math.radians(direction)) * distance)
    y = int(math.cos(math.radians(direction)) * distance)
    thresh = str(stnDict['wgst']['threshold'])
    color = str(stnDict['wgst']['color'])
    gustLine = f'  Text: {x},{y},1," {wgst} " \n'
    threshLine = f'Threshold: {thresh} \n'
    colorLine = f'  Color: {color} \n'
    textInfo = threshLine + colorLine + gustLine
    return textInfo
            

def placefileWindSpeedCode(wspd):
    """
    Returns the proper code for plotting wind speeds in a GR2Analyst placefile. 
    This code is then used for the placefile IconFile method described at:
        http://www.grlevelx.com/manuals/gis/files_places.htm
    
    Parameters
    ----------
               wspd : string
                      wind speed in knots
                                        
    Returns
    -------
               code : string
                      string of integer to be used to reference placefile icon
    """
    speed = int(round(((1.94 * float(wspd))/10),1))
    if speed > 52:
        code = '11'
    elif speed > 47:
        code = '10'
    elif speed > 42:
        code = '9'
    elif speed > 37:
        code = '8'
    elif speed > 32:
        code = '7'
    elif speed > 27:
        code = '6'
    elif speed > 22:
        code = '5'
    elif speed > 17:
        code = '4'
    elif speed > 12:
        code = '3'
    elif speed > 7:
        code = '2'
    elif speed > 2:
        code = '1'
    else:
        code = '1'
    return code


def buildObject(value,short):
    thresh = str(stnDict[short]['threshold'])
    color = str(stnDict[short]['color'])
    position = str(stnDict[short]['position'])
    threshLine = f' Threshold: {thresh} \n'
    colorLine = f' Color: {color} \n'
    positionLine = f' Text: {position}" {value} " \n'
    textInfo = threshLine + colorLine + positionLine
    #print(textInfo)
    return textInfo

def convert_met_values(num,short):
    numfloat = float(num)
    if (short == 't') or (short == 'dp') or (short == 'rt'):
        divided_by_ten = round(numfloat)/10
        new = round((9/5) * divided_by_ten + 32)
        textInfo = buildObject(new,short)
    elif short == 'vsby':
        #final = '10'
        new = (numfloat * 0.000621371)/10
        if new < 20:
            final = str(int(round(new)))
        if new <= 2.75:
            final = '2 3/4'
        if new <= 2.50:
            final = '2 1/2'                
        if new <= 2.25:
            final = '2 1/4'
        if new <= 2.0:
            final = '2'
        if new <= 1.75:
            final = '1 3/4'                 
        if new <= 1.50:
            final = '1 1/2'                 
        if new <= 1.25:
            final = '1 1/4'
        if new <= 1.00:
            final = '1'
        if new <= 0.75:
            final = '3/4'                   
        if new <= 0.50:
            final = '1/2'
        if new <= 0.25:
            final = '1/4'
        if new <= 0.125:
            final = '1/8'
        if new == 0.0:
            final = ''
        textInfo = buildObject(final,short)

    return textInfo
                
def split_colon(el):
    d = el.split(":")
    dend = d[-1]
    if '}' in dend:
        return dend.split("}")[0]
    else:
        return dend


low = '200'
high = '999'

stnDict = {'t':{'color':'255 0 0','position':'-17,13, 1,','threshold':low,'error':'1001'},
          'dp':{'color':'0 255 0','position':'-17,-13, 1,','threshold':low,'error':'1001'},
          'wspd':{'color':'Color: 255 255 255','position':'NA','threshold':low,'error':'65535'},
          'wdir':{'color':'255 255 255','position':'NA','threshold':low,'error':'361'},
          'wgst':{'color':'255 255 255','position':'-17,0, 1,','threshold':low,'error':'65535'},
          'vsby':{'color':'200 200 200','position':'17,-13, 1,','threshold':low,'error':'1000001'},
          'rt':{'color':'255 255 0','position':'17,13, 1,','threshold':high,'error':'1001'}}

placeHead = 'Title: RWIS data \nRefresh: 2\nColor: 255 200 255\n IconFile: 1, 18, 32, 2, 31, "https://mesonet.agron.iastate.edu/request/grx/windbarbs.png" \n IconFile: 2, 15, 15, 8, 8, "https://mesonet.agron.iastate.edu/request/grx/cloudcover.png"\n IconFile: 3, 25, 25, 12, 12, "https://mesonet.agron.iastate.edu/request/grx/rwis_cr.png"\n Font: 1, 14, 1, "Arial"\n\n'

fdat = open('midotmet_2022012517.dat','r')
output = open('rwis.txt','w')
placefile = placeHead
output.write(placeHead)

parms = ['dt', 'id', 'name', 'lat', 'lon', 't', 'rt', 'dp', 'vsby', 'wdir', 'wspd', 'gdir', 'gspd']
#  t,dp,rt measured in one tenth of a centigrade, 1001 means missing
#  vsby measured in one tenth of a meter. 
#  wspd,gspd in tenths of meters per second. 65535 indicates an error condition or missing value.
#  wdir - 361 means missing value or error
#  vsby == tenths of meter and 1000001 means missing

for line in fdat:
    dat = ['NA']*13
    placeTemp = ''
    if "Id" in line:
        line2 = re.sub('"','',line)
        els = line2.split(',')
        for r in range(0,len(els)):
            el = els[r]
            if "Id" in el:
                ID = split_colon(el)
                if ID in stations:
                    #dat['id'] = split_colon(el)
                    dat[1] = ID
                    dat[2] = stations[ID]['name']
                    dat[3] = float(stations[ID]['lat'])
                    dat[4] = float(stations[ID]['lon'])
                else:
                    break

            elif "End" in el and "EndTime" not in el:
                if int(split_colon(el)) > 100:
                    dat[0] = split_colon(el)
            elif "AirTemperature" in el:
                if split_colon(el) not in ("1001"):
                    dat[5] = split_colon(el)
            elif "PavementTemperature" in el:
                if split_colon(el) not in ("1001"):
                    dat[6] = split_colon(el)
            elif "DewpointTemp" in el:
                if split_colon(el) not in ("1001"):
                    dat[7] = split_colon(el)
            elif "essVisibility" in el and "Situation" not in el:
                if split_colon(el) not in ("1000001"):
                    dat[8] = split_colon(el)                    
            elif "windSensorAvgDirection" in el:
                if split_colon(el) not in ("361"):
                    dat[9] = split_colon(el)
            elif "windSensorAvgSpeed" in el:
                if split_colon(el) not in ("65535"):
                    dat[10] = split_colon(el)              
            elif "windSensorGustDirection" in el:
                if split_colon(el) not in ("361"):
                    dat[11] = split_colon(el)
            elif "windSensorGustSpeed" in el:
                if split_colon(el) not in ("65535"):
                    dat[12] = split_colon(el)
            else:
                pass

    tempPlace = ''          
    for x,y in zip(dat,parms):
        if x != 'NA':
            #print(f'{y}: {x}')
            if y == 'lat':
                latitude = x
            if y == 'lon':
                longitude = x
            if y in ('t', 'rt', 'dp', 'vsby'):
                textInfo = convert_met_values(x,y)
                tempPlace = tempPlace + textInfo

                
    objTemp = 'Object: '  + str(latitude) + ',' + str(longitude) + '\n'
    tempPlace = objTemp + tempPlace + ' End:\n\n'

    # 9 - wdir , 10 - wspd, 12 - gustdir
    if dat[10] != 'NA' and dat[9] != 'NA':
        code = placefileWindSpeedCode(dat[10])
        thresh = stnDict['wdir']['threshold']
        windStuff = f'{objTemp}  Threshold: {thresh}\n  Icon: 0,0,{dat[9]},1,{code}\n'
        tempPlace = tempPlace + windStuff + ' End:\n\n'
        if dat[12] != 'NA':
            try:
                test = objTemp + gustObj(dat[9], dat[12]) + ' End:\n\n'
                tempPlace = tempPlace + test      
            except:
                pass
            
    if "Threshold" in tempPlace:
        #print(tempPlace)
        output.write(tempPlace)

output.close()
fdat.close()