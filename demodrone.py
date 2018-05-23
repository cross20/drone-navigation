from Mambo import Mambo
import string
import random
import time

string.numbers = '0123'

bestFit = open("mamboTimes.txt", "r")
bestFitTime = bestFit.read()
print("best fit time", bestFitTime)
bestFit.close()
crashed = False

bestFitTime = float(bestFitTime)

finishTime = 0.0
startTime = 0.0

flightDuration = 1.0 # seconds
pauseDuration = 0.5 # seconds

navString = ""
navList = ['', '', '', '', '', '']

mamboAddr = "71649803"
mambo = Mambo(mamboAddr, use_wifi=True)

parents = input("Is this the first generation? Enter \"y\" or \"n\". ")

if parents == 'y':
    navFile = open("mamboStrings.txt", "w")
    navTimeFile = open("mamboTimes.txt", "w")

    for x in range(0, 6):
        navString += random.choice(string.numbers)

    navFile.write(navString)
    #navTimeFile.write(0.0)

    for y in range (0, (len(navString))):
        navList[y] = navString[y]

    print("nav list is", navList)

    navFile.close()
    navTimeFile.close()

if parents == 'n':
    navFile = open("mamboStrings.txt", "r")
    navString = navFile.read()

    index = random.randint(0, 5)
    print("new index", index)

    for y in range (0, (len(navString))):
        navList[y] = navString[y]

    print("old list is", navList)

    navList[index] = random.choice(string.numbers)
    print("new list is", navList)

print("connecting")
success = mambo.connect(num_retries=3)
print("connected")

if (success):
    startTime = time.time()
    print("start time")
    print("taking off!")
    mambo.safe_takeoff(5)

    if (mambo.sensors.flying_state != "emergency"):

        for y in range(0, (len(navString))):

            roll = 0
            pitch = 0

            if navList[y] == '0':
                roll = 60
                print("right")

            elif navList[y] == '1':
                roll = -60
                print("left")

            elif navList[y] == '2':
                pitch = 60
                print("forward")

            elif navList[y] == '3':
                pitch = -60
                print("backward")

            else:
                print("navigation error")

            mambo.fly_direct(roll=roll, pitch=pitch, yaw=0, vertical_movement=0, duration=flightDuration)
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=pauseDuration)  # pause before moving again
            # Roll is axis from nose to tail (x)
            # Pitch is axis from wing to wing (y)
            # Yaw is axis from belly to top (z)

            if mambo.sensors.flying_state == 'landed':
                finishTime = time.time() - startTime  # Current fitness
                crashed = True

                print("flying state is %s" % mambo.sensors.flying_state)
                break

        mambo.smart_sleep(5)

        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
        mambo.smart_sleep(5)

        if crashed == False:
            finishTime = time.time() - startTime  # Current fitness

        if finishTime > bestFitTime:
            print("best flight time:", round(finishTime, 2), "seconds.")
            bestFitTime = finishTime

            tempString = ""

            for z in range(0, (len(navString))):
                print("z", z)
                tempString += navList[z]

            print("temp string", tempString)

            navFile = open("mamboStrings.txt", "w")
            navFile.write(tempString)
            navFile.close()

            bestFitStringTime = str(bestFitTime)

            bestFitOverwirte = open("mamboTimes.txt", "w")
            bestFitOverwirte.write(bestFitStringTime);
            bestFitOverwirte.close()

        else:
            print("flight time:", round(finishTime, 2), "seconds.")

    print("flying state is %s" % mambo.sensors.flying_state)

print("disconnecting")
mambo.disconnect()