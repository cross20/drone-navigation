from Mambo import Mambo
import string
import random
import time

string.numbers = '0123'

bestFitTime = 0.0
finishTime = 0.0

flightDuration = 1.0 # seconds
pauseDuration = 0.5 # seconds
flightCycles = 10

bestFitString = ['0', '1', '2', '3', '0', '1']
navString = ['0', '1', '2', '3', '0', '1']

mamboAddr = "71649864"
mambo = Mambo(mamboAddr, use_wifi=True)

print("connecting")
success = mambo.connect(num_retries=3)
print("connected")

for x in range(0, flightCycles):

    # first and second generation
    if x == 0 or x == 1:
        for z in range(0, 6):
            navString[z] = random.choice(string.numbers)

    # mutation generations (third and beyond)
    else:
        navString = bestFitString
        index = random.randint(0, (len(navString)-1))
        print("new index", index)
        navString[index] = random.choice(string.numbers)

    if (success):
        startTime = time.time()
        print("start time")
        print("taking off!")
        mambo.safe_takeoff(5)

        if (mambo.sensors.flying_state != "emergency"):

            for y in range(0, ((len(navString))-1)):

                roll = 0
                pitch = 0

                if navString[y] == '0':
                    roll = 60
                    print("right")

                elif navString[y] == '1':
                    roll = -60
                    print("left")

                elif navString[y] == '2':
                    pitch = 60
                    print("forward")

                elif navString[y] == '3':
                    pitch = -60
                    print("backward")

                else:
                    print("navigation error")

                mambo.fly_direct(roll=roll, pitch=pitch, yaw=0, vertical_movement=0, duration=flightDuration)
                mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=pauseDuration) # pause before moving again
                # Roll is axis from nose to tail (x)
                # Pitch is axis from wing to wing (y)
                # Yaw is axis from belly to top (z)

                if mambo.sensors.flying_state == 'landed':
                    finishTime = time.time() - startTime  # Current fitness

                    if finishTime > bestFitTime:
                        print("best flight time:", round(finishTime, 2), "seconds.")
                        bestFitTime = finishTime
                        bestFitString = navString

                    else:
                        print("flight time:", round(finishTime, 2), "seconds.")

                    print("flying state is %s" % mambo.sensors.flying_state)
                    break

            mambo.smart_sleep(5)

            print("landing")
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.safe_land(5)
            mambo.smart_sleep(5)

            finishTime = time.time() - startTime  # Current fitness

            if finishTime > bestFitTime:
                print("best flight time:", round(finishTime, 2), "seconds.")
                bestFitTime = finishTime
                bestFitString = navString

            else:
                print("flight time:", round(finishTime, 2), "seconds.")

            print("flying state is %s" % mambo.sensors.flying_state)

            if x != (flightCycles - 1):
                input("click \"here\" and press return (here) -->")

print("disconnecting")
mambo.disconnect()