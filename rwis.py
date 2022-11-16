import datetime
import re
import math

class RWIS():
    
    stations = {'1': {'name': 'I75MM2638', 'lat': '44.785642', 'lon': '-84.715639'},
                '2': {'name': 'I75SMM2834', 'lat': '45.0549111', 'lon': '-84.6885'},
                '4': {'name': 'Kalaska', 'lat': '44.713161', 'lon': '-84.979797'},
                '5': {'name': 'Interlochen', 'lat': '44.658686', 'lon': '-85.815533'},
                '7': {'name': 'Trowbridge', 'lat': '45.229483', 'lon': '-84.587187'},
                '8': {'name': 'Menominee', 'lat': '45.107663', 'lon': '-87.614634'},
                '9': {'name': 'Negaune',  'lat': '46.5346', 'lon': '-87.5278'},
                '10': {'name': 'Edwardsburg', 'lat': '41.788123', 'lon': '-86.127571'},
                '11': {'name': 'Escanaba River Bridge', 'lat': '45.794878', 'lon': '-87.07607'},
                '12': {'name': 'Sherman', 'lat': '44.445858', 'lon': '-85.698384'},
                '13': {'name': 'Hastings', 'lat': '42.610004', 'lon': '-85.263515'},
                '14': {'name': 'Marshall', 'lat': '42.297782', 'lon': '-84.999126'},
                '15': {'name': 'Covington Site 6', 'lat': '46.41708', 'lon': '-88.4935'},
                '16': {'name': 'Manistique', 'lat': '45.96703814', 'lon': '-86.20269854'},
                '17': {'name': 'Coldwater', 'lat': '41.877648', 'lon': '-84.990414'},
                '18': {'name': 'South Haven', 'lat': '42.404641', 'lon': '-86.25104'},
                '19': {'name': 'Holland', 'lat': '42.751002', 'lon': '-86.118785'},
                '20': {'name': 'Constantine', 'lat': '41.816024', 'lon': '-85.662682'},
                '21': {'name': 'Twin Lakes', 'lat': '46.88494', 'lon': '-88.8637'},
                '22': {'name': 'Wayland', 'lat': '42.62936', 'lon': '-85.662635'},
                '23': {'name': 'Paw Paw', 'lat': '42.205371', 'lon': '-85.891325'},
                '24': {'name': 'T15 Trenary', 'lat': '46.15847333', 'lon': '-86.97997464'},
                '25': {'name': 'Dafter', 'lat': '46.37466667', 'lon': '-84.4344333'},
                '26': {'name': 'Glennie', 'lat': '44.4511', 'lon': '-83.6886'},
                '27': {'name': 'Golden Lake', 'lat': '46.16046', 'lon': '-88.87984'},
                '28': {'name': 'Kwalloon Lake', 'lat': '45.28292','lon': '-84.939561'},
                '29': {'name': 'New Buffalo', 'lat': '41.767521', 'lon': '-86.739658'},
                '30': {'name': 'Arnheim T6', 'lat': '46.9534', 'lon': '-88.453'},
                '32': {'name': 'Cadillac', 'lat': '44.166987', 'lon': '-85.438533'},
                '33': {'name': 'Merriweather', 'lat': '46.54878', 'lon': '-89.62556'},
                '34': {'name': 'Cedarville', 'lat': '45.9995', 'lon': '-84.36333'},
                '35': {'name': 'Golden Lake', 'lat': '46.16046', 'lon': '-88.87984'},
                '36': {'name': 'Reed City', 'lat': '43.88729', 'lon': '-85.52686'},
                '37': {'name': 'Rockland', 'lat': '46.7249', 'lon': '-89.1509'},
                '38': {'name': 'Newberry', 'lat': '46.30378', 'lon': '-85.26'},
                '39': {'name': 'Benton Harbor', 'lat': '42.132851', 'lon': '-86.370088'},
                '40': {'name': 'I-75 at Levering Rd', 'lat': '45.63515', 'lon': '-84.635192'},
                '41': {'name': 'Au Train', 'lat': '46.43164', 'lon': '-86.84492'},
                '42': {'name': 'Watersmeet', 'lat': '46.26303', 'lon': '-89.17819'},
                '43': {'name': 'Shingleton', 'lat': '46.33225', 'lon': '-86.46589'},
                '44': {'name': 'Nisula', 'lat': '46.7658', 'lon': '-88.9452'},
                '45': {'name': 'Brevort', 'lat': '46.00841', 'lon': '-85.00555'},
                '46': {'name': 'Paradise', 'lat': '46.60047', 'lon': '-85.22383'},
                '47': {'name': 'Rose City', 'lat': '44.51188', 'lon': '-84.128347'},
                '48': {'name': 'Kalkaska', 'lat': '44.7166', 'lon': '-85.1906'},
                '49': {'name': 'Hartford', 'lat': '42.192917', 'lon': '-86.1657'},
                '50': {'name': 'Phoenix', 'lat': '47.38878', 'lon': '-88.27761'},
                '51': {'name': 'Maple City', 'lat': '44.8063', 'lon': '-85.8963'},
                '52': {'name': 'Eastport', 'lat': '45.1074', 'lon': '-85.3521'},
                '53': {'name': 'DeTour', 'lat': '45.97233', 'lon': '-84.08558'},
                '54': {'name': 'West Branch', 'lat': '44.24511', 'lon': '-84.22731'},
                '55': {'name': 'Charlevoix', 'lat': '45.36155', 'lon': '-85.17717'},
                '56': {'name': 'Rapid River', 'lat': '45.9261', 'lon': '-86.9837'},
                '57': {'name': 'Elmira', 'lat': '45.075', 'lon': '-84.8982'},
                '58': {'name': 'Lachine', 'lat': '45.0675', 'lon': '-83.7169'},
                '59': {'name': 'Houghton Lake', 'lat': '44.33489', 'lon': '-84.80651'},
                '60': {'name': 'Wolverine', 'lat': '45.27269', 'lon': '-84.59'},
                '61': {'name': 'Ludington', 'lat': '43.95574', 'lon': '-86.33909'},
                '62': {'name': 'Twin Lakes', 'lat': '46.88494', 'lon': '-88.8637'},
                '63': {'name': 'Kiva', 'lat': '46.2721', 'lon': '-87.1174'},
                '64': {'name': 'Ontonagon', 'lat': '46.86689', 'lon': '-89.31436'},
                '65': {'name': 'Harvey', 'lat': '46.48812', 'lon': '-87.23149'},
                '66': {'name': 'Curran', 'lat': '44.7265', 'lon': '-83.8083'},
                '67': {'name': 'St. Ignace', 'lat': '45.89735', 'lon': '-84.74475'},
                '68': {'name': 'Sundell', 'lat': '46.34745833', 'lon': '-87.11594722'},
                '69': {'name': 'Wellston', 'lat': '44.2227', 'lon': '-85.8053'},
                '70': {'name': 'Engadine', 'lat': '46.10089', 'lon': '-85.6178'},
                '71': {'name': 'Michigamme', 'lat': '46.53887', 'lon': '-88.12978'},
                '72': {'name': 'Trout Creek', 'lat': '46.47888', 'lon': '-88.99046'},
                '73': {'name': 'Grayling', 'lat': '44.61225', 'lon': '-84.70769'},
                '74': {'name': 'Seney', 'lat': '46.34538', 'lon': '-86.03578'},
                '75': {'name': 'Waters', 'lat': '44.8766', 'lon': '-84.68803'},
                '76': {'name': 'Cedar River', 'lat': '45.55023131', 'lon': '-87.26991195'},
                '77': {'name': 'Makinaw City', 'lat': '45.76115', 'lon': '-84.73107'},
                '78': {'name': 'Williamsburg', 'lat': '44.77101', 'lon': '-85.40423'},
                '79': {'name': 'Cooks', 'lat': '45.9096', 'lon': '-86.48062'},
                '80': {'name': 'Benzonia', 'lat': '44.58695', 'lon': '-86.09905'},
                '81': {'name': 'Calumet', 'lat': '47.21913', 'lon': '-88.458'},
                '82': {'name': 'Wakefield', 'lat': '46.4773', 'lon': '-89.9519'},
                '83': {'name': 'Gwinn', 'lat': '46.27616', 'lon': '-87.41586'},
                '84': {'name': 'Rudyard', 'lat': '46.18625', 'lon': '-84.56087'},
                '85': {'name': 'Hermansville', 'lat': '45.75189', 'lon': '-87.6825'},
                '86': {'name': 'Republic', 'lat': '46.25009', 'lon': '-88.01069'},
                '87': {'name': 'Presque Isle # 32', 'lat': '45.331', 'lon': '-83.5754'},
                '88': {'name': 'Silver City', 'lat': '46.83028', 'lon': '-89.56828'},
                '89': {'name': 'Blaney Park', 'lat': '46.1006', 'lon': '-85.9267'},
                '90': {'name': 'Galesburg', 'lat': '42.271174', 'lon': '-85.441124'},
                '91': {'name': 'Gaylord West', 'lat': '45.061387', 'lon': '-84.782222'},
                '92': {'name': 'Cut River Bridge', 'lat': '46.044314', 'lon': '-85.12423'},
                '93': {'name': 'I75NSMM2765-BDWS', 'lat': '44.9581167', 'lon': '-84.67409722'},
                '94': {'name': 'Kalamazoo', 'lat': '42.23807', 'lon': '-85.677811'},
                '95': {'name': 'Fife Lake', 'lat': '44.5123', 'lon': '-85.4022'},
                '96': {'name': 'Manistee', 'lat': '44.2198', 'lon': '-86.3088'},
                '97': {'name': 'US-31 at 31BR', 'lat': '43.25075', 'lon': '-86.20448'},
                '98': {'name': 'Coopersville', 'lat': '43.05335', 'lon': '-85.90804'},
                '99': {'name': 'US-31 at I-96', 'lat': '43.17153', 'lon': '-86.20579'},
                '103': {'name': 'Square Lake Road', 'lat': '42.614312', 'lon': '-83.233604'},
                '110': {'name': 'Escanaba River Bridge', 'lat': '45.794878', 'lon': '-87.07607'},
                '117': {'name': 'Engadine', 'lat': '46.10089', 'lon': '-85.6178'},
                '121': {'name': 'MDOT site', 'lat': '44.7556', 'lon': '-85.51966'},
                '124': {'name': 'MM-22 AT NORTH EAGLE', 'lat': '45.05765', 'lon': '-85.69938'},
                '125': {'name': 'M-32 AT COUNTY RD 491', 'lat': '44.96178', 'lon': '-84.28186'},
                '126': {'name': 'I-75 NORTH OF EXIT 215', 'lat': '44.28402', 'lon': '-84.32824'},
                '127': {'name': 'BDWS BRIDGE', 'lat': '44.17932', 'lon': '-85.42504'},
                '128': {'name': 'M115 at N River Road', 'lat': '43.979868', 'lon': '-85.083738'},
                '132': {'name': 'M-20 at Costabella Ave', 'lat': '43.595634', 'lon': '-85.085774'},
                '133': {'name': 'US-10 at M-47', 'lat': '43.59716', 'lon': '-84.139437'},
                '134': {'name': 'B-15', 'lat': '43.177376', 'lon': '-83.769255'},
                '135': {'name': 'B-17', 'lat': '42.80168', 'lon': '-83.730006'},
                '136': {'name': 'B-19', 'lat': '43.009118', 'lon': '-83.679774'},
                '137': {'name': 'I-69 at M-24', 'lat': '43.024745', 'lon': '-83.322205'},
                '138': {'name': 'WB I-69 Rest Area W of Capac', 'lat': '42.992582', 'lon': '-82.959523'},
                '139': {'name': 'Zilwaukee Bridge', 'lat': '43.48901', 'lon': '-83.925009'},
                '140': {'name': 'Henry Marsh Bridge', 'lat': '43.440276', 'lon': '-83.948587'},
                '141': {'name': 'M-1', 'lat': '42.774375', 'lon': '-83.526573'},
                '142': {'name': 'M-2', 'lat': '42.868855', 'lon': '-83.295864'},
                '143': {'name': 'M-5', 'lat': '42.477155', 'lon': '-83.113198'},
                '144': {'name': 'M-1', 'lat': '42.707172', 'lon': '-82.774397'},
                '145': {'name': 'M-1', 'lat': '42.367718', 'lon': '-83.545674'},
                '146': {'name': 'M-9', 'lat': '42.341591', 'lon': '-83.4415'},
                '147': {'name': 'M-9', 'lat': '42.275913', 'lon': '-83.160324'},
                '148': {'name': 'M-10', 'lat': '42.093341', 'lon': '-83.377842'},
                '149': {'name': 'M-11', 'lat': '42.21912', 'lon': '-83.54002'},
                '150': {'name': 'M-13', 'lat': '42.640709', 'lon': '-83.239648'},
                '151': {'name': 'M-14', 'lat': '42.453832', 'lon': '-83.430961'},
                '152': {'name': 'M-18', 'lat': '42.555847', 'lon': '-82.859558'},
                '153': {'name': 'M-19', 'lat': '42.496231', 'lon': '-82.918015'},
                '154': {'name': 'M-22', 'lat': '42.187557', 'lon': '-83.243858'},
                '155': {'name': 'M-24', 'lat': '42.383812', 'lon': '-83.478035'},
                '156': {'name': 'Crooks', 'lat': '42.605172', 'lon': '-83.170011'},
                '157': {'name': 'I75S-MM060.1', 'lat': '42.4604209', 'lon': '-83.1060032'}}

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

    placehead = 'Title: RWIS data \nRefresh: 2\nColor: 255 200 255\n     IconFile: 1, 18, 32, 2, 31, "https://mesonet.agron.iastate.edu/request/grx/windbarbs.png" \n     IconFile: 2, 15, 15, 8, 8, "https://mesonet.agron.iastate.edu/request/grx/cloudcover.png"\n     IconFile: 3, 25, 25, 12, 12, "https://mesonet.agron.iastate.edu/request/grx/rwis_cr.png"\n     Font: 1, 14, 1, "Arial"\n\n'

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

doit = RWIS('/cips/RWIS/midotmet.dat','/home/www/html/soo/rwis.txt')
# --------------------------------------------------------