import os
import datetime
import re
import csv
from resources.RWISmetadata import RWIS_stations as stations
class RWIS():
    
    #--------------------------------------------------------------------------
    low = '125'
    high = '999'
    
    stnDict = {'t':{'color':'255 50 50','position':'-17,13, 1,','threshold':low,'error':'1001',
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
                    'name':'  Road Temp |  F  |'},
               'some_temperature_type':{'color':'255 255 0','position':'17,13, 1,','threshold':high,'error':'1001',
                    'name':'  Road Temp |  F  |'},
               'speed':{'color':'255 255 0','position':'17,13, 1,','threshold':high,'error':'1001',
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
        
    def __init__(self,input_dir,output_path):
        #self.datafile = 'midotmet_2022012813.dat'
        self.input_dir = input_dir
        self.files = os.listdir(self.input_dir)
        self.output_path = output_path
        self.output = open(self.output_path,'w',newline='')
        self.write = csv.writer(self.output)
        self.parms = ['dt', 'id', 'name', 'lat', 'lon', 't', 'rt', 'dp', 'vsby', 'wdir', 'wspd', 'gdir', 'gspd']
        self.write.writerow(self.parms)
        self.master_dat = []
        self.iterate_files()

    def iterate_files(self):
        for f in self.files:
            if '20221114' in str(f):
                fin = os.path.join(self.input_dir,f)
                self.open_next_file(fin)
                self.fdat.close()
            else:
                pass
        return

    def open_next_file(self,f):
        self.fdat = open(f,'r')
        self.build_placefile()
        self.fdat.close()
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

        Returns
        -------
                   final:
                          value that's been converted
        """
        numfloat = float(num)
        if (short == 'some_temperature_type'):
            divided_by_ten = round(numfloat)/10
            final = int(round((9/5) * divided_by_ten + 32))
        elif (short == 'speed'):
            final = int(round(((1.94 * numfloat)/10),1))         
        elif short == 'vsby':
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

        return final

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
        self.master_dat = []
        for line in self.fdat:
            time_missing = True
            dat = ['NA']*13    # create "blank" list where elements (listed in parms) are updated if they exist
            if "Id" in line:
                line2 = re.sub('"','',line)
                els = line2.split(',')
                for r in range(0,len(els)):
                    el = els[r]
                    if "Id" in el:
                        ID = self.split_colon(el)
                        if ID in stations:
                            dat[1] = ID
                            dat[2] = stations[ID]['name']
                            dat[3] = float(stations[ID]['lat'])
                            dat[4] = float(stations[ID]['lon'])
                        else:
                            break    # No point in continuing if this station isn't in the stations dictionary

                    elif "End" in el and time_missing:
                        if int(self.split_colon(el)) > 100:
                            epochtime = int(self.split_colon(el)) + (0 * 60 * 60)
                            obTime = str(datetime.datetime.fromtimestamp(epochtime))
                            dat[0] = obTime
                            time_missing = False
                            #print(dat[0])
                        else:
                            print(f'Bad time!')
                    elif "AirTemperature" in el:
                        if self.split_colon(el) not in ("1001"):
                            parsed = self.split_colon(el)
                            dat[5] = int(self.convert_met_values(parsed,'some_temperature_type'))
                    elif "PavementTemperature" in el:
                        if self.split_colon(el) not in ("1001"):
                            parsed = self.split_colon(el)
                            dat[6] = int(self.convert_met_values(parsed,'some_temperature_type'))
                    elif "DewpointTemp" in el:
                        if self.split_colon(el) not in ("1001"):
                            parsed = self.split_colon(el)
                            dat[7] = self.convert_met_values(parsed,'some_temperature_type')
                    elif "essVisibility" in el and "Situation" not in el:
                        if self.split_colon(el) not in ("1000001"):
                            parsed = self.split_colon(el)
                            dat[8] = self.convert_met_values(parsed,'vsby')               
                    elif "windSensorAvgDirection" in el:
                        if self.split_colon(el) not in ("361"):
                            dat[9] = self.split_colon(el)
                    elif "windSensorAvgSpeed" in el:
                        if self.split_colon(el) not in ("65535"):
                            parsed = self.split_colon(el)
                            dat[10] = self.convert_met_values(parsed,'speed')                
                    elif "windSensorGustDirection" in el:
                        if self.split_colon(el) not in ("361"):
                            dat[11] = self.split_colon(el)
                    elif "windSensorGustSpeed" in el:
                        if self.split_colon(el) not in ("65535"):
                            parsed = self.split_colon(el)
                            dat[12] = self.convert_met_values(parsed,'speed')     
                    else:
                        pass

            if dat[1] != 'NA':
                self.master_dat.append(dat)

        self.write.writerows(self.master_dat)

        return

# --------------------------------------------------------
# instantiate class with the following two arguments:
#  input - filepath to rwis data file
# output - filepath to created placefile

#doit = RWIS('/cifs/RWIS/midotmet.dat','/data/www/html/soo/rwis.txt')
doit = RWIS('C:/data/RWIS/text','C:/data/scripts/RWIS/rwis.txt')
# --------------------------------------------------------