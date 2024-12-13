import getpass
# import pprint
import os
import json
import requests
cache_filename = '.giftcard_cache'

cached_data = {}
if os.path.exists(cache_filename):
    cached_data = json.load(open(cache_filename))

if 'session_id' not in cached_data:
    # ask the user for an authenticated session ID, rather than hardcoding it or building an auth workflow here
    print('\nPlease log in via https://www.adventofcode.com/ then paste the authenticated Session ID here.\n')
    cached_data['session_id'] = getpass.getpass('Advent of Code Session ID: ')
    print()

    json.dump(cached_data, open(cache_filename, 'w'))

giftcard_star_threshold = 25
# TODO: update this URL each year (or make the year a parameter somehow)
leaderboard_url = 'https://adventofcode.com/2024/leaderboard/private/view/210077.json'

# use the session ID to get the data from the specified leaderboard
leaderboard_response = requests.get(leaderboard_url, headers={'Cookie': f'session={cached_data['session_id']};'})

try:
    leaderboard_response.raise_for_status()
except requests.HTTPError:
    print(f'URL request failed with {leaderboard_response.status_code}: {leaderboard_response.reason}')
    exit(-1)

try:
    leaderboard = leaderboard_response.json()
except requests.exceptions.JSONDecodeError:
    print('Valid response does not contain JSON body - perhaps not logged in? (need to delete cache file?)')
    exit(-1)

# see which users have crossed the threshold
gift_card_earners = {}
not_yet_there = {}
for member_id in leaderboard['members']:
    if leaderboard['members'][member_id]['name'] is None:
        leaderboard['members'][member_id]['name'] = 'Anonymous ' + member_id
    star_count = leaderboard['members'][member_id]['stars']
    if star_count >= giftcard_star_threshold:
        gift_card_earners[leaderboard['members'][member_id]['name']] = star_count
    elif star_count > 0:
        not_yet_there[leaderboard['members'][member_id]['name']] = star_count
    else:
        # do we care about users on the leaderboard who have not done anything this year???
        pass

print()
print('Gift Card Earners (alphabetical order):')
print('--------------------------------------')
print()

# sort output by star count descending (hence the *-1) then alphabetically by name ascending
for earner in sorted(gift_card_earners, key=lambda e: (gift_card_earners[e]*-1, e)):
    print(f'{earner}: {gift_card_earners[earner]}')

print(f'\nTotal qualifiers: {len(gift_card_earners)}')

print()
print('Non-Qualifiers (alphabetical order):')
print('-----------------------------------')
print()

# sort output by star count descending (hence the *-1) then alphabetically by name ascending
for earner in sorted(not_yet_there, key=lambda e: (not_yet_there[e]*-1, e)):
    print(f'{earner}: {not_yet_there[earner]}')

print(f'\nTotal non-qualifiers: {len(not_yet_there)}')
