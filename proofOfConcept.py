from Mambo import Mambo

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

        mambo.fly_direct(roll=60, pitch=0, yaw=1000, vertical_movement=0, duration=1.50)
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