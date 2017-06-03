def set_rps(*args):
    result = []
    for a in args:
        a = a.lower()
        if 'rock' in a:
            a = 'Rock'
        elif 'paper' in a:
            a = 'Paper'
        else:
            a = 'Scissors'
        result.append(a)
    result = tuple(result)
    return result


def eval_rps(a, b):
    if a == 'Rock':
        if b == 'Paper':
            return 'p2'
        if b == 'Scissors':
            return 'p1'
        return 'tie'
    if a == 'Paper':
        if b == 'Rock':
            return 'p1'
        if b == 'Scissors':
            return 'p2'
        return 'tie'
    if a == 'Scissors':
        if b == 'Rock':
            return 'p2'
        if b == 'Paper':
            return 'p1'
        return 'tie'
    return 0