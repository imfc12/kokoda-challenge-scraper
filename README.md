# KOKODA WEB SCRAPER
This project scrapes fundraising data from the Kokoda Challenge website, including team totals and individual member contributions.

The data is processed into an Excel spreadsheet with sections for each team:
- **Team name**
- **Total raised**
- **Fundraising target**
- **Percentage of target achieved**

Within each team section, individual members are listed in descending order by amount raised.

At the top of the spreadsheet, the following summary is included:
- Total fundraising target (all teams combined)
- Overall amount raised
- Last updated timestamp
- Highest fundraising team
- Highest fundraising individual (across all teams)


## .env file to configure
Refer to `env_example.txt` for setup. The .env file should include:

- **Team names** – List of teams to track
- **Excluded members** – Teachers/group members excluded from individual rankings but included in team totals
- **Team ranges** – Define where each team's data should be placed in the `Kokoda Results.xlsx` file


## Code
1. `kokoda_scraper.py` – Scrapes the Kokoda Challenge team pages
2. `kokoda_excel_processor.py` – Processes the scraped data and writes to Excel

## How to Run
1. Set up `.env` as described
2. Run `kokoda_excel_processor.py`
3. Open `Kokoda Results.xlsx` to view results


### To Do / Improvements
- Make the script more modular:
    * Auto-fill cell A1 with: '{School/Group Name} Kokoda Fundraising {Year}'
    * Auto-calculate total fundraising target from all team targets and write to cell A2
    * Dynamically assign team sections based on event type (e.g. 'Brisbane 18km Event - Target {amount}')
    * Automatically adjust placement based on team count and order, instead of using hardcoded 'team ranges'
    
    