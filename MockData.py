import tbapy
import csv
import random
import math
import pandas
import numpy

def setapikey():
    global apikey
    apikey = 'fWFSAeNa3VxZUdVJhaXgAXjnM9mfLBmbw1bbOrviglJBtJxmcUTANIMpECdWSSwU'
    return apikey

def makeprofile(team_num):
    df = pandas.read_csv(r'MockData2.csv')
    teamdf = df[df['Team Number'] == int(team_num)]

    leaveRange = list(teamdf["Leave"])
    autoSpeakerRange =  list(teamdf["Auto Speaker"])
    autoAmpRange = list(teamdf["Auto Amp"])
    muffledSpeaker = list(teamdf["Tele Muffled Speaker"])
    amplifiedSpeaker = list(teamdf["Tele Amplified Speaker"])
    teleSRange = list(numpy.add(muffledSpeaker, amplifiedSpeaker))
    teleARange = list(teamdf["Tele Amp"])
    climbRange = list(teamdf["Climb"])
    harmonyRange = list(teamdf["Harmony"])
    spotlightRange = list(teamdf["Spotlight"])

    profile = {'team': team_num,
               'leave': leaveRange,
               'auto_speaker': autoSpeakerRange,
               'auto_amp': autoAmpRange,
               'tele_speaker': teleSRange,
               'tele_amp': teleARange,
               'climb': climbRange,
               'harmony': harmonyRange,
               'spotlight': spotlightRange}
    
    return profile

def setstat(range):
    rangeLength = len(range)
    randomNumber = random.randint(0,rangeLength-1)
    stat = range[randomNumber]

    return stat

tba = tbapy.TBA(setapikey())
year = 2024
events = ["2017mnmi2"]

matches = tba.event_matches(events[0])

with open('MockData.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ["Match Number", "Alliance Color", "Team Number", "Leave", "Auto Speaker", "Auto Amp", "Tele Muffled Speaker", "Tele Amplified Speaker", "Tele Amp", "Climb", "Harmony", "Spotlight"]
    writer.writerow(header)

    for match in matches:
        matchID = match["key"]
        if match["match_number"] > 57 or match["comp_level"] != "qm":
            continue
            
        matchNumber = match["match_number"]
        redAlliance = match["alliances"]["red"]["team_keys"]
        blueAlliance = match["alliances"]["blue"]["team_keys"]
        autoAmp = 0
        amplifiedSpeaker = 0
        ri = 0
        for robot in redAlliance:
            ri += 1
            allianceColor = "Red"
            teamNumber = str(robot)[3:]
            leave = 0
            climb = 0

            if ri == 1:
                if match["score_breakdown"]["red"]["robot1Auto"] == "Mobility":
                    leave = 2
            elif ri == 2:
                if match["score_breakdown"]["red"]["robot2Auto"] == "Mobility":
                    leave = 2
            elif ri == 3:
                if match["score_breakdown"]["red"]["robot3Auto"] == "Mobility":
                    leave = 2
            
            with open('SampleData.csv', mode='r') as s:
                reader = csv.DictReader(s)
                
                for row in reader:
                    if str(matchNumber) == row["MATCH "] and teamNumber == row["TEAM"]:
                        if int(row["Auto Gear"]) > 0:
                            autoSpeaker = random.randint(1,3)
                        else:
                            autoSpeaker = 0

                        if int(row["Tele Gear"]) > 0:
                            muffledSpeaker = random.randint(int(row["Tele Gear"]), int(row["Tele Gear"]) + 3)
                        else:
                            muffledSpeaker = 0

                        if int(row["Tele Fuel"]) > 0:
                            teleAmp = math.ceil(int(row["Tele Fuel"]) / 6)
                        else:
                            teleAmp = 0

                        if row["Climb"] == '0.5':
                            climb = 3
                            harmony = 0
                            spotlight = random.randint(0,1)
                        elif row["Climb"] == '1':
                            climb = 3
                            harmony = 2
                            spotlight = random.randint(0,1)
                        else:
                            climb = 0
                            harmony = 0
                            spotlight = 0

                        writeRow = [matchNumber, allianceColor, teamNumber, leave, autoSpeaker, autoAmp, muffledSpeaker, amplifiedSpeaker, teleAmp, climb, harmony, spotlight]
                        print(writeRow)
                        writer.writerow(writeRow)
                        break
        bi = 0
        for robot in blueAlliance:
            bi += 1
            allianceColor = "Blue"
            teamNumber = str(robot)[3:]
            leave = 0
            climb = 0

            if bi == 1:
                if match["score_breakdown"]["blue"]["robot1Auto"] == "Mobility":
                    leave = 2
            elif bi == 2:
                if match["score_breakdown"]["blue"]["robot2Auto"] == "Mobility":
                    leave = 2
            elif bi == 3:
                if match["score_breakdown"]["blue"]["robot3Auto"] == "Mobility":
                    leave = 2
            
            with open('SampleData.csv', mode='r') as s:
                reader = csv.DictReader(s)
                
                for row in reader:
                    if str(matchNumber) == row["MATCH "] and teamNumber == row["TEAM"]:
                        if int(row["Auto Gear"]) > 0:
                            autoSpeaker = random.randint(1,3)
                        else:
                            autoSpeaker = 0

                        if int(row["Tele Gear"]) > 0:
                            muffledSpeaker = random.randint(int(row["Tele Gear"]), int(row["Tele Gear"]) + 3)
                        else:
                            muffledSpeaker = 0

                        if int(row["Tele Fuel"]) > 0:
                            teleAmp = math.ceil(int(row["Tele Fuel"]) / 6)
                        else:
                            teleAmp = 0

                        if row["Climb"] == '0.5':
                            climb = 3
                            harmony = 0
                            spotlight = random.randint(0,1)
                        elif row["Climb"] == '1':
                            climb = 3
                            harmony = 2
                            spotlight = random.randint(0,1)
                        else:
                            climb = 0
                            harmony = 0
                            spotlight = 0

                        writeRow = [matchNumber, allianceColor, teamNumber, leave, autoSpeaker, autoAmp, muffledSpeaker, amplifiedSpeaker, teleAmp, climb, harmony, spotlight]
                        print(writeRow)
                        writer.writerow(writeRow)
    
    for match in matches:
        if match["match_number"] < 57 or match["comp_level"] != "qm":
            continue

        matchNumber = match["match_number"]
        redAlliance = match["alliances"]["red"]["team_keys"]
        blueAlliance = match["alliances"]["blue"]["team_keys"]
        autoAmp = 0
        amplifiedSpeaker = 0
        ri = 0
        for robot in redAlliance:
            ri += 1
            allianceColor = "Red"
            teamNumber = str(robot)[3:]
            leave = 0
            climb = 0

            if ri == 1:
                if match["score_breakdown"]["red"]["robot1Auto"] == "Mobility":
                    leave = 2
            elif ri == 2:
                if match["score_breakdown"]["red"]["robot2Auto"] == "Mobility":
                    leave = 2
            elif ri == 3:
                if match["score_breakdown"]["red"]["robot3Auto"] == "Mobility":
                    leave = 2

            profile = makeprofile(teamNumber)

            autoSpeaker = setstat(profile["auto_speaker"])
            autoAmp = setstat(profile["auto_amp"])
            muffledSpeaker = setstat(profile["tele_speaker"])
            amplifiedSpeaker = 0
            teleAmp = setstat(profile["tele_amp"])
            climb = setstat(profile["climb"])
            harmony = setstat(profile["harmony"])
            spotlight = setstat(profile["spotlight"])

            writeRow = [matchNumber, allianceColor, teamNumber, leave, autoSpeaker, autoAmp, muffledSpeaker, amplifiedSpeaker, teleAmp, climb, harmony, spotlight]
            print(writeRow)
            writer.writerow(writeRow)
        bi = 0
        for robot in blueAlliance:
            bi += 1
            allianceColor = "Blue"
            teamNumber = str(robot)[3:]
            leave = 0
            climb = 0

            if bi == 1:
                if match["score_breakdown"]["blue"]["robot1Auto"] == "Mobility":
                    leave = 2
            elif bi == 2:
                if match["score_breakdown"]["blue"]["robot2Auto"] == "Mobility":
                    leave = 2
            elif bi == 3:
                if match["score_breakdown"]["blue"]["robot3Auto"] == "Mobility":
                    leave = 2

            profile = makeprofile(teamNumber)

            autoSpeaker = setstat(profile["auto_speaker"])
            autoAmp = setstat(profile["auto_amp"])
            muffledSpeaker = setstat(profile["tele_speaker"])
            amplifiedSpeaker = 0
            teleAmp = setstat(profile["tele_amp"])
            climb = setstat(profile["climb"])
            harmony = setstat(profile["harmony"])
            spotlight = setstat(profile["spotlight"])

            writeRow = [matchNumber, allianceColor, teamNumber, leave, autoSpeaker, autoAmp, muffledSpeaker, amplifiedSpeaker, teleAmp, climb, harmony, spotlight]
            print(writeRow)
            writer.writerow(writeRow)
