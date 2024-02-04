import csv
import random

def makeMatchString(matchNum):
    eventString = '2024test_qm'
    matchString = eventString+str(matchNum)

    return matchString

def makeScout():
    scoutList = ['Bulbasaur', 'Charmander', 'Squirtle', 'Caterpie', 'Weedle', 'Pidgey', 'Rattata', 'Spearow', 'Ekans', 'Pikachu', 'Sandshrew', 
                 'Nidoran', 'Clefairy', 'Vulpix', 'Jigglypuff', 'Zubat', 'Oddish', 'Paras', 'Venonat', 'Diglett', 'Meowth', 'Psyduck', 'Growlithe']
    scout = scoutList[random.randint(0, len(scoutList) - 1)]

    return scout

def makeStartPos():
    xPos = random.randint(0,120)
    yPos = random.randint(0,480)
    pos = (str(xPos), str(yPos))

    return pos

def determinePreload(autoSpeaker):
    prob = random.randint(1,10)
    if int(autoSpeaker) > 0:
        preload = 'true'
    else:
        if prob > 1:
            preload = 'true'
        else:
            preload = 'false'

    return preload

def makeActions(row, preload):
    actions = []
    if preload == 'true':
        time = -1
    else:
        time = 0
    # Auto
    autoShots = int(row['Auto Speaker'])
    if autoShots != 0:
        autoSplit = 15 / autoShots
    for auto in range(0,autoShots):
        scoreTime = time + round(autoSplit / 2) + random.randint(-2,2)
        if time == -1:
            actionObj1 = {'time': time, 'action': 'intake', 'location': 'wing', 'phase': 'pregame'}
            actionObj2 = {'time': 153-scoreTime, 'action': 'place', 'location': 'speaker', 'amplified': 'false', 'phase': 'auto'}
        else:
            pickupLocation = random.randint(1,2)
            if pickupLocation == 1:
                location = 'center'
            else:
                location = 'wing'
            actionObj1 = {'time': 153-time, 'action': 'intake', 'location': location, 'phase': 'auto'}
            actionObj2 = {'time': 153-scoreTime, 'action': 'place', 'location': 'speaker', 'amplified': 'false', 'phase': 'auto'}
        actions.append(actionObj1)
        actions.append(actionObj2)
        time = scoreTime + round(autoSplit / 2) + random.randint(-4, 2)

    # Tele
    teleShots = int(row['Tele Muffled Speaker']) + int(row['Tele Amplified Speaker']) + int(row['Tele Amp'])
    ampShots = int(row['Tele Amp'])
    amplifiedShots = int(row['Tele Amplified Speaker'])
    if teleShots != 0:
        teleSplit = 135 / teleShots
    for tele in range(0, teleShots):
        if tele < ampShots:
            shotLocation = 'amp'
        else: 
            shotLocation = 'speaker'
        if ampShots <= tele < amplifiedShots:
            amplified = 'true'
        else:
            amplified = 'false'
        pickupLocation = random.randint(1,3)
        if pickupLocation == 1:
            location = 'center'
        elif pickupLocation == 2:
            location = 'source'
        else:
            location = 'wing'
        if time == -1:
            actionObj1 = {'time': time, 'action': 'intake', 'location': 'wing', 'phase': 'pregame'}
            time = 15
            scoreTime = time + round(teleSplit / 2) + random.randint(-4, 2)
            actionObj2 = {'time': 153-scoreTime, 'action': 'place', 'location': shotLocation, 'amplified': amplified, 'phase': 'teleOp'}
        else:
            scoreTime = time + round(teleSplit / 2) + random.randint(-4, 2)
            actionObj1 = {'time': 153-time, 'action': 'intake', 'location': location, 'phase': 'teleOp'}
            actionObj2 = {'time': 153-scoreTime, 'action': 'place', 'location': shotLocation, 'amplified': amplified, 'phase': 'teleOp'}

        actions.append(actionObj1)
        actions.append(actionObj2)
        time = scoreTime + round(teleSplit / 2) + random.randint(-4, 2)
    
    return actions

