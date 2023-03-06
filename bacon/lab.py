"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3


# NO ADDITIONAL IMPORTS ALLOWED!

# we are using BFS. FIFO, QUEUE


def transform_data(raw_data):
    """WE NEED TO KNOW IF ACTORS HAVE ACTED TOGETHER
    (I.E. A DICT WITH ACTOR KEY AND SET OF ACTOR VALUES)
    AS WELL AS A DICT WITH FILM KEY AND ACTORS,
    THEN WE CAN HAVE ACTORS CONNECTING FILMS"""
    actor_dict = {}
    film_dict = {}
    dict_film = {}
    # generating actor dict and film dict at the same time!
    for data in raw_data:
        try:
            actor_dict[data[1]].add(data[0])
        except KeyError:
            actor_dict[data[1]] = {data[0], data[1]}
        try:
            actor_dict[data[0]].add(data[1])
        except KeyError:
            actor_dict[data[0]] = {data[1], data[0]}
        try:
            film_dict[data[1]].add(data[-1])
        except KeyError:
            film_dict[data[1]] = {data[-1]}
        try:
            film_dict[data[0]].add(data[-1])
        except KeyError:
            film_dict[data[0]] = {data[-1]}
        if data[-1] not in dict_film:
            dict_film[data[-1]] = {data[0], data[1]}
        elif data[-1] in dict_film:
            dict_film[data[-1]].add(data[0])
            dict_film[data[-1]].add(data[1])
    # corrections
    return actor_dict, film_dict, dict_film


def acted_together(transformed_data, actor_id_1, actor_id_2):
    return actor_id_1 in transformed_data[0][actor_id_2]


def actors_with_bacon_number(transformed_data, n):
    """
    Returns a set of actors with the specified bacon number.

            Parameters:
                    transformed_data (tuple of dictionaries):
                        A tuple of dictionaries
                        one of which maps actor IDs to coactor IDs,
                        the other maps film IDs to actors in said film
                    n (int) : An integer
            Returns:
                    set(start) (a list converted to  a set): The set of actors that
                    have the nth bacon number
    """
    visited = {4724}
    start = {4724}
    for _ in range(n):
        start = next_level(visited, start, transformed_data)
        if not start:
            break
        visited.update(start)
    return start
    # IF WE HAVE REACHED OUR TARGET, RETURN QUEUE ^^
    # ELSE, ADD THIS NODES CHILDREN TO THE QUEUE


def next_level(visited, target_set, transformed_data):
    """
    Returns a list of actors that have acted with the actors given in "target_list".

            Parameters:
                    transformed_data (tuple of dictionaries):
                        A tuple of dictionariess
                        one of which maps actor IDs to coactor IDs,
                        the other maps film IDs to actors in said film
                    n (int) : An integer
            Returns:
                    new_level (set): The set of actors that have
                    acted with the actors in target list
                    but are not in "visited".
    """
    new_level = set()
    for actor in target_set:
        children = transformed_data[0][actor]
        for child in children:
            if child not in visited:
                new_level.add(child)
    return new_level


def bacon_path(transformed_data, actor_id):
    return actor_path(transformed_data, 4724, lambda x: x == actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    return actor_path(transformed_data, actor_id_1, lambda x: x == actor_id_2)


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Returns an list of actor IDs that form a path from the actor with
    "actor_id_1" to those who satisfy .

            Parameters:
                    transformed_data (tuple of dictionaries):
                        A tuple of dictionariess
                        one of which maps actor IDs to costar IDs,
                        an other maps film IDs to actor ID in said film
                        and a third that maps actor IDs to film IDs
                    actor_id_1 (int) : An integer that represents the
                        ID of this actor
                    goal_test_function (func) : A function that when applied
                        to a group of actors, will return True,
                        used for the BFS implementation
            Returns:
                    path (list): The shortest list of actors from actor_id_1 to any one
                    that fits the goal_test_function.
    """
    visited = set()
    queue = [actor_id_1]  # INITIALISED AT BACON - CAN GENERALISE.
    idmap = {}
    while queue:
        curr = queue.pop(0)
        # visited.add(curr)
        if goal_test_function(curr):
            # INITIALISE MAP BACK
            path = []
            while curr != actor_id_1:
                path.append(curr)
                curr = idmap[curr]
            return [actor_id_1] + path[::-1]
        for neighbour in transformed_data[0][curr]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                idmap[neighbour] = curr


def actors_connecting_films(transformed_data, film1, film2):
    paths = [
        actor_path(transformed_data, x, lambda b: b in transformed_data[2][film2])
        for x in transformed_data[2][film1]
    ]
    return min(paths, key=len) if paths else None


def movie_match(transformed_data, actor_id_1, actor_id_2):
    return transformed_data[1][actor_id_1].intersection(transformed_data[1][actor_id_2])


def movie_path(transformed_data, actor_id_1, actor_id_2):
    pathactor = actor_to_actor_path(transformed_data, actor_id_1, actor_id_2)
    path = []
    for i in range((len(pathactor)) - 1):
        path.extend(movie_match(transformed_data, pathactor[i], pathactor[i + 1]))
    return path


if __name__ == "__main__":
    pass
