from classify import *
import math

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
##    # this is not the right solution!
##    return hamming_distance(list1, list2)
    sum = 0
    for i in xrange(len(list1)):
        sum+=(list1[i]-list2[i])**2
    return sum**(.5)

#Once you have implemented euclidean_distance, you can check the results:
evaluate(nearest_neighbors(euclidean_distance, 2), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 3)
evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
##print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.
import math
def information_disorder(yes, no):
    nt = len(yes)+len(no)
    yesTypeCount = {}
    noTypeCount = {}
    for thing in yes:
        if yesTypeCount.get(thing)==None:
            yesTypeCount[thing] = 1
        else:
            yesTypeCount[thing]+=1
    for thing in no:
        if noTypeCount.get(thing)==None:
            noTypeCount[thing]=1
        else:
            noTypeCount[thing]+=1
    yesDisorder = 0
    nb = 1.0*len(yes)
    for cType in yesTypeCount.keys():
        nbc = 1.0*yesTypeCount[cType]
        yesDisorder+= -1.0*(nbc/nb)*math.log(nbc/nb,2)
    yesDisorder*=(nb/nt)

    noDisorder = 0
    nb = 1.0*len(no)
    for cType in noTypeCount.keys():
        nbc = 1.0 * noTypeCount[cType]
        noDisorder+= -1.0 * (nbc/nb)*math.log(nbc/nb,2)
    noDisorder*=(nb/nt)
    return yesDisorder+noDisorder

    
##print CongressIDTree(senate_people, senate_votes, information_disorder)
##evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

def binarySearchWithN(people,votes,desiredRight):
    minN = 0
    maxN = 100
    mid = (minN+maxN)/2
    correct = limited_house_classifier(people, votes,mid)
    deltaN = 2  
    while correct < desiredRight - deltaN or  correct > desiredRight + deltaN :
        correct = limited_house_classifier(people, votes,mid)
        if correct < desiredRight - deltaN:
            minN = mid
        elif correct > desiredRight + deltaN:
            maxN = mid
        else:
            return mid
        mid = (minN+maxN)/2
    return mid

binarySearchWithN(house_people, house_votes, 430)            
            
        

## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = binarySearchWithN(house_people, house_votes,430)
print "n1= ", N_1
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
print "rep classified = " , rep_classified

## Find a value of n that classifies at least 90 senators correctly.
subtract = 1
goal = 90
N_2 = binarySearchWithN(senate_people, senate_votes,90)
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
while senator_classified>goal:
    N_2 -=1
    senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
    print "got: ",senator_classified, "with: ",N_2
N_2+=3
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)

print "n2= ", N_2, " classified ",senator_classified

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = binarySearchWithN(last_senate_people, last_senate_votes,90)+1
print "n3= ", N_3
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)


## The standard survey questions.
NAME = "Rebecca"
COLLABORATORS = "noone"
HOW_MANY_HOURS_THIS_LAB_TOOK = "10"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""


## This function is used by the tester; please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn
