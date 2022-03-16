from tqdm import tqdm
from scraper import get_match_info, get_player_gamehashes

GENERATE_GAMEHASHES = True

PAGE_PLAYERS_PATH = './data/page_players.csv'
GAMEHASHES_PATH = './data/gamehashes.txt'

MATCH_CSV_PATH = './data/match.csv'
PLAYER_CSV_PATH = './data/player.csv'
MATCH_STAT_CSV_PATH = './data/match_stat.csv'
TEAM_STAT_CSV_PATH = './data/team_stat.csv'

MATCH_KEYS = ['gamehash', 'map', 'start_time', 'duration', 'a_score', 'b_score']

PLAYER_KEYS = ['ign', 'discrim', 'real_name', 'room_num']

MATCH_STAT_KEYS = ['gamehash', 'name', 'discrim', 'rank', 'team', 'agent', 
               'ACS', 'ADR', 'ECON', 'K', 'D', 'A', 'HSP', 'FK', 'FD', 'MK']

TEAM_STAT_KEYS = ['gamehash', 'team', 'bank', 'loadout']


def get_gh_dict():
    gh_dict = dict()
    with open(GAMEHASHES_PATH, 'r', encoding='utf-8') as file:
        gamehashes = file.read().split()
    for gh in tqdm(gamehashes):
        gh_dict[gh] = get_match_info(gh)
    return gh_dict


# Get gamehashes played by page members, return their pids
def get_page_gamehashes():
    with open(PAGE_PLAYERS_PATH, 'r', encoding='utf-8') as file:
        lines = file.read().split('\n')
    names = [l.split(',')[:2] for l in lines[1:]]
    page_pids, gamehashes = set(), set()
    for pid in tqdm(names):
        page_pids.add('#'.join(pid))
        if GENERATE_GAMEHASHES:        
            gamehashes.update(get_player_gamehashes(pid[0], pid[1]))
    print(len(gamehashes))
    if GENERATE_GAMEHASHES:
        with open(GAMEHASHES_PATH, 'w', encoding='utf-8') as file:
            for gh in gamehashes:
                file.write(f"{gh}\n")
    print('Page Gamehash Generation Complete')
    return page_pids


def write_match(game_info):
    match_file = open(MATCH_CSV_PATH, 'w', encoding='utf-8')
    match_file.write(','.join(MATCH_KEYS) + '\n')

    for gh, (m, p_info) in game_info.items():
        m_entry = ''
        for key in MATCH_KEYS:
            m_entry += f'{m[key]},'
        match_file.write(m_entry[:-1] + '\n')
    match_file.close()


# Add non-page players to 
def write_player(already_added, game_info):
    player_file = open(PLAYER_CSV_PATH, 'w', encoding='utf-8')
    player_file.write(','.join(PLAYER_KEYS) + '\n')

    for gh, (m, p_info) in game_info.items():
        for p in p_info:
            pid = f"{p['name']}#{p['discrim']}"
            if pid in already_added:
                continue
            player_file.write(f"{p['name']},{p['discrim']},,\n")
            already_added.add(pid)
    player_file.close()


def write_match_stat(game_info):
    match_stat_file = open(MATCH_STAT_CSV_PATH, 'w', encoding='utf-8')
    match_stat_file.write(','.join(MATCH_STAT_KEYS) + '\n')

    for gh, (m, p_info) in game_info.items():
        for p in p_info:
            p_entry = ''
            for key in MATCH_STAT_KEYS:
                p_entry += f'{p[key]},'
            match_stat_file.write(p_entry[:-1] + '\n')
    match_stat_file.close()


def write_team_stat(game_info):
    team_stat_file = open(TEAM_STAT_CSV_PATH, 'w', encoding='utf-8')
    team_stat_file.write(','.join(TEAM_STAT_KEYS) + '\n')

    for gh, (m, p_info) in game_info.items():
        a_entry = f"{m['gamehash']},A,{m['a_bank']},{m['a_loadout']}\n"
        b_entry = f"{m['gamehash']},B,{m['b_bank']},{m['b_loadout']}\n"
        team_stat_file.write(a_entry + b_entry)
    team_stat_file.close()


if __name__ == '__main__':
    page_pids = get_page_gamehashes()
    game_info = get_gh_dict()
    write_match(game_info)
    write_player(page_pids, game_info)
    write_match_stat(game_info)
    write_team_stat(game_info)