from constraint_api import *
from test_problems import get_pokemon_problem

#### PART 1: WRITE A DEPTH-FIRST SEARCH CONSTRAINT SOLVER

def has_empty_domains(csp) :
    "Returns True if the problem has one or more empty domains, otherwise False"
    #raise NotImplementedError
    for var in csp.variables:
        if len(csp.domains[var])==0:
            return True
    return False
    

def check_all_constraints(csp) :
    """Return False if the problem's assigned values violate some constraint,
    otherwise True"""

    for constraint in csp.get_all_constraints():
        assigned1 = csp.get_assigned_value(constraint.var1)
        assigned2 = csp.get_assigned_value(constraint.var2)
        check = constraint.check(assigned1,assigned2)
        if check==False and assigned1!=None and assigned2!=None:
            return False 
    return True

        
def solve_constraint_dfs(problem) :
    """Solves the problem using depth-first search.  Returns a tuple containing:
    1. the solution (a dictionary mapping variables to assigned values), and
    2. the number of extensions made (the number of problems popped off the agenda).
    If no solution was found, return None as the first element of the tuple."""
    q = [problem]
    extCount = 0
    while len(q)!=0:
        removed = q[0]
        q = q[1:]
        extCount+=1
        if has_empty_domains(removed) or check_all_constraints(removed)==False:
            continue
        if len(removed.unassigned_vars)==0:
            return (removed.assigned_values,extCount)
            
        var = removed.pop_next_unassigned_var()
        extensions = []
        for val in removed.get_domain(var):
            csp_new = removed.copy()
            csp_new.set_assigned_value(var,val)
            extensions.append(csp_new)
        
        q = extensions + q
    return (None,extCount)

#### PART 2: DOMAIN REDUCTION BEFORE SEARCH

def eliminate_from_neighbors(csp, var) :
    """Eliminates incompatible values from var's neighbors' domains, modifying
    the original csp.  Returns an alphabetically sorted list of the neighboring
    variables whose domains were reduced, with each variable appearing at most
    once.  If no domains were reduced, returns empty list.
    If a domain is reduced to size 0, quits immediately and returns None."""
    reduced = []
    val = csp.get_assigned_value(var)
    replacement = []
    for constraint in csp.constraints_between(var,None):
        var2 = constraint.var2
        domainCopy = csp.domains[var2][:]
        numLeft = len(domainCopy)
        if (val!=None):
            for i in xrange(len(domainCopy)):
                possibleVal2 = domainCopy[i]
                check = constraint.check(val,possibleVal2)
                if (check==False):
                    didEliminate = csp.eliminate(var2,possibleVal2)
                    if (didEliminate):
                        numLeft-=1
                        if var2 not in reduced:
                            reduced.append(var2)
                    if numLeft==0:
                        return None
    return sorted(reduced)                       
                    

