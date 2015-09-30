from production import IF, AND, OR, NOT, THEN, forward_chain
from data import *

#### Part 1: Multiple Choice #########################################

ANSWER_1 = '2'

ANSWER_2 = 'no'

ANSWER_3 = '2'

ANSWER_4 = '1'

ANSWER_5 = '0'


#### Part 2: Transitive Rule #########################################

transitive_rule = IF( AND('(?x) beats (?y)', '(?y) beats (?z)'),
                      THEN('(?x) beats (?z)') )

# You can test your rule by uncommenting these print statements:
##print forward_chain([transitive_rule], abc_data)
##print forward_chain([transitive_rule], poker_data)
##print forward_chain([transitive_rule], minecraft_data)


#### Part 3: Family Relations #########################################

# Define your rules here:



# Add your rules to this list:
family_rules = (
    IF( AND( 'person (?x)'),
        THEN( 'self (?x) (?x)')),
    
    IF( AND( 'parent (?x) (?y)','parent (?x) (?z)',NOT( 'self (?y) (?z)')),
        THEN( 'sibling (?y) (?z)')),

    IF( AND( 'parent (?x) (?y)'),
        THEN( 'child (?y) (?x)')),

    IF( AND( 'sibling (?x) (?y)', 'parent (?x) (?z)','parent (?y) (?w)'),
        THEN( 'cousin (?z) (?w)')),

    IF( AND( 'parent (?x) (?y)', 'parent (?y) (?z)'),
        THEN( 'grandparent (?x) (?z)')),

    IF( AND( 'grandparent (?x) (?y)'),
        THEN( 'grandchild (?y) (?x)'))
    )

# Uncomment this to test your data on the Simpsons family:
#print forward_chain(family_rules, simpsons_data, verbose=False)

# These smaller datasets might be helpful for debugging:
#print forward_chain(family_rules, sibling_test_data, verbose=True)
#print forward_chain(family_rules, grandparent_test_data, verbose=True)

# The following should generate 14 cousin relationships, representing 7 pairs
# of people who are cousins:
black_family_cousins = [ 
    relation for relation in 
    forward_chain(family_rules, black_data, verbose=False) 
    if "cousin" in relation ]

# To see if you found them all, uncomment this line:
#print black_family_cousins


#### Part 4: Backward Chaining #########################################

# Import additional methods for backchaining
from production import PASS, FAIL, match, populate, simplify, variables

def backchain_to_goal_tree(rules, hypothesis):
    anyMatches = False
    results = OR(hypothesis)
    for rule in rules:
        for statement in rule.consequent():
            matchOutput = match(statement, hypothesis)
            if matchOutput !=None:
                anyMatches = True 
                populatedAnt = populate(rule.antecedent(), matchOutput) #populate antecedent with vocab
                if isinstance(populatedAnt,list):
                    ands = AND()
                    ors = OR()
                    for statement in populatedAnt: #populated Ant is and / or
                        if isinstance(populatedAnt,AND):
                            ands.append(backchain_to_goal_tree(rules,statement))
                        elif isinstance(populatedAnt,OR):
                            ors.append(backchain_to_goal_tree(rules,statement))
                    if len(ands)!=0:
                        results.append(ands)
                    elif len(ors)!=0:
                        results.append(ors)
                else:
                    results.append(backchain_to_goal_tree(rules,populatedAnt))
    if anyMatches == False:
        results.append(OR(hypothesis))
    return simplify(results)
        #output statement as leaf of goal tree
            

# Uncomment this to run your backward chainer:
#print backchain_to_goal_tree(zookeeper_rules, 'opus is a penguin')


#### Survey #########################################

NAME = "Rebecca Corcillo"
COLLABORATORS = "nobody"
HOW_MANY_HOURS_THIS_LAB_TOOK = 7
WHAT_I_FOUND_INTERESTING = "coding rules"
WHAT_I_FOUND_BORING = "bugs"
SUGGESTIONS = None


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

# The following lines are used in the tester. DO NOT CHANGE!
transitive_rule_poker = forward_chain([transitive_rule], poker_data)
transitive_rule_abc = forward_chain([transitive_rule], abc_data)
transitive_rule_minecraft = forward_chain([transitive_rule], minecraft_data)
family_rules_simpsons = forward_chain(family_rules, simpsons_data)
family_rules_black = forward_chain(family_rules, black_data)
family_rules_sibling = forward_chain(family_rules, sibling_test_data)
family_rules_grandparent = forward_chain(family_rules, grandparent_test_data)
family_rules_anonymous_family = forward_chain(family_rules, anonymous_family_test_data)
