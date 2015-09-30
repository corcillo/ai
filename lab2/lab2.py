from search import Edge, UndirectedGraph, do_nothing_fn, make_generic_search
import read_graphs
from sets import Set
all_graphs = read_graphs.get_graphs()
GRAPH_0 = all_graphs['GRAPH_0']
GRAPH_1 = all_graphs['GRAPH_1']
GRAPH_2 = all_graphs['GRAPH_2']
GRAPH_3 = all_graphs['GRAPH_3']
GRAPH_FOR_HEURISTICS = all_graphs['GRAPH_FOR_HEURISTICS']

#Change this to True if you want to run additional local tests for debugging:
RUN_ADDITIONAL_TESTS = False

#### PART 1: Helper Functions #########################################

def path_length(graph, path):
    if len(path)==1:
        return 0
    length = 0
    for i in xrange(len(path)-1):
        length+=graph.get_edge(path[i],path[i+1]).length
    return length

def has_loops(path):
    nodeToFreq = {}
    for node in path:
        if nodeToFreq.get(node)!=None:
            return True
        nodeToFreq[node]=1
    return False


def extensions(graph, path):
    neighbors = graph.get_neighbors(path[-1])
    return [path+[neighbor] for neighbor in neighbors if neighbor not in path]


def sort_by_heuristic(graph, goalNode, nodes):
    nodes = sorted(nodes)
    return sorted(nodes,None,lambda n: graph.get_heuristic_value(n,goalNode))


# You can ignore the following line.  It allows generic_search (PART 3) to 
# access the extensions and has_loops functions that you defined in PART 1.
generic_search = make_generic_search(extensions, has_loops)  # DO NOT CHANGE

#### PART 2: Search Algorithms #########################################

# Note: Optionally, you may skip to Part 3: Generic Search,
# then complete Part 2 using your answers from Part 3.