def domain_reduction(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    If queue is None, initializes propagation queue by adding all variables in
    their default order.  Returns a list of all variables that were dequeued,
    in the order they were removed from the queue.  Variables may appear in the
    list multiple times.
    If a domain is reduced to size 0, quits immediately and returns None."""
    if (queue==None):
        queue = csp.get_all_variables()
    dequeued = []
    while len(queue)!=0:
        removedVar = queue[0]
        dequeued.append(removedVar)
        queue = queue[1:]
        for constraint in csp.constraints_between(removedVar,None)[:]:
            var2 = constraint.var2
            val2 = csp.get_assigned_value(var2)
            var2Domain = csp.get_domain(var2)[:]
            removedDomain = csp.get_domain(removedVar)[:]
            if len(removedDomain)==0 or len(var2Domain)==0:
                return None
            for domainVal2 in var2Domain:
                anyNonViolators = False
                for domainVal in removedDomain:
                    check = constraint.check(domainVal,domainVal2)
                    if check==True:
                        anyNonViolators = True
                        continue
                if anyNonViolators==False:
                    csp.eliminate(var2, domainVal2)
                    if len(csp.get_domain(var2))==0:
                        return None
                    if var2 not in queue:
                        queue.append(var2)
    return dequeued
            
            
# QUESTION 1: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DON'T use domain reduction before solving it?

# Hint: Use get_pokemon_problem() to get a new copy of the Pokemon problem
#    each time you want to solve it with a different search method.
csp = get_pokemon_problem()
ANSWER_1 = solve_constraint_dfs(csp)[1]
# QUESTION 2: How many extensions does it take to solve the Pokemon problem
#    with dfs if you DO use domain reduction before solving it?
csp = get_pokemon_problem()
domain_reduction(csp,None)
ANSWER_2 = solve_constraint_dfs(csp)[1]


#### PART 3: PROPAGATION THROUGH REDUCED DOMAINS

def solve_constraint_propagate_reduced_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through all reduced domains.  Same return type as
    solve_constraint_dfs."""
    q = [problem]
    extCount = 0
    while len(q)!=0:
        removed = q[0]
        q = q[1:]
        extCount+=1
        if has_empty_domains(removed) or check_all_constraints(removed)==False:
            continue
        if len(removed.unassigned_vars)==0:
            return (removed.assigned_values,extCount)
            
        var = removed.pop_next_unassigned_var()
        extensions = []
        for val in removed.get_domain(var):
            csp_new = removed.copy()
            csp_new.set_assigned_value(var,val)
            domain_reduction(csp_new,[var])
            extensions.append(csp_new)
        
        q = extensions + q
    return (None,extCount)

# QUESTION 3: How many extensions does it take to solve the Pokemon problem
#    with propagation through reduced domains? (Don't use domain reduction
#    before solving it.)
csp = get_pokemon_problem()
ANSWER_3 = solve_constraint_propagate_reduced_domains(csp)[1]



#### PART 4: PROPAGATION THROUGH SINGLETON DOMAINS

def domain_reduction_singleton_domains(csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Only propagates through singleton domains.
    Same return type as domain_reduction."""
    if (queue==None):
        queue = csp.get_all_variables()
    dequeued = []
    while len(queue)!=0:
        removedVar = queue[0]
        dequeued.append(removedVar)
        queue = queue[1:]
        for constraint in csp.constraints_between(removedVar,None)[:]:
            var2 = constraint.var2
            val2 = csp.get_assigned_value(var2)
            var2Domain = csp.get_domain(var2)[:]
            removedDomain = csp.get_domain(removedVar)[:]
            if len(removedDomain)==0 or len(var2Domain)==0:
                return None
            for domainVal2 in var2Domain:
                anyNonViolators = False
                for domainVal in removedDomain:
                    check = constraint.check(domainVal,domainVal2)
                    if check==True:
                        anyNonViolators = True
                        continue
                if anyNonViolators==False:
                    csp.eliminate(var2, domainVal2)
                    if len(csp.get_domain(var2))==0:
                        return None
                    if var2 not in queue and len(csp.get_domain(var2))==1:
                        queue.append(var2)
    return dequeued

def solve_constraint_propagate_singleton_domains(problem) :
    """Solves the problem using depth-first search with forward checking and
    propagation through singleton domains.  Same return type as
    solve_constraint_dfs."""
    q = [problem]
    extCount = 0
    while len(q)!=0:
        removed = q[0]
        q = q[1:]
        extCount+=1
        if has_empty_domains(removed) or check_all_constraints(removed)==False:
            continue
        if len(removed.unassigned_vars)==0:
            return (removed.assigned_values,extCount)
            
        var = removed.pop_next_unassigned_var()
        extensions = []
        for val in removed.get_domain(var):
            csp_new = removed.copy()
            csp_new.set_assigned_value(var,val)
            domain_reduction_singleton_domains(csp_new,[var])
            extensions.append(csp_new)
        
        q = extensions + q
    return (None,extCount)

# QUESTION 4: How many extensions does it take to solve the Pokemon problem
#    with propagation through singleton domains? (Don't use domain reduction
#    before solving it.)
csp = get_pokemon_problem()
ANSWER_4 = solve_constraint_propagate_singleton_domains(csp)[1]


#### PART 5: FORWARD CHECKING

def propagate(enqueue_condition_fn, csp, queue=None) :
    """Uses constraints to reduce domains, modifying the original csp.
    Uses enqueue_condition_fn to determine whether to enqueue a variable whose
    domain has been reduced.  Same return type as domain_reduction."""
    if (queue==None):
        queue = csp.get_all_variables()
    dequeued = []
    while len(queue)!=0:
        removedVar = queue[0]
        dequeued.append(removedVar)
        queue = queue[1:]
        for constraint in csp.constraints_between(removedVar,None)[:]:
            var2 = constraint.var2
            val2 = csp.get_assigned_value(var2)
            var2Domain = csp.get_domain(var2)[:]
            removedDomain = csp.get_domain(removedVar)[:]
            if len(removedDomain)==0 or len(var2Domain)==0:
                return None
            for domainVal2 in var2Domain:
                anyNonViolators = False
                for domainVal in removedDomain:
                    check = constraint.check(domainVal,domainVal2)
                    if check==True:
                        anyNonViolators = True
                        continue
                if anyNonViolators==False:
                    csp.eliminate(var2, domainVal2)
                    if len(csp.get_domain(var2))==0:
                        return None
                    if var2 not in queue and enqueue_condition_fn(csp,var2):
                        queue.append(var2)
    return dequeued

def condition_domain_reduction(csp, var) :
    """Returns True if var should be enqueued under the all-reduced-domains
    condition, otherwise False"""
    return True

def condition_singleton(csp, var) :
    """Returns True if var should be enqueued under the singleton-domains
    condition, otherwise False"""
    return len(csp.get_domain(var))==1

def condition_forward_checking(csp, var) :
    """Returns True if var should be enqueued under the forward-checking
    condition, otherwise False"""
    return False


#### PART 6: GENERIC CSP SOLVER

def solve_constraint_generic(problem, enqueue_condition=None) :
    """Solves the problem, calling propagate with the specified enqueue
    condition (a function).  If enqueue_condition is None, uses DFS only.
    Same return type as solve_constraint_dfs."""
    q = [problem]
    extCount = 0
    while len(q)!=0:
        removed = q[0]
        q = q[1:]
        extCount+=1
        if has_empty_domains(removed) or check_all_constraints(removed)==False:
            continue
        if len(removed.unassigned_vars)==0:
            return (removed.assigned_values,extCount)
            
        var = removed.pop_next_unassigned_var()
        extensions = []
        for val in removed.get_domain(var):
            csp_new = removed.copy()
            csp_new.set_assigned_value(var,val)
            if (enqueue_condition!=None):
                propagate(enqueue_condition,csp_new,[var])
            extensions.append(csp_new)
        
        q = extensions + q
    return (None,extCount)

# QUESTION 5: How many extensions does it take to solve the Pokemon problem
#    with DFS and forward checking, but no propagation? (Don't use domain
#    reduction before solving it.)
csp = get_pokemon_problem()

ANSWER_5 = solve_constraint_generic(csp, condition_forward_checking)[1]


#### PART 7: DEFINING CUSTOM CONSTRAINTS

def constraint_adjacent(m, n) :
    """Returns True if m and n are adjacent, otherwise False.
    Assume m and n are ints."""
    return abs(m-n)==1

def constraint_not_adjacent(m, n) :
    """Returns True if m and n are NOT adjacent, otherwise False.
    Assume m and n are ints."""
    return not constraint_adjacent(m,n)

def all_different(variables) :
    """Returns a list of constraints, with one difference constraint between
    each pair of variables."""
    constraints = []
    for i in xrange(len(variables)):
        var1 = variables[i]
        for j in xrange(i+1,len(variables)):
            var2 = variables[j]
            if var1!=var2:
                constraints.append(Constraint(var1,var2,constraint_different))
    return constraints
                


#### PART 8: MOOSE PROBLEM (OPTIONAL)

moose_problem = ConstraintSatisfactionProblem(["You", "Moose", "McCain",
                                               "Palin", "Obama", "Biden"])

# Add domains and constraints to your moose_problem here:


# To test your moose_problem AFTER implementing all the solve_constraint
# methods above, change TEST_MOOSE_PROBLEM to True:
TEST_MOOSE_PROBLEM = False


#### SURVEY ###################################################

NAME = "Rebecca Corcillo"
COLLABORATORS = "Nobody"
HOW_MANY_HOURS_THIS_LAB_TOOK = "10"
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""
SUGGESTIONS = ""


###########################################################
### Ignore everything below this line; for testing only ###
###########################################################

if TEST_MOOSE_PROBLEM:
    # These lines are used in the local tester iff TEST_MOOSE_PROBLEM is True
    moose_answer_dfs = solve_constraint_dfs(moose_problem.copy())
    moose_answer_propany = solve_constraint_propagate_reduced_domains(moose_problem.copy())
    moose_answer_prop1 = solve_constraint_propagate_singleton_domains(moose_problem.copy())
    moose_answer_generic_dfs = solve_constraint_generic(moose_problem.copy(), None)
    moose_answer_generic_propany = solve_constraint_generic(moose_problem.copy(), condition_domain_reduction)
    moose_answer_generic_prop1 = solve_constraint_generic(moose_problem.copy(), condition_singleton)
    moose_answer_generic_fc = solve_constraint_generic(moose_problem.copy(), condition_forward_checking)
    moose_instance_for_domain_reduction = moose_problem.copy()
    moose_answer_domain_reduction = domain_reduction(moose_instance_for_domain_reduction)
    moose_instance_for_domain_reduction_singleton = moose_problem.copy()
    moose_answer_domain_reduction_singleton = domain_reduction_singleton_domains(moose_instance_for_domain_reduction_singleton)
