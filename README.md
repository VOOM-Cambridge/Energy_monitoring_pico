# Energy_monitoring_pico

To use first load the pimoroni-badger2040w-v0.0.2-micropython.uf2 firmware onto the pico. 
Once loaded and it has restarted automatically save the remaining files onto the pico as named. 
Use IDE such as Thorny to edit codes

To set up:
1. Set Wifi login details 
2. Set address for where MQTT data packets should be sent (the MQTT boker locations)
3. Test - it will try to connect 20 times before failing, check if it connects to wifi and broker ok
4. Current sensor may need additional calibations