def postgame(robotScore):
    modifier = random.randint(0,2)
    if robotScore < 6:
        rating = random.randint(0,4)
        driverSkill = max(rating + 1 - modifier, 0)
        defenseSkill = max(rating - 1 + modifier, 0)
        speed = random.randint(1,5)
    elif 6 <= robotScore < 12:
        rating = random.randint(2, 6)
        driverSkill = max(rating + 1 - modifier, 0)
        defenseSkill = max(rating - 1 + modifier, 0)
        speed = random.randint(2,6)
    elif 12 <= robotScore < 18:
        rating = random.randint(4, 8)
        driverSkill = rating - 1 + modifier
        defenseSkill = rating + 1 - modifier
        speed = random.randint(4,8)
    elif 18 <= robotScore < 24:
        rating = random.randint(6, 10)
        driverSkill = min(rating - 1 + modifier, 10)
        defenseSkill = rating - 1 - modifier
        speed = random.randint(6, 10)
    else:
        rating = random.randint(8, 10)
        driverSkill = min(rating - 1 + modifier, 10)
        defenseSkill = rating - 1 - modifier
        speed = random.randint(8, 10)
    
    postgameArray = ["Test strat", str(rating), str(driverSkill), str(defenseSkill), str(speed), "Test thoughts"]

    return postgameArray

with open('MockScoutingSchema.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    header = ['Scouting Schema']
    writer.writerow(header)

    with open('MoreMockData.csv', mode='r') as s:
        reader = csv.DictReader(s)

        prevMatch = 0

        for row in reader:
            robotScore = int(row['Leave']) + int(row['Auto Speaker']) * 5 + int(row['Tele Muffled Speaker']) * 2 + \
                int(row['Tele Amplified Speaker']) * 5 + int(row['Climb']) + int(row['Tele Amp']) + int(row['Harmony']) \
                + int(row['Spotlight'])
            # Event
            matchString = makeMatchString(row['Match Number'])
            matchNum = str(row['Match Number'])
            alliance = row['Alliance Color']
            team = str(row['Team Number'])
            scout = makeScout()
            submission = str(random.randint(0,10000))

            # Pregame
            startPos = makeStartPos()
            startX = startPos[0]
            startY = startPos[1]
            preload = determinePreload(row['Auto Speaker'])

            # Game
            actions = makeActions(row, preload)

            # Untimed
            if int(row['Leave']) == 2:
                exitAuto = 'true'
            else:
                exitAuto = 'false'
            
            if int(row['Climb']) == 3:
                hang = 'true'
            else:
                hang = 'false'
            
            if int(row['Harmony']) == 2:
                harmony = 1
            else:
                harmony = 0
            
            if int(row['Spotlight']) == 1:
                spotlight = 'true'
            else:
                spotlight = 'false'
            if prevMatch != int(row['Match Number']):
                spotlightAttempt = 'true'
                prevMatch = int(row['Match Number'])
            else:
                spotlightAttempt = 'false'

            # Postgame
            postgameArray = postgame(robotScore)
            strategy = str(postgameArray[0])
            rating = postgameArray[1]
            driverSkill = postgameArray[2]
            defenseSkill = postgameArray[3]
            speed = postgameArray[4]
            thoughts = postgameArray[5]

            schema = '{{"event": "{0}", "match": {1}, "alliance": "{2}", "team": {3}, "scout": "{4}", "submission": {5},\
"pregame": {{"start": [{6},{7}], "preload": {8} }}, "game": {{"actions": {9}, "untimed": {{"exitAuto": {10},\
 "hangMatch": {11}, "parkMatch": {12}, "harmony": {13}, "spotlight": {14}, "spotlightAttempt": {21} }} }}, "postgame": {{\
"strategy": ["{15}"], "rating": {16}, "driverSkill": {17}, "defenseSkill": {18}, "speed": {19}, "thoughts": "{20}"\
}}}}'
            formattedSchema = schema.format(matchString,matchNum,alliance,team,scout,submission,startX,startY,preload,actions,exitAuto,\
                                hang,'false',harmony,spotlight,strategy,rating,driverSkill,defenseSkill,speed,thoughts,spotlightAttempt)
            print([formattedSchema])
            writer.writerow([formattedSchema])

# Fix the csv after it is written because I'm lazy
input = open('MockScoutingSchema.csv', 'r')
input = ''.join([i for i in input])\
    .replace('""', '"')\
    .replace('\'', '"')\
    .replace('"true"', 'true')\
    .replace('"false"', 'false')\
    .replace('"{', '{')\
    .replace('}"', '}')
output = open('MockScoutingSchemaFinal.csv', 'w')
output.writelines(input)
output.close()
