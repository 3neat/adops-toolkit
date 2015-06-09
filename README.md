# Ad Ops Toolkit
A programmatic buy side toolkit for working with The Trade Desk HD Report files. 

## Current Features
------
* allows for aggregating Site report metrics using any combination of *Advertisers*, *Campaigns* and *Ad Groups* (called **Views**). 
* multiple **Views** can be saved within `views.json`, all of which will be processed when the program runs.

## Usage
------
1. Clone Ad Ops Toolkit to your computer: `git clone git@github.com:3neat/adops.git`
2. Within the `adops/` folder, save all HD raw reports into a sub-folder `reports/`. It's a good idea to keep your report date ranges consistant as .
3. Edit `views.json` to specify how to aggregate the data view:
```
    {
        "name": "samplefilename",     # Filename of the exported View
        "report_type": "Site",        # Report Type to be processed; currently only Site
        "advertiser": null,           # Specified Advertiser, Campaign, Ad Group IDs to be processed: 
        "campaign": null,             # - use a JSON array if 1 or more ID
        "adgroup": null,              # - if processing all, set to null
        "date_range": null,           # Number of days back to process; ie. null, or 120
        "rules": null                 # JSON array containing DataFrame query rules...
    }
```
4. Open console and execute main.py: `python main.py`
5. Processed files will be located in the `adops` folder


## TODO
------
~~* Add user specified rules filtering capability~~
~~* Assign Rules within Views~~
~~* Cross-platform compatibility~~
~~* Process by Campaign and Ad Group~~
* Fix problem with "(blank)" site impressions being excluded
* Compatibility with Conversion (and others) report types
* User specified 'groupby' - Site, Device Type, Supply Vendor, etc
* Create a requirements.txt
* Refactor file export to XLS using ExcelWriter if not too slow
* User specified reports folder location passed through CLI
* Implement unit tests
* Implement logging
* UI to build out Views
* Export data into DB
* Import data from DB in addition to report files
* Refactor into pip module
* User specified performance metric calculations
* User specified report types for processing reports outside TTD
* User specified location of export files
* TTD API integration