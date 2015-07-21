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
        "report_type": "Site",        # Report Type to be processed
        "group_by": null,             # Specify the dimension to group the output report
        "advertiser": null,           # Specified Advertiser, Campaign, Ad Group IDs to be processed: 
        "campaign": null,             # - use a JSON array if 1 or more ID
        "adgroup": null,              # - if processing all, set to null
        "date_range": null,           # Number of days back to process; ie. null, or 120
        "rules": null                 # JSON array containing DataFrame query rules...
    }
```
4. Open console and execute main.py: `python main.py`
5. Processed files will be located in the `adops` folder
