from scraper import get_gamehashes
from tqdm import tqdm

# Input
USERNAMES_PATH = './names.txt'

# Output
GAMEHASHES_PATH = './gamehashes.txt'

if __name__ == '__main__':
    with open(USERNAMES_PATH, 'r', encoding='utf-8') as file:
        names = file.read().split()
    gamehashes = set()
    for name in tqdm(names):
        pid = name.split('#')
        gamehashes.update(get_gamehashes(pid[0], pid[1]))
    with open(GAMEHASHES_PATH, 'w', encoding='utf-8') as file:
        for gh in gamehashes:
            file.write(f"{gh}\n")
