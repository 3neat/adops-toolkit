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
```json
    {
        "name": "samplefilename",     # Filename of the exported View
        "report_type": "Site",        # Report Type to be processed; currently only Site
        "advertiser": null,           ## Specified Advertiser, Campaign, Ad Group IDs to be processed: 
        "campaign": null,             ## - use a JSON array if 1 or more ID
        "adgroup": null,              ## - if processing all, set to null
        "date_range": null            ## Number of days back to process; ie. null, or 120
    }
```
4. Open console and execute main.py: `python main.py`
5. Processed files will be located in the `adops` folder


## TODO
------
1. Add user specified rules filtering capability
2. Assign Rules within Views
3. Command line interface w/ arguments
4. Cross-platform compatibility
5. User specified reports folder location
6. Compatibility with other report types
7. User specified 'groupby' - Site, Device Type, Supply Vendor, etc
8. UI to build out Views
9. Implement unit tests
10. Import data from DB in addition to report files
11. Implement logging
12. Refactor into pip module
13. User specified performance metric calculations
14. User specified headers for working with reports from outside TTD
15. User specified location of export files
XX. API integration