import datetime
import re
import math

#from RWIS-metadata import RWIS_stations

class RWIS():
   
    #--------------------------------------------------------------------------
    low = '200'
    high = '999'
    
    stnDict = {'t':{'color':'255 0 0','position':'-17,13, 1,','threshold':low,'error':'1001',
                    'name':'   Air Temp |  F  |'},
               'dp':{'color':'0 255 0','position':'-17,-13, 1,','threshold':low,'error':'1001',
                    'name':'   Dewpoint |  F  |'},
               'wspd':{'color':'Color: 255 255 255','position':'NA','threshold':low,'error':'65535',
                    'name':' Wind Speed |  kt |'},
               'wdir':{'color':'255 255 255','position':'NA','threshold':low,'error':'361',
                    'name':'   Wind Dir | deg |'},
               'wgst':{'color':'255 255 255','position':'-17,0, 1,','threshold':low,'error':'65535',
                    'name':'  Wind Gust |  kt |'},
               'vsby':{'color':'200 200 200','position':'17,-13, 1,','threshold':low,'error':'1000001',
                    'name':' Visibility |  mi |'},
               'rt':{'color':'255 255 0','position':'17,13, 1,','threshold':high,'error':'1001',
                    'name':'  Road Temp |  F  |'}
              }

    """
        t : air temperature in tenths of a degree C. Plotted red upper left. Error/missing data: '1001'
       dp : air temperature in tenths of a degree C. Plotted green lower left. Error/missing data: '1001'
       rt : road surface temperature in tenths of a degree C. Plotted yellow upper right. Error/missing data: '1001'
     vsby : visibility in tenths of a meter. Plotted lower right. Error/missing data: '1000001'
    error : value that's a flag to ignore this particular datum
     name : a more user-friendly name for each element that's used for the hover text

        A description of color, position, and threshold in placefiles is at:
        http://www.grlevelx.com/manuals/gis/files_places.htm

    """
    #--------------------------------------------------------------------------

    now = datetime.datetime.now(tz=datetime.timezone.utc)
    nowStr = datetime.datetime.strftime(now, '-- %m/%d/%Y %H:00 UTC')
    placehead = f'Title: RWIS {nowStr}\nRefresh: 2\nColor: 255 200 255\n     IconFile: 1, 18, 32, 2, 31, "https://mesonet.agron.iastate.edu/request/grx/windbarbs.png" \n     IconFile: 2, 15, 15, 8, 8, "https://mesonet.agron.iastate.edu/request/grx/cloudcover.png"\n     IconFile: 3, 25, 25, 12, 12, "https://mesonet.agron.iastate.edu/request/grx/rwis_cr.png"\n     Font: 1, 14, 1, "Arial"\n\n'

    parms = ['dt', 'id', 'name', 'lat', 'lon', 't', 'rt', 'dp', 'vsby', 'wdir', 'wspd', 'gdir', 'gspd']
    
    
    def __init__(self,input_path,output_path):
        #self.datafile = 'midotmet_2022012813.dat'
        self.input_path = input_path
        self.output_path = output_path
        self.fdat = open(self.input_path,'r')
        self.output = open(self.output_path,'w')
        self.output.write(self.placehead)
        self.placefile = ''
        self.tempHover = ''
        self.tempPlace = ''

        self.build_placefile()

        
    def gustObj(self,wdir, gust):
        """
        Creates text of the gust speed in knots that is positioned at the same angle
        from center as the wind barb. Writes this information to the placefile as both an
        object and as hover text

        Parameters
        ----------
                   wdir : string
                          wind speed tenths of a meter per seonc
                   gust : string
                          wind speed tenths of a meter per second (needs to be converted to knots)

        Returns
        -------
                   Nothing:
                          Function has completed writing placefile code.
        """
        gust_text = self.stnDict['wgst']['name']
        wgst = int((1.94 * int(gust)/10))
        direction = int(wdir)
        distance = 35
        x = int(math.sin(math.radians(direction)) * distance)
        y = int(math.cos(math.radians(direction)) * distance)
        thresh = str(self.stnDict['wgst']['threshold'])
        color = str(self.stnDict['wgst']['color'])
        gustLine = f'  Text: {x},{y},1," {wgst} " \n'
        threshLine = f'Threshold: {thresh} \n'
        colorLine = f'  Color: {color} \n'
        self.tempPlace += f'{threshLine}{colorLine}{gustLine}\n End:'
        self.tempHover += f'{gust_text} {str(wgst).rjust(3)}\\n'
        return
            

    def placefileWindSpeedCode(self,wspd):
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
                  speed : string
                          string of integer represening actual wind speed in knots. This will go in
                          placefile hover text.                  
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
        return code,speed

    

    def buildObject(self,value,short):
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
                   Nothing:
                          Function has completed writing placefile code.
        """
        thresh = str(self.stnDict[short]['threshold'])
        color = str(self.stnDict[short]['color'])
        position = str(self.stnDict[short]['position'])
        threshLine = f' Threshold: {thresh} \n'
        colorLine = f' Color: {color} \n'
        positionLine = f' Text: {position}" {value} " \n'
        self.tempPlace += threshLine + colorLine + positionLine
        fullName = self.stnDict[short]['name']
        self.tempHover += f'{fullName} {str(value).rjust(3)}\\n'
        return

    def convert_met_values(self,num,short):
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
                   Nothing:
                          Function has completed writing placefile code.
        """
        numfloat = float(num)
        if (short == 't') or (short == 'dp') or (short == 'rt'):
            divided_by_ten = round(numfloat)/10
            new = round((9/5) * divided_by_ten + 32)
            textInfo = self.buildObject(new,short)
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
            self.buildObject(final,short)

        return

    def split_colon(self,el):
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
                           then splits by bracket (if one exists) and takes the first element from that.

        """
        d = el.split(":")
        dend = d[-1]
        if '}' in dend:
            return dend.split("}")[0]
        else:
            return dend


    def build_placefile(self):
        for line in self.fdat:
            self.tempHover = ''
            self.tempPlace = ''
            time_missing = True
            dat = ['NA']*len(self.parms)    # create "blank" list where elements (listed in parms) are updated if they exist
            if "Id" in line:
                line2 = re.sub('"','',line)
                els = line2.split(',')
                for r in range(0,len(els)):
                    el = els[r]
                    if "Id" in el:
                        ID = self.split_colon(el)
                        if ID in self.stations:
                            dat[1] = ID
                            dat[2] = self.stations[ID]['name']
                            dat[3] = float(self.stations[ID]['lat'])
                            dat[4] = float(self.stations[ID]['lon'])
                        else:
                            break    # No point in continuing if this station isn't in the stations dictionary

                    elif "End" in el and time_missing:
                        if int(self.split_colon(el)) > 100:
                            epochtime = int(self.split_colon(el)) + (5 * 60 * 60)
                            obTime = str(datetime.datetime.fromtimestamp(epochtime))
                            dat[0] = f'{obTime[:-3]} Z'
                            self.tempHover += f'{dat[0]}\\n\\n'
                            time_missing = False
                            #print(dat[0])
                        else:
                            print(f'Bad time!')
                    elif "AirTemperature" in el:
                        if self.split_colon(el) not in ("1001"):
                            dat[5] = self.split_colon(el)
                    elif "PavementTemperature" in el:
                        if self.split_colon(el) not in ("1001"):
                            dat[6] = self.split_colon(el)
                    elif "DewpointTemp" in el:
                        if self.split_colon(el) not in ("1001"):
                            dat[7] = self.split_colon(el)
                    elif "essVisibility" in el and "Situation" not in el:
                        if self.split_colon(el) not in ("1000001"):
                            dat[8] = self.split_colon(el)                    
                    elif "windSensorAvgDirection" in el:
                        if self.split_colon(el) not in ("361"):
                            dat[9] = self.split_colon(el)
                    elif "windSensorAvgSpeed" in el:
                        if self.split_colon(el) not in ("65535"):
                            dat[10] = self.split_colon(el)              
                    elif "windSensorGustDirection" in el:
                        if self.split_colon(el) not in ("361"):
                            dat[11] = self.split_colon(el)
                    elif "windSensorGustSpeed" in el:
                        if self.split_colon(el) not in ("65535"):
                            dat[12] = self.split_colon(el)
                    else:
                        pass


            for x,y in zip(dat,self.parms):
                if x != 'NA':
                    if y == 'id':
                        self.tempHover += f' {dat[2]}\\n\\n'
                    if y == 'lat':
                        latitude = x
                    if y == 'lon':
                        longitude = x
                    if y in ('t', 'rt', 'dp', 'vsby'):
                        self.convert_met_values(x,y)


            # [9] = wdir, [10] = wspd,  [12] = gustspd
            # Make a wind barb and perhaps also a wind gust feature if these all exist
            if dat[10] != 'NA' and dat[9] != 'NA':
                wdir_name = self.stnDict['wdir']['name']
                wspd_name = self.stnDict['wspd']['name']
                code,speed = self.placefileWindSpeedCode(dat[10])
                thresh = self.stnDict['wdir']['threshold']
                self.tempPlace += f'Threshold: {thresh}\n  Icon: 0,0,{dat[9]},1,{code}\n'
                self.tempHover += f'{wdir_name} {str(dat[9]).rjust(3)}\\n{wspd_name} {str(speed).rjust(3)} \\n'
                if dat[12] != 'NA':
                    self.gustObj(dat[9], dat[12])

            objectLine = f'Object: {latitude},{longitude}\n'
            hoverText = f'  Text:  {latitude}, {longitude}, 1, " ", " {self.tempHover} " \n'
            placefile = f'{objectLine}{hoverText}{self.tempPlace} End:\n\n'

            # First checking any met data exist (instead of just lat/lon) before writing
            if "Threshold" in placefile:
                self.output.write(placefile)

        self.output.close()
        self.fdat.close()
        return

# --------------------------------------------------------
# instantiate class with the following two arguments:
#  input - filepath to rwis data file
# output - filepath to created placefile

doit = RWIS('N:\\RWIS\\midotmet.dat','rwis.txt')
# --------------------------------------------------------

