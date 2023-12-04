import re

def parse_card(card_data: str) -> dict:
    card_data = card_data.strip()
    id_regex = re.compile(r'\d+:')
    regex = re.compile(r'\d+')
    
    n_card = int(re.findall(id_regex,card_data)[0].strip(':'))
    win_n = list(map(lambda x: int(x),re.findall(regex,card_data.split(': ')[1].split(' | ')[0])))
    own_n = list(map(lambda x: int(x),re.findall(regex,card_data.split(': ')[1].split(' | ')[1])))
    
    return {
        'n_card':int(n_card),
        'win_n':win_n,
        'own_n':own_n
    }

def get_card_score(card_dict: dict) -> int:
    score = 0
    for n in card_dict['own_n']:
        if n in card_dict['win_n']:
            if score == 0:
                score = 1
            else:
                score = score * 2
    return score

def check_card_generation(data: list) -> list:
    for i, card in enumerate(data):
        card_id = card['n_card']
        n_match = len(list(set(data[i]['win_n']).intersection(set(data[i]['own_n']))))
        data[i]['generates'] = list(range(card_id + 1, card_id + n_match + 1))

    return data

def get_expanded_len(data: list) -> int:
    n_total_cards = 0
    data = check_card_generation(data)
    curr_cards = [1]*len(data)

    i = 0
    while sum(curr_cards) > 0:
        while curr_cards[i] > 0:
            for generate_id in data[i]['generates']:
                curr_cards[generate_id - 1] += 1
            curr_cards[i] -= 1
            n_total_cards += 1
        i += 1

    return n_total_cards

if __name__ == "__main__":
    with open('input.txt','r') as fd:
        data = list(map(parse_card, fd.readlines()))

    # Part 1
    score = sum(list(map(get_card_score,data)))
    print(f'The total score of part 1 is {score}')

    # Part 2
    n_cards = get_expanded_len(data)
    print(f'The total number of cards in part 2 is {n_cards}')

