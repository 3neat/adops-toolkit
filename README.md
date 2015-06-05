# adops
AdOps Toolkit  - A programmatic buy side toolkit for working with The Trade Desk HD Report files... A work in progress

## Current functionality
1. Create custom Views that enable concatenation of weekly Site report files. A View can be any combination of Advertiser, Campaign and AdGroups for a given Report Type and Date Range.
2. Strip down exported files to most common fields and add performance metrics


## Setup
* Note: must run this module in PyCharm until __main__ is fixed
1. Within the module folder, create a 'reports/' that contains all HD Report files to be analyzed
2. Create new views within 'views.json', if field is not used set to null. 'advertiser', 'campaign', 'adgroup' are JSON Array values. 'date_range' is a numeric string (without quotes).
