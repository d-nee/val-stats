from tqdm import tqdm
from scraper import get_match_info

GAMEHASHES_PATH = './gamehashes.txt'
MATCH_CSV_PATH = './matches.csv'
MATCH_STATS_CSV_PATH = './player_stats.csv'

MATCH_KEYS = ['gamehash', 'map', 'start_date', 'start_time', 'duration',
              'a_score', 'b_score', 'a_bank', 'a_loadout', 
              'b_bank', 'b_loadout']

PLAYER_KEYS = ['gamehash', 'name', 'discrim', 'team', 'agent', 'ACS', 'ECON',
               'K', 'D', 'A', 'ADR', 'HSP', 'FK', 'FD', 'MK']

if __name__ == '__main__':
    with open(GAMEHASHES_PATH, 'r', encoding='utf-8') as file:
        gamehashes = file.read().split()
    
    match_file = open(MATCH_CSV_PATH, 'w', encoding='utf-8')
    match_stats_file = open(MATCH_STATS_CSV_PATH, 'w', encoding='utf-8')

    match_file.write(','.join(MATCH_KEYS) + '\n')
    match_stats_file.write(','.join(PLAYER_KEYS) + '\n')

    for gh in tqdm(gamehashes):
        m, p_info = get_match_info(gh)

        m_entry = ''
        for key in MATCH_KEYS:
            m_entry += f'{m[key]},'
        match_file.write(m_entry[:-1] + '\n')
        for p in p_info:
            p_entry = ''
            for key in PLAYER_KEYS:
                p_entry += f'{p[key]},'
            match_stats_file.write(p_entry[:-1] + '\n')
    
    match_file.close()
    match_stats_file.close()