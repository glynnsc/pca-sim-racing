#!python3

#############################################
## This program acquires data directly from the 
## iRacing application via the python irsdk()
## and requires an active iRacing session
##
## To process telmetry data written to an ibt file,
## use the process-ibt.py program, which converts
## ibt to json records.
#############################################

import csv
import json
import time
import irsdk

ir = irsdk.IRSDK()
ir.startup()

## ToDo
# get CarSetUp
# car_setup = ir['CarSetup']
#    if car_setup:
#	setup = json.dumps(ir['CarSetup']) # creates a python dict
#        car_setup_tick = ir.get_session_info_update_by_key('CarSetup')
#        if car_setup_tick != state.last_car_setup_tick:
#            state.last_car_setup_tick = car_setup_tick
#            print('car setup update count:', car_setup['UpdateCount'])

# get SessionInfo
# if ir['SessionInfo']:
#	session = json.dumps(ir['SessionInfo'])
# get WeekendInfo
# if ir['WeekendInfo']:
#	weekend = json.dumps(ir['WeekendInfo'])
#   print(ir['WeekendInfo']['TeamRacing'])

#	SessionTimeOfDay = ir['SessionTimeOfDay'] # Time of day in seconds, s
#	Skies = ir['Skies'] # Skies (0=clear/1=p cloudy/2=m cloudy/3=overcast),
#      	Lap = ir['Lap'] # Laps started count,
#      	LapCurrentLapTime = ir['LapCurrentLapTime'] # Estimate of players current lap time as shown in F3 box, s
#      	CarIdxEstTime = ir['CarIdxEstTime'] # Estimated time to reach current location on track, s
#      	LapDist = ir['LapDist'] # Meters traveled from S/F this lap, m
#      	LapDistPct = ir['LapDistPct'] # sames as above as percentage
      
#      	Speed = ir['Speed'] # GPS vehicle speed, m/s
#      	Brake = ir['Brake'] # 0=brake released to 1=max pedal force, %
#      	Throttle = ir['Throttle'] # 0=off throttle to 1=full throttle, %
#      	RPM = ir['RPM'] # Engine rpm, revs/min
#      	Gear = ir['Gear'] # -1=reverse  0=neutral  1..n=current gear,
#      	LatAccel = ir['LatAccel'] # Lateral acceleration (including gravity), m/s^2
#      	LongAccel = ir['LongAccel'] # Longitudinal acceleration (including gravity), m/s^2


try:
	with open('output-file.csv', 'w', newline='') as f1:
		fieldnames = ['Lap', 'LapCurrentLapTime', 'LapDist', 'LapDistPct','Speed','Gear','RPM','Throttle','Brake','LatAccel','LongAccel']
		writer=csv.DictWriter(f1, fieldnames=fieldnames)
		writer.writeheader()
		while True:
			print(str(ir['Lap']), ir['LapCurrentLapTime'], ir['LapDist'], ir['LapDistPct'], ir['Speed'], ir['Gear'], ir['RPM'], ir['Throttle'], ir['Brake'], ir['LatAccel'], ir['LongAccel'], sep=',')
			
			writer.writerow({'Lap':ir['Lap'], 'LapCurrentLapTime':ir['LapCurrentLapTime'], 'LapDist':ir['LapDist'], 'LapDistPct':ir['LapDistPct'], 'Speed':ir['Speed'], 'Gear': ir['Gear'], 'RPM': ir['RPM'], 'Throttle':ir['Throttle'], 'Brake':ir['Brake'], 'LatAccel':ir['LatAccel'], 'LongAccel':ir['LongAccel']})
			time.sleep(1)
except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
