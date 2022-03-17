with open('./data/player.csv', 'r', encoding='utf-8') as file:
    lines = file.read().split('\n')
with open('./data/player.csv', 'w', encoding='utf-8') as file:
    file.write(lines[0] + '\n')
    for l in lines[1:]:
        file.write(l[:-1] + '\\N,\\N\n')
