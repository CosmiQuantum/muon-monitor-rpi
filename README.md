# muon-monitor-rpi
RPi code and documentation for running the muon monitor at NEXUS

When stacking the PMTs, from top to bottom, PMT 15 should be on top, PMT 9 should be in the middle, and PMT 14 should be on the bottom.
When plugging in the signal cables from the PMT to the Linear Fan-in/Fan-out Module, ensure that, from top to bottom, you connect PMT 9, then PMT 14, then finally PMT 15.


All the detail here can be found in one of two papers _track down papers_

Muon paddles are stacked in the order seen above, each one consists of a scintillating material (the paddle bit), which then is connected to the Phototube high voltage zener divider. 
They are powered by the power supply, which is at the bottom of the electronics rack. 
They are connected via red cables to the high voltage divider. 

The signal from these muon paddles is then connected to the NIM fan in fan out module. 
This spreads the signal, where it is passed into the pulse discriminator
Pulse discriminator then converts into logical pulses (10 ns wide), which is then fed into a logical coincidence module. 
This determines if the pulses are found, within the given window, then exports them to a pulse widener, which basically just makes it into a 1 ms pulse for the raspberry pi DAC to read, as otherwise it's sampling rate is too low. 

The data is then stored in the raspberry pi, and is access by ssh-ing into it from loud-0hw, or any other computer on the LAN, though I always use loud-0hw. 
This data is found under `\home\muonium\data\muon_tagger\continuous\YYYY_MMDD\YYMMDD_HHMMSS.csv`

# Turning it on
