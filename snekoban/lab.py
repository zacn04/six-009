"""
6.1010 Spring '23 Lab 4: Snekoban Game
"""


# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}

def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    #ASSUME EMPTY SPACE UNLESS OTHERWISE SPECIFIED
    walls = set()
    computers = set()
    targets = set()
    player = set()
    for index, row in enumerate(level_description):
        for jindex, elem in enumerate(row):
            match elem:
                case ["wall"]:
                    walls.add((index,jindex))
                case ["computer"]:
                    computers.add((index,jindex))
                case ["target", "player"]:
                    player = (index,jindex)
                    targets.add((index,jindex))
                case ["player", "target"]:
                    player = (index,jindex)
                    targets.add((index,jindex))
                case ["target"]:
                    targets.add((index,jindex))
                case ["target", "computer"]:
                    targets.add((index,jindex))
                    computers.add((index,jindex))
                case ["computer", "target"]:
                    targets.add((index,jindex))
                    computers.add((index,jindex))
                case ["player"]:
                    player = (index, jindex)
    return {
        "player": player,
        "wall": frozenset(walls),
        "computer": computers,
        "target": frozenset(targets),
        "length": len(level_description),
        "width": len(level_description[0])
    }


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    return (game["target"] == game["computer"]) and (game["target"] != frozenset())


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    #CHECK IF A MOVE IS POSSIBLE
    ngame = {
        "player": game["player"],
        "wall": game["wall"],
        "computer": game["computer"].copy(),
        "target": game["target"],
        "length": game["length"],
        "width": game["width"]
    }
    pos = game["player"]
    new_pos = tuple(sum(x) for x in zip(pos, direction_vector[direction]))
    if new_pos in game["wall"]: #IMPOSSIBLE
        new_pos = pos
    elif new_pos in game["computer"]: 
        second_space = tuple(sum(x) for x in zip(new_pos, direction_vector[direction]))
        if second_space in game["computer"] or second_space in game["wall"]: #IMPOSSBILE
            new_pos = pos
        else:
            ngame["computer"].discard(new_pos)
            ngame["computer"].add(second_space)
        #OTHERWISE ITS FINE
    ngame["player"] = new_pos
    return ngame
            
def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    #ASSUME EMPTY UNLESS OTHERWISE SPECIFIED
    ngame = [[[] for i in range(game["width"])] for i in range(game["length"])]
    for elem in game:
        if elem in ("length", "width"):
            continue
        if elem in ("player"):
            ngame[game[elem][0]][game[elem][1]] = [str(elem)]
        for position in game[elem]:
            if elem != "player":
                ngame[position[0]][position[1]].extend([str(elem)])
    return ngame

def game_to_string(game):
    """Given a game representation,
    convert it to a string that represents the unique state."""
    string = ""
    string += str(hash(game["player"]))
    for loc in game["computer"]:
        string += str(hash(loc))
    return string

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    legal_moves = ["up", "down", "left", "right"]
    move_map = {}
    visited = set()
    root = game_to_string(game)
    queue = [game]
    visited.add(root)
    while queue:
        curr = queue.pop(0)
        if victory_check(curr):
            sequence = []
            while curr != game:
                b_repr = game_to_string(curr)
                sequence.append(move_map[b_repr][1])
                curr = move_map[b_repr][0]
            return sequence[::-1]
        for move in legal_moves:
            neighbour = step_game(curr,move)
            if not neighbour == curr:
                s_repr = game_to_string(neighbour)
                if s_repr not in visited:
                    visited.add(s_repr)
                    queue.append(neighbour)
                    move_map[s_repr] = (curr,move)
if __name__ == "__main__":
    pass
