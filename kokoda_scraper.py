from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Create a teacher's list as they are not to be added to the results
# Retrieve list of teachers from .env, private info
teachers = os.getenv('teachers_env').split(',')

# Returns: team_name, raised, target, unsorted_entrants, rank
def kokoda_scrape(lords_team) -> tuple[str, int, int, list, int]:
    html_text = requests.get(f'https://www.kokodachallenge.com/fundraisers/{lords_team}').text
    soup = BeautifulSoup(html_text, 'lxml')
    # Locate Div containing team name, funds and target
    team = soup.find('div', class_ = 'col-sm-5 pull-right funraisin-profile-header')
    # Check to see if the page exists (if team has been registered)
    if team is None:
        return lords_team, None, None, None, None
    
    """Team name"""
    team_name = team.h1.text.strip()
    
    """Money"""
    # Parent Div - money
    money = soup.find('div', class_ = 'sidebar-top')
    # Money Raised
    raised_div = money.find('div', class_ = 'iveRaised pull-left')
    raised_str = raised_div.h3.strong.text.strip()
    raised = round(int(raised_str.replace('$', '').replace(',', '')), 0)
    # Target Funds
    target_div = money.find('div', class_ = 'myGoal pull-right')
    target_str = target_div.h3.strong.text.strip()
    target = round(int(target_str.replace('$', '').replace(',', '')), 0)
    
    """Members"""
    # Locate Members Div and each member Div
    members_block = soup.find('div', id = 'MembersBlock')
    members = members_block.find_all('div', class_ = 'panel p20') 
    
    """Rank"""
    # Retrieve Rank of team
    rank_div = soup.find('div', class_ = 'raised')
    rank = rank_div.h3.text.strip()

    unsorted_entrants = []
    """Members"""
    # Loop through each member, retrieve name and raised amount
    for mem in members:
        memb = mem.find('div', class_ = 'profilename text-center')
        # Name
        member = memb.h3.text.strip()
        funds_tag = mem.find('h3', class_ = 'amount color-secondary mt0 mb0')
        # Extract funds amount
        funds_amount = int(funds_tag.text.strip().replace('$', '').replace('$', '').replace(',', '')) if funds_tag else 0
        # Add a tuple of member and funds to 'unsorted_entrants' list
        unsorted_entrants.append((member, funds_amount))

    return team_name, raised, target, unsorted_entrants, rank