def dfs(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        removed = q[0]
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        extendedPaths = sorted(extendedPaths,None, lambda p: p[-1])
        nonLoopPaths = [path for path in extendedPaths if has_loops(path) is False]
        q = nonLoopPaths + q
    return None
##    my_dfs_fn = generic_search(*generic_dfs)
##    return my_dfs_fn(graph, startNode, goalNode)
##        

def bfs(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        removed = q[0]
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        extendedPaths = sorted(extendedPaths,None, lambda p: p[-1])
        nonLoopPaths = [path for path in extendedPaths if has_loops(path) is False]
        q = q + nonLoopPaths
    return None
##    my_bfs_fn = generic_search(*generic_bfs)
##    return my_bfs_fn(graph, startNode, goalNode)
##        

def hill_climbing(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        removed = q[0]
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        extendedPaths = sorted(extendedPaths,None,lambda p: graph.get_heuristic_value(p[-1],goalNode))
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False:
                if path[-1]==goalNode:
                    return path
                nonLoopPaths.append(path)
        q = nonLoopPaths + q
    return None


def best_first(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        q = sorted(q,cmp = lambda p1,p2: heurComparator(graph,goalNode,p1,p2))
        removed = q[0]
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False:
                nonLoopPaths.append(path)
        q = nonLoopPaths + q
    return None


def beam(graph, startNode, goalNode, beam_width):
    q = {0:[[startNode]]}
    level = 0
    while len(q[level])!=0:
        removed = q[level][0]
        q[level] = q[level][1:]
        if removed[-1]==goalNode:
            return removed
        
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = [path for path in extendedPaths if has_loops(path) is False]
                
        insertLevel = level+1
        if insertLevel in q.keys():
            q[insertLevel]= q[insertLevel]+nonLoopPaths
        else:
            q[insertLevel] = nonLoopPaths

        q[insertLevel]=newHSort(graph,goalNode,q[insertLevel])
 #       q[insertLevel] = sorted(q[insertLevel],cmp = lambda p1,p2: heurComparator(graph,goalNode,p1,p2))
        keepNum = min(beam_width, len(q[insertLevel]))
        q[insertLevel] = q[insertLevel][0:keepNum]

        if len(q[level])==0:
            level+=1
            
    return None



def branch_and_bound(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        q = sorted(q,None,lambda p: path_length(graph,p))
        removed = q[0]
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False:
                nonLoopPaths.append(path)
        q = q + nonLoopPaths
    return None


def branch_and_bound_with_heuristic(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        q = sorted(q,None,lambda p: path_length(graph,p)+graph.get_heuristic_value(p[-1],goalNode))
        removed = q[0]
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False:
                nonLoopPaths.append(path)
        q = q + nonLoopPaths
    return None


def branch_and_bound_with_extended_set(graph, startNode, goalNode):
    q = [[startNode]]
    extendedSet = Set([])
    while len(q)!=0:
        q = sorted(q,None,lambda p: path_length(graph,p))
        removed = q[0]
        extendedSet.add(removed[-1])
        if removed[-1]==goalNode:
            return removed
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False and path[-1] not in extendedSet:
                nonLoopPaths.append(path)
        q = q + nonLoopPaths
    return None

def a_star(graph, startNode, goalNode):
    q = [[startNode]]
    while len(q)!=0:
        q = sorted(q,lambda path1,path2: cmp(path_length(graph,path1)+graph.get_heuristic_value(path1[-1],goalNode),path_length(graph,path2)+graph.get_heuristic_value(path2[-1],goalNode)))
        #q = sorted(q,lambda p: path_length(graph,p)+graph.get_heuristic_value(p[-1],goalNode))

        removed = q[0]
        q = q[1:]
        extendedPaths = extensions(graph,removed)
        nonLoopPaths = []
        for path in extendedPaths:
            if has_loops(path) is False:
                if path[-1]==goalNode:
                    return path
                nonLoopPaths.append(path)
        q = q + nonLoopPaths
    return None


#### PART 3: Generic Search #######################################

# Define your custom path-sorting functions here.  
# Each path-sorting function should be in this form:

# def my_sorting_fn(graph, goalNode, paths):
#     # YOUR CODE HERE
#     return sorted_paths
def lengthComparator(graph, goalNode, p1, p2):
    p1Len = path_length(graph,p1)
    p2Len = path_length(graph,p2)
    p1Elt = p1[-1]
    p2Elt = p2[-1]
    if p1Len < p2Len:
        return -1
    elif p1Len > p2Len:
        return 1
    else:
        if p1Elt < p2Elt:
            return -1
        elif p1Elt > p2Elt:
            return 1
        else:
            return 0

def heurComparator(graph, goalNode, p1, p2):
    p1Elt = p1[-1]
    p2Elt = p2[-1]
    p1H = graph.get_heuristic_value(p1Elt,goalNode)
    p2H = graph.get_heuristic_value(p2Elt,goalNode)
    if p1H < p2H:
        return -1
    elif p1H > p2H:
        return 1
    else:
        if p1Elt < p2Elt:
            return -1
        elif p1Elt > p2Elt:
            return 1
        else:
            return -1
        
def bothComparator(graph, goalNode, p1, p2):
    p1Elt = p1[-1]
    p2Elt = p2[-1]
    p1H = graph.get_heuristic_value(p1Elt,goalNode) + path_length(graph,p1)
    p2H = graph.get_heuristic_value(p2Elt,goalNode) + path_length(graph,p2)
    if p1H < p2H:
        return -1
    elif p1H > p2H:
        return 1
    else:
        if p1Elt < p2Elt:
            return 1
        elif p1Elt > p2Elt:
            return -1
        else:
            return 0
                                   
                  
def no_sorting_fn(graph, goalNode, paths):
    return paths
def no_sorting(graph, goalNode, agenda):
    return agenda
def sort_paths_by_heuristic(graph, goalNode, paths):
    return sorted(paths,cmp = lambda p1,p2: heurComparator(graph,goalNode,p1,p2))
def sort_by_length(graph,goalNode,agenda):
    return sorted(agenda, cmp = lambda p1,p2: lengthComparator(graph,goalNode,p1,p2))
def sort_by_length_and_heuristic(graph,goalNode,agenda):
    return sorted(agenda,cmp = lambda p1,p2: bothComparator(graph,goalNode,p1,p2))
def newHSort(graph,goalNode,paths):
    paths = sorted(paths)
    return sorted(paths,key = lambda x : graph.get_heuristic_value(x[-1],goalNode))

generic_dfs = [no_sorting_fn, True, no_sorting, False]#good

generic_bfs = [no_sorting_fn, False, no_sorting, False] #good

generic_hill_climbing = [sort_paths_by_heuristic, True, no_sorting, False] 

#sort_new_paths_fn, add_paths_to_front_of_agenda, sort_agenda_fn, use_extended_set)

#WRONG agenda fn
generic_best_first = [no_sorting_fn, True, newHSort, False]

#WRONG agenda fn
generic_branch_and_bound = [no_sorting_fn, False, sort_by_length, False]

generic_branch_and_bound_with_heuristic = [no_sorting_fn, False, sort_by_length_and_heuristic, False]

#WRONG agenda fn
generic_branch_and_bound_with_extended_set = [no_sorting_fn, False, sort_by_length, True]

generic_a_star = [no_sorting_fn, False, sort_by_length_and_heuristic, True]

# Here is an example of how to call generic_search (uncomment to run):
#my_dfs_fn = generic_search(*generic_dfs)
#my_dfs_path = my_dfs_fn(GRAPH_2, 'S', 'G')
#print my_dfs_path

# Or, combining the first two steps:
#my_dfs_path = generic_search(*generic_dfs)(GRAPH_2, 'S', 'G')
#print my_dfs_path


### OPTIONAL: Generic Beam Search
# If you want to run local tests for generic_beam, change TEST_GENERIC_BEAM to True:
TEST_GENERIC_BEAM = False

# The sort_agenda_fn for beam search takes fourth argument, beam_width:
# def my_beam_sorting_fn(graph, goalNode, paths, beam_width):
#     # YOUR CODE HERE
#     return sorted_beam_agenda

generic_beam = [None, None, None, None]

# Uncomment this to test your generic_beam search:
#print generic_search(*generic_beam)(GRAPH_2, 'S', 'G', beam_width=2)


#### PART 4: Heuristics ###################################################

def is_admissible(graph, goalNode):
    for node in graph.nodes:
        shortestPath = bfs(graph,node,goalNode)
        shortestPathLength = path_length(graph,shortestPath)
        if graph.get_heuristic_value(node,goalNode) > shortestPathLength:
            return False
    return True


def is_consistent(graph, goalNode):
    for edge in graph.edges:
        if edge.length < abs(graph.get_heuristic_value(edge.startNode,goalNode)-graph.get_heuristic_value(edge.endNode, goalNode)):
            return False
    return True


### OPTIONAL: Picking Heuristics
# If you want to run local tests on your heuristics, change TEST_HEURISTICS to True:
TEST_HEURISTICS = False

# heuristic_1: admissible and consistent

[h1_S, h1_A, h1_B, h1_C, h1_G] = [None, None, None, None, None]

heuristic_1 = {'G': {}}
heuristic_1['G']['S'] = h1_S
heuristic_1['G']['A'] = h1_A
heuristic_1['G']['B'] = h1_B
heuristic_1['G']['C'] = h1_C
heuristic_1['G']['G'] = h1_G


# heuristic_2: admissible but NOT consistent

[h2_S, h2_A, h2_B, h2_C, h2_G] = [None, None, None, None, None]

heuristic_2 = {'G': {}}
heuristic_2['G']['S'] = h2_S
heuristic_2['G']['A'] = h2_A
heuristic_2['G']['B'] = h2_B
heuristic_2['G']['C'] = h2_C
heuristic_2['G']['G'] = h2_G


# heuristic_3: admissible but A* returns non-optimal path to G

[h3_S, h3_A, h3_B, h3_C, h3_G] = [None, None, None, None, None]

heuristic_3 = {'G': {}}
heuristic_3['G']['S'] = h3_S
heuristic_3['G']['A'] = h3_A
heuristic_3['G']['B'] = h3_B
heuristic_3['G']['C'] = h3_C
heuristic_3['G']['G'] = h3_G


# heuristic_4: admissible but not consistent, yet A* finds optimal path

[h4_S, h4_A, h4_B, h4_C, h4_G] = [None, None, None, None, None]

heuristic_4 = {'G': {}}
heuristic_4['G']['S'] = h4_S
heuristic_4['G']['A'] = h4_A
heuristic_4['G']['B'] = h4_B
heuristic_4['G']['C'] = h4_C
heuristic_4['G']['G'] = h4_G


#### SURVEY ###################################################

NAME = "Rebecca Corcillo"
COLLABORATORS = "nobody"
HOW_MANY_HOURS_THIS_LAB_TOOK = 10
WHAT_I_FOUND_INTERESTING = "remembering search and coding it"
WHAT_I_FOUND_BORING = "debugging"
SUGGESTIONS = "be more clear with what we should return/ return if we dont find a path"

# Patch for lab2.py  
# Paste the following lines into the bottom of your lab2.py:

generic_dfs_sort_new_paths_fn = generic_dfs[0]
generic_bfs_sort_new_paths_fn = generic_bfs[0]
generic_hill_climbing_sort_new_paths_fn = generic_hill_climbing[0]
generic_best_first_sort_new_paths_fn = generic_best_first[0]
generic_branch_and_bound_sort_new_paths_fn = generic_branch_and_bound[0]
generic_branch_and_bound_with_heuristic_sort_new_paths_fn = generic_branch_and_bound_with_heuristic[0]
generic_branch_and_bound_with_extended_set_sort_new_paths_fn = generic_branch_and_bound_with_extended_set[0]
generic_a_star_sort_new_paths_fn = generic_a_star[0]

generic_dfs_sort_agenda_fn = generic_dfs[2]
generic_bfs_sort_agenda_fn = generic_bfs[2]
generic_hill_climbing_sort_agenda_fn = generic_hill_climbing[2]
generic_best_first_sort_agenda_fn = generic_best_first[2]
generic_branch_and_bound_sort_agenda_fn = generic_branch_and_bound[2]
generic_branch_and_bound_with_heuristic_sort_agenda_fn = generic_branch_and_bound_with_heuristic[2]
generic_branch_and_bound_with_extended_set_sort_agenda_fn = generic_branch_and_bound_with_extended_set[2]
generic_a_star_sort_agenda_fn = generic_a_star[2]
