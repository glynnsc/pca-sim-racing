# PCA SimRacing
Useful things for Porsche Club of America PCA SimRacing with iRacing.

I'm a longtime PCA member, racer and instructor, but new to iRacing (January-2021), so figured I would capture things I found useful along the way to getting started with PCA-SimRacing.

This repo is focused on the basics of PCA SimRacing with iRacing, and goes deep into details, software and methods for telemetry data analysis.


### Important iRacing Links
  - https://www.iracing.com/
  - https://ir-core-sites.iracing.com/members/pdfs/101101.01_User_Guide.pdf
  - https://d3bxz2vegbjddt.cloudfront.net/members/pdfs/FIRST_Sporting_Code_v2014.12.17.01.pdf
  
### Other Useful Links
  - Good Set of reference material and insights from [EdRacing](http://www.edracing.com/edr/)
  - YouTube Channels:
    - TBD

### Important PCA SimRacing Links
  - How to get started, all the information below can be found at https://pcasimracing.com/
  - Must have: Sim racing setup, wheel, pedals, and an iRacing account. https://www.iracing.com/
  - Sign up for the PCA Simracing League here. https://register-simracing.pca.org/
  - Sign up for our Discord server here. https://pcasimracing.com/joining-our-discord-server/


### Cockpit - Not recommendations, this is just a list of what I started with.
  - RSeat RSEAT N1 Black/White
  - RSeat N1 Keyboard/Mouse tray Upgrade kit White
  - Logitech - G923 Racing Wheel and Pedals, FFB Strength 2.2Nm
  - Headset - [SteelSeries Actis-7 White](https://steelseries.com/gaming-headsets/arctis-7?color=white)
  - Lenovo Legion Tower 5 - Intel Core i7-10700F (2.90 GHz) - 16GB DDR4 - 1TB HDD + 256GB SSD - NVIDIA GeForce RTX 2060 6 GB GDDR6 - Windows 10 Home

### Newbie Stuff
- Field Of View Set-Up - https://www.youtube.com/watch?v=23PXJooAfrg&feature=emb_logo ; https://www.youtube.com/watch?v=PQVQhYU3ccs
  - Understanding that this can be changed and how to change it to your liking is most important.  The standard/recommendations from iRacing or Youtube or Experts may not be the right set up for each person.  This is a very individualized thing.  I ended up using a FOV setting of 65 because it feels more natural and I'm faster and more consistent.  The FOV iRacing calculation and the recommendations from uTube were 45, which I could not even drive at all.
  - **Pro-Tip: this can be adjusted on the fly using keys `[` and `]`.**
  - **Pro-Tip: use `Ctrl-F12` while in the pit, then choose `Cockpit` for video view.  This pops out graphics black box where many viewing, driving position and sound adjustments can be adjusted while sitting in the car in the pits.** 
- Force Feedback Set-Up - https://www.youtube.com/watch?v=5v8XSEeJFnM&feature=youtu.be
  - Similar to FOV, it is important to understand how to set this up.  Yet the recommendations may not be right for each person.  After much testing and set up according to iRacing, uTube and others sources I ended up faster and more consistent with a much lighter force feedback than was recommended based on my setup
- Brake Pedal Force and Range Calibration - https://www.youtube.com/watch?v=6wYWnVp9s2I
  - With the lower to middle tier pedal sets, getting the brake force and brake pedal position correct is challenging.  And this issue has a substantial impact on laptimes.  I've been struggling with this one quite a bit, never being able to get the pedal position quite right, under braking, over-braking, lock-up, trail-braking - all of it very inconsistent, which leads to difficulty laying down fast and consistent laps.  As a rookie I'm learning that, in addition to laying down lot's of laps, watching videos, testing different setups and analyzing telemetry, another very important way of reducing laptimes is getting your Cockpit configurations and calibrations optimized for your style, the car and the track.  Check out the youtube video above, which talks about this issue and describes a configuration mod that will significantly improve your confidence and consistency in the braking zone - which will ultimately lead to laying down those fast laps.
  - It comes down to each of us being unique, test, test, test and find out what is right for you.  And accept that what is right for you today may change over time based on experience, equipment, game and tech updates and may just evolve over time as your driving style evolves.
- Keyboard Shortcuts - https://www.iracing.com/keyboard-shortcuts/
 - Communications & Sound
    - Adjustments for Racing and Comms for iRacing + Discord - links TBD
    - Adjust the app.ini file according this youtube guide, maximize tire and other noises, reduce engine noise, make sure able to hear comms over car noise.

### Telemetry Data Pipeline
- Telemetry folder, ibt file, Alt-L
- Python SDK for processing telemetry data: https://github.com/kutu/pyirsdk
  - this sdk actually works right off the shelf.  I did some testing and can capture all iRacing parameters with just a few lines of code --- Nice!
  - Find a simple python program at [telemetry/acquire-data.py](https://github.com/glynnsc/pca-sim-racing/blob/main/telemetry/acquire-data.py) to capture real-time data and write to csv out-file.
  - Process iRacing.ibt files with [telemetry/process-ibt.py](https://github.com/glynnsc/pca-sim-racing/blob/main/telemetry/process-ibt.py) - telemetry data is written to .ibt files by keyboard `Alt-L` - ibt files contain more data including track GPS Latitutude and Longitude coordinates which are required for track map visuals and positional comparisons.
  - Automated data pipeline in AWS using S3, Glue Job, Glue Crawler and Athena.  The iRacing.ibt files can be uploaded to an S3 bucket, processed by [telemetry/proccess-ibt-aws-glue.py](https://github.com/glynnsc/pca-sim-racing/blob/main/telemetry/proccess-ibt-aws-glue.py) and made available for interactive analysis via Athena SQL.  To-Do - Config details for Glue ETL job and Glue Crawler - will right up a gist on this part.
  
### Analysis
  - Need to checkout [Virtual Race School](https://virtualracingschool.com/) for data analysis
  - Session Telemetry Analysis Jupyter Notebook [iracing-telemetry-methods-dev1](https://github.com/glynnsc/pca-sim-racing/blob/main/telemetry/iracing-telemetry-methods-dev1.ipynb)
  - ![](https://user-images.githubusercontent.com/9019313/109421862-1db78d80-79a7-11eb-92f2-31f2dfeff688.png)