# Process data so that it can be transferred to excel
def process_kokoda_data(teams: list) -> tuple[dict, dict, int]:
    # Dictionary to be returned and will contain all Kokoda info
    final_kokoda_team_results = {}
    # Dictionary to store information on highest overall fundraising (member & team)
    overall_results = {}
    # Keep track of sum of overall fundraising from each team
    overall_fundraising = 0
    # Keep track of the highest fundraiser for each team. To then extract the max from that list and input into 'I2'
    top_students_fundraisers = []
    # Append all raised amounts from each team to then extract team with highest amount raised and input into 'I3'
    all_teams_fundraise_amounts = []
    for name in tqdm(teams, desc='In Progress...'):
        team, raised_amount, target_amount, unsorted_entrants, rank = kokoda_scrape(name)
        # If team webpage does not exist, all variables except 'team' will be None. Omit this team from processing
        if raised_amount is None:
            # print(f'TM:{team}-AMT:{raised_amount}-TAR:{target_amount}-PER:{None}-STDMEM:{unsorted_entrants}-RNK:{rank}')
            # Input into final dicitonary for reference only. REMOVED as it causes issues in excel transfer
            # final_kokoda_team_results[team] = {'rais': None, 'targ': None,'perc': None, 'memb': None, 'rank': None}
            continue
        # Calculate overall fundraising from every team's raised_amount
        overall_fundraising += raised_amount
        # Create a sorted list of the team members and remove teachers that are present in 'teachers' variable, in the same operation
        sorted_members = sorted([x for x in unsorted_entrants if x[0] not in teachers], key=lambda x: x[1], reverse=True)
        # Take the highest fundraiser of that team
        # 'If' ternary operator is present to check if a teacher only is registered in the team (they are removed in above step)
        highest_fundraiser = max(sorted_members, key=lambda x: x[1]) if sorted_members else None

        # Calculate team's percentage of funds raised
        percentage = round(int((raised_amount / target_amount * 100)), 0)

        # Insert into dict here, sorted_members, percentage as well
        final_kokoda_team_results[team] = {'rais': raised_amount, 'targ': target_amount,'perc': percentage, 'memb': sorted_members, 'rank': rank}

        # Do not pass in highest fundraiser if None (There are no 'highest fundraisers' because there is no one with raised money)
        if highest_fundraiser is not None:
            # Split the top fundraiser so we can insert the team as well in 'top_students_fundraisers'
            n, m = highest_fundraiser # n = name, m = money
            # We split the values so we can add team name 'team' to top_students_fundraisers
            top_students_fundraisers.append((n, m, name))
        # Pass in team's fundraise amount to do a comparison for highest at the end
        all_teams_fundraise_amounts.append((team, raised_amount))
        # print(f'TM:{team}-AMT:{raised_amount}-TAR:{target_amount}-PER:{percentage}-STDMEM:{unsorted_entrants}-RNK:{rank}')
    
    # Find highest member fundraiser from all teams
    # 'IF' ternary operator checks if 'top_students_fundraisers' is empty due to the removal of teachers and students not being registered yet
    top_mem_fundraiser = max(top_students_fundraisers, key=lambda x:x[1]) if top_students_fundraisers else ()
    # Find highest team fundraiser
    top_team_fundraiser = max(all_teams_fundraise_amounts, key=lambda x:x[1])

    overall_results['top_mem_fundraiser'] = top_mem_fundraiser
    overall_results['top_team_fundraiser'] = top_team_fundraiser

    # print(f'Top Student Fundraiser: {top_mem_fundraiser[0]}, ${top_mem_fundraiser[1]}, {top_mem_fundraiser[2]}')
    # print(f'Top Team Fundraiser: {top_team_fundraiser[0]}, ${top_team_fundraiser[1]}')

    return final_kokoda_team_results, overall_results, overall_fundraising




















'''Multi-team Brisbane teams test'''
# bris_teams = ['BLORDS1', 'BLORDS2', 'BLORDS3', 'BLORDS4', 'BLORDS5', 'BLORDS6',
#                'BLORDS7', 'BLORDS8', 'BLORDS9', 'BLORDS10', 'BLORDS11', 'BLORDS12',
#                'BLORDS13', 'BLORDS14', 'BLORDS15'] 

# gc_teams = ['GCLORDS1', 'GCLORDS2', 'GCLORDS3', 'GCLORDS4', 'GCLORDS5', 'GCLORDS6',
#                'GCLORDS7', 'GCLORDS8', 'GCLORDS9', 'GCLORDS10'] 

# t_f_teams = ['BLORDS2', 'BLORDS3']

# def multi_teams(teams):
#     overall_fundraising = 0
#     for lords in teams:
#         team, raise_amount, target_amount, percentage, entrants, rank = kokoda_update(lords)
#         overall_fundraising += raise_amount
#         print(f'Team: {team} - Raised: ${raise_amount} - Target: ${target_amount} - Percentage: {percentage}% - Members: {entrants} - Rank: {rank}')
#     print(overall_fundraising)

# multi_teams(t_f_teams)

'''Single team test'''
# def single_team(team):
#     team, raise_amount, target_amount, percentage, entrants, rank = kokoda_update(team)
#     print(f'Team: {team} - Raised: {raise_amount} - Target: {target_amount} - Percentage: {percentage} - Members: {entrants} - Rank: {rank}')

# single_team('BLORDS10')


# TO CALCULATE
# Team percentage of raised/target
# Overall Fundraising - Move to NEW_Kokoda_results.py