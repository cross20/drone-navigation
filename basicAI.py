from Mambo import Mambo
import string
import random

# Basic AI Navigation

string.numbers = '01'

# Navigation will determine where the drone will go
# 0 (left), 1 (right)
boy = ""
girl = ""
# Mother will cross with the father
mother = ""
father = ""

mother = random.choice(string.numbers)
father = random.choice(string.numbers)

# Cross over

crossPointBoy = random.randint(0, len(mother))
boy += father[crossPointBoy:]
boy += mother[:crossPointBoy]

crossPointGirl = random.randint(0, len(father))
girl += mother[crossPointGirl:]
girl += father[:crossPointGirl]

# Mutation

boy[random.randint(0, len(boy))] = random.choice(string.numbers)
girl[random.randint(0, len(girl))] = random.choice(string.numbers)

# Concatenation

boy += random.choice(string.numbers)
girl += random.choice(string.numbers)

mamboAddr = "71649864"

mambo = Mambo(mamboAddr, use_wifi=True)

print("connecting")
success = mambo.connect(num_retries=3)
print("connected")


if(success):
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)



    print("taking off!")
    mambo.safe_takeoff(5)

    if (mambo.sensors.flying_state != "emergency"):

        print("flying state is %s" % mambo.sensors.flying_state)
        print("Flying direct: going up")

        for x in range(0, len(boy)):
            if boy[x] == 0:
                mambo.fly_direct(roll=60, pitch=0, yaw=0, vertical_movement=0, duration=1.50)
                # Roll is axis from nose to tail (x)
                # Pitch is axis from wing to wing (y)
                # Yaw is axis from belly to top (z)
            if boy[x] == 1:
                mambo.fly_direct(roll=-60, pitch=0, yaw=0, vertical_movement=0, duration=1.50)
                # Roll is axis from nose to tail (x)
                # Pitch is axis from wing to wing (y)
                # Yaw is axis from belly to top (z)


        mambo.smart_sleep(5)

        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
        mambo.smart_sleep(5)

print("disconnect")
mambo.disconnect()

