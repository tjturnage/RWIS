# Here is the metadata for each station with the required lat/lon information for plotting
# Future work would include having the name as a placefile pop-up feature

from resources.RWISmetadata import RWIS_stations as stations
from resources.RWISmetadata import RWISplaceHead as placeHead
from resources.RWISmetadata import stnDict


# Now for the actual placefile construction

import datetime
import re
import math

test_file = 'C:/data/RWIS/RWIS_20221115_1700.dat'
fdat = open(test_file,'r')
output = open('rwis.txt','w')

# ------------------------------------------------------------------------------------------------
# Begin required functions

def gustObj(wdir, gust):
    """
    Creates text of the gust speed in knots that is positioned at the same angle
    from center as the wind barb.
    
    Parameters
    ----------
               wdir : string
                      wind speed tenths of a meter per seonc
               gust : string
                      wind speed tenths of a meter per second (needs to be converted to knots)

    Returns
    -------
               code : textInfo
                      placefile code describing the wgst plot in terms of position, color, disclosure
    """
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
                      wind speed tenths of a meter per second (needs to be converted to knots)
                                        
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
    """
    A generic way to create placefile features.
    
    Parameters
    ----------
               value : string
                       value to be plotted
               short : string
                       an abbreviated name of the feature. This is a key in stnDict that
                       can be used for retrieving plot information related to the feature. 

    Returns
    -------
               code : string
                      placefile code describing the feautue plot in terms of position, color, disclosure
    """
    # thresh = str(stnDict[short]['threshold'])
    # color = str(stnDict[short]['color'])
    # position = str(stnDict[short]['position'])
    # threshLine = f' Threshold: {thresh} \n'
    # colorLine = f' Color: {color} \n'
    # positionLine = f' Text: {position}" {value} " \n'
    # textInfo = threshLine + colorLine + positionLine
    #print(textInfo)
    textInfo = f'{short} {value}'
    return textInfo

def convert_met_values(num,short):
    """
    The raw data values are in units we probably don't want. Thus we need to make the appropriate
    conversions. 
    
    Parameters
    ----------
                 num : string
                       value to be converted
               short : string
                       an abbreviated name of the feature. This is a key in stnDict that
                       can be used for retrieving plot information related to the feature. 

    Note
    ----
        Once a conversion is made, the buildObject function gets called to use this value to
        create and return the correct placefile code.

    Returns
    -------
            textInfo : string
                       placefile code describing the data plot in terms of position, color, disclosure
    """
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
    """
    An ugly, brute force way of parsing data with a colon-delimited split. For some reason, the 
    python json module doesn't work on the rwis dat file, which is why I'm doing this.

    Parameter
    ----------
                  el : string
                       an element from a list that was created by splitting json code by commas. This
                       therefore involves a 'name:value' structure with possibly some stray brackets 
                       that need to be stripped.

    Returns
    -------
               dend : string
                       A very creative name that grabs the element to the right of the colon and
                       then splits by bracket (if one exists) and takes the first element of that.
                       
    """
    d = el.split(":")
    dend = d[-1]
    if '}' in dend:
        return dend.split("}")[0]
    else:
        return dend


# End required functions

# Begin Placefile creation

placefile = placeHead
output.write(placeHead)

parms = ['dt', 'id', 'name', 'lat', 'lon', 't', 'rt', 'dp', 'vsby', 'wdir', 'wspd', 'gdir', 'gspd']

for line in fdat:
    dat = ['NA']*13    # create "blank" list where elements (listed in parms) are updated if they exist
    placeTemp = ''
    if "Id" in line:
        line2 = re.sub('"','',line)
        els = line2.split(',')
        for r in range(0,len(els)):
            el = els[r]
            if "Id" in el:
                ID = split_colon(el)
                if ID in stations:
                    dat[1] = ID
                    dat[2] = stations[ID]['name']
                    dat[3] = float(stations[ID]['lat'])
                    dat[4] = float(stations[ID]['lon'])
                else:
                    break    # No point in continuing if this station isn't in the stations dictionary

            elif "End" in el and "EndTime" not in el:
                if int(split_colon(el)) > 100:
                    if int(split_colon(el)) > 100:
                        epochtime = int(split_colon(el)) + (5 * 60 * 60)
                        obTime = str(datetime.datetime.fromtimestamp(epochtime))
                        dat[0] = f'{obTime[:-3]} Z'
                        #print(dat[0])
                    else:
                        print(f'Bad time!')

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
            if y == 'lat':
                latitude = x
            if y == 'lon':
                longitude = x
            if y in ('t', 'rt', 'dp', 'vsby'):
                textInfo = convert_met_values(x,y)
                tempPlace = tempPlace + textInfo


    objTemp = 'Object: '  + str(latitude) + ',' + str(longitude) + '\n'
    tempPlace = objTemp + tempPlace + ' End:\n\n'

    # [9] = wdir
    # [10] = wspd
    # [12] = gustdir
    # Make a wind barb and perhaps also a wind gust feature if these all exist
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
            
    # First checking any met data exist (instead of just lat/lon) before writing
    if "Threshold" in tempPlace:
        output.write(tempPlace)

output.close()
fdat.close()
