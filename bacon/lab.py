#!/usr/bin/env python3

from cgitb import small
import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    #returns a dictionary of actor IDs and a set of coactors
    output = {x[0]:set() for x in raw_data} 
    for item in raw_data:
        try:
            output[item[0]].add(item[1])
        except:
            pass
        try:
            output[item[1]].add(item[0])
        except:
            pass
    return output


def acted_together(transformed_data, actor_id_1, actor_id_2):
    a = transformed_data
    return (actor_id_2 in a[actor_id_1]) or (actor_id_1 in a[actor_id_2]) or (actor_id_1 == actor_id_2)


def actors_with_bacon_number(transformed_data, n):
    a = transformed_data
    output = {4724}
    ever = set()
    for i in range(n):
        dummy = output.copy()
        for item in dummy:
            output.remove(item)
            try:
                output.update(a[item])
            except:
                return set()
            ever.update({item})
        output.difference_update(ever)
        output.discard(4724)
    return output

def bacon_path(transformed_data, actor_id): #doesnt get the shortest path
    ''' attempting to implemenet a breadth first search'''
    a = transformed_data
    if actor_id not in a:
        return None
    parents  = {actor_id:None}
    visited = set()
    queue = [actor_id] #the ones we're checking in the current loop, i.e. our current level of the bfs
    agenda = set()
    path = []
            #the ones that we haven't yet committed to queue, but have encountered by virtue of being neighbours to accessed ones 
    while queue:
        #print('item in queue', queue[-1], 'queue', queue)
        neighbours = a[queue[-1]]
        j = queue.pop()
        visited.add(j)
        #print(f'neighbours for item {j}', neighbours)
        agenda.update(neighbours)
        #print(f'agenda is {agenda}')
        #print(f'visited is {visited}')
        for item in agenda:
            if item not in visited:
                parents.update({item:j}) 
                if item == 4724:
                        parents.update({item:j})    
                        b = True
                        actor = 4724
                        while b:
                            #print(f'adding {actor} to the path')
                            path.append(actor) if actor not in path else b
                            if path[-1] == actor_id:
                                return path
                            #print(a, parents, path)
                            actor = parents[actor]
                            if actor == actor_id:
                                b = False
                                for item in path:
                                    try:
                                        path.append(parents[item]) if parents[item] not in path else b
                                    except KeyError:
                                        path.pop()
                                        return path
                                return path
                else:
                    #print(f'adding {item} to the queue')
                    queue.append(item)
            else:
                continue    
    return None      
                #transform agenda into a thing where it finds the path
def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    ''' attempting to implemenet a breadth first search'''
    a = transformed_data
    if actor_id_2 not in a or actor_id_1 not in a:
        return None
    parents  = {actor_id_1:None}
    visited = set()
    queue = [actor_id_1] #the ones we're checking in the current loop, i.e. our current level of the bfs
    agenda = set()
    path = []
            #the ones that we haven't yet committed to queue, but have encountered by virtue of being neighbours to accessed ones 
    while queue:
        #print('item in queue', queue[-1], 'queue', queue)
        neighbours = a[queue[-1]]
        j = queue.pop()
        visited.add(j)
        #print(f'neighbours for item {j}', neighbours)
        agenda.update(neighbours)
        #print(f'agenda is {agenda}')
        #print(f'visited is {visited}')
        for item in agenda:
            if item not in visited:
                parents.update({item:j})
                if item == actor_id_2:
                        parents.update({item:j})
                        b = True
                        actor = actor_id_2
                        while b:
                            #print(f'adding {actor} to the path')
                            path.append(actor) if actor not in path else b
                            if path[-1] == actor_id_1:
                                return path
                            #print(a, parents, path)
                            actor = parents[actor]
                            if actor == actor_id_1:
                                b = False
                                for item in path:
                                    try:
                                        path.append(parents[item]) if parents[item] not in path else b
                                    except KeyError:
                                        path.pop()
                                        return path
                                return path
                else:
                    #print(f'adding {item} to the queue')
                    queue.append(item) 
            else:
                continue   
    return None   


def actor_path(transformed_data, actor_id_1, goal_test_function):
    raise NotImplementedError("Implement me!")


def actors_connecting_films(transformed_data, film1, film2):
    raise NotImplementedError("Implement me!")


if __name__ == "__main__":
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
    with open("resources/tiny.pickle", 'rb') as g:
        tiny = pickle.load(g) 
    with open("resources/large.pickle", 'rb') as h:
        large = pickle.load(h)
    with open("resources/names.pickle", 'rb') as i:
        names = pickle.load(i)
    a = transform_data(smalldb)
    #print(a[4724])
    x = actors_with_bacon_number(transform_data(large), 6)
    '''b = {x:y for y,x in zip(names.keys(), names.values())}
    #print(b)
    something = set()
    for item in x:
        print()
        something.add(b[item])
    #print(transform_data(large))
    print(bacon_path(transform_data(smalldb), 1640))'''
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    
