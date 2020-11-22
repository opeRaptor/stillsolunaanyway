import ugfx, gc, wifi, badge, system, time, display, machine
from time import sleep, localtime
import urequests as requests

#/** the width of the eink display */
#define BADGE_EINK_WIDTH  296
#/** the height of the eink display */
#define BADGE_EINK_HEIGHT 128

try: 
    while True:
        try:
            wifi.init()
            while not wifi.sta_if.isconnected():
                sleep(0.1)
        except:
            wifi.connect()
            print("Connecting to WiFi")
            if not wifi.wait():
                time.sleep(2)
                print("Connection Error, Rebooting")
                machine.reset()
        
        wifi.ntp(False)
        rtc = machine.RTC()
        print(rtc.now())
        
        #url="http://ip-api.com/line/?fields=city"
        #url = "http://travelplanner.mobiliteit.lu/restproxy/departureBoard?accessId=cdt&id=A=1@O=Lintgen,%20Kräizung@X=6,125115@Y=49,720344@U=82@L=160702003@B=1@p=1594365298&format=json"
        url= 'http://wttr.in/?format="%S:+%m+%s"'
        while True:
            r = requests.get(url)
            print("API HTTP request status Code:",r.status_code)
            #print(r.status_code)
            
            if r.status_code == 200:
                break
            else:
                # Hope it won't 500 a little later
                print("Bad response")
                time.sleep(5)

        print("Data:",r.text)

        sunrise = r.text[1:6]
        moonPhase = r.text[11:12]
        sunset = r.text[13:18]
        #sunrise = sunrise[:8]
        
        r.close()
        gc.collect()
        #sunrise = r.text[:8]
        #sunset = r.text[:-8]


        print(sunrise)
        print(moonPhase)
        print(sunset)
        
        #sunriseSec = (sunrise[1]*10*60*60) + (sunrise[2]*60*60) + (sunrise[3]*10*60) + (sunrise[4]*60)

        sunriseSec = (int(sunrise[0]) *10*60*60) + (int(sunrise[1]) *60*60) + (int(sunrise[3]) *10*60) + (int(sunrise[4]) *60)
        sunsetSec = (int(sunset[0]) *10*60*60) + (int(sunset[1]) *60*60) + (int(sunset[3]) *10*60) + (int(sunset[4]) *60)
        
        nightLen = (24*3600) - sunsetSec + sunriseSec
        dayLen = sunsetSec - sunriseSec

        #now = (int(sunset[0]) *10*60*60) + (int(sunset[1]) *60*60) + (int(sunset[3]) *10*60) + (int(sunset[4]) *60)
        now = rtc.now()
        nowStr = str(now[3]) + ":" + str(now[4])
        now = int(now[3])*60*60 + int(now[4])*60
        
        print("now",now)
        if (now >= sunsetSec) & (now <= (24*3600)):
            print("Before midnight")
            nowNight = (now - sunsetSec)
        elif (now <= sunriseSec) & (now >= 0):
            print("After midnight")
            nowNight = ((24*3600)-sunsetSec) + now

        print("sunrise",sunriseSec)
        print("sunset",sunsetSec)

        print("night len",nightLen)
        print("day len",dayLen)
        print(24*3600,":",dayLen+nightLen)

        print("now night",nowNight)

        x = int((nowNight/nightLen) * 296)
        print("Moon pos:",x)
        x = int(x - (90/2))
        print("Moon pos:",x)

        display.drawFill(0x000000) # Fill the screen with black
        display.drawPng(x,8,"/lib/stillsolunaanyway/moon.png")
        print(display.pngInfo("/lib/stillsolunaanyway/moon.png"))
        

        display.drawText(0, 105, sunset, 0xFFFFFF, "Roboto_Regular18") 
        display.drawText(140, 105, nowStr, 0xFFFFFF, "Roboto_Regular18") 
        display.drawText(245, 105, sunrise, 0xFFFFFF, "Roboto_Regular18") 
        
        
        display.flush() # Write the contents of the buffer to the display
        badge.eink_busy_wait()
        
        time.sleep(15)
        #display.drawpng(0,0,moon1.png)

except:
    print("################################################################################################################################################################")
    print("################################################################################################################################################################")
    print("Something bad happened (blame lack of RAM), exception, we need a reboot")
    print("################################################################################################################################################################")
    print("################################################################################################################################################################")
    #system.reboot()
    machine.reset()


###############################################################################################################################################################################
import wifi, woezel,machine
wifi.connect()
wifi.wait()
woezel.install("stillsolunaanyway")
machine.reset()

#make app run on boot
import machine
machine.nvs_setstr("system", "default_app", "stillsolunaanyway")