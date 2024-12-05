rules = []
updates = []
section = 1
with open("input", "r") as f:
    for line in f.readlines():
        if section == 1:
            if len(line) == 1:
                section = 2
            else:
                rules.append(list(map(int, line.split("|"))))
        elif section == 2:
            updates.append(list(map(int, line.split(","))))

def existsInList(x, list):
   for l in list:
      if (l == x):
         return True;
   return False;

def existsBeforeInList(x, list, index):
    if (index > len(list)):
       index = len(list)
    for targetSearchIndex in range(0, index):
        if (list[targetSearchIndex] == x):
            return True
    return False

def existsAfterInList(x, list, index):
    if (index < 0):
       index = 0;
    for searchIndex in range (index, len(list)):
        if (list[searchIndex] == x):
           return True
    return False

def middleNumber(list):
    return list[len(list) // 2]

def swap(a, b, list):
   t = list.index(a)
   ta = list[list.index(a)]
   u = list.index(b)
   list[t] = list[list.index(b)]
   list[u] = ta

def correctlyOrderedList(list):
    for pageIndex in range(0, len(list)):
        neededPage = list[pageIndex]
        for ruleIndex in range(0, len(rules)):
            if rules[ruleIndex][0] == neededPage:
                targetPage = rules[ruleIndex][1]
                if not existsInList(targetPage, list):
                   continue

                if existsBeforeInList(targetPage, list, pageIndex):
                    return False

                if existsAfterInList(targetPage, list, pageIndex+1):
                    for targetRuleIndex in range(0, len(rules)):
                        if (rules[targetRuleIndex][0] == targetPage):
                            ruleTargetPage = rules[targetRuleIndex][1]
                            if (existsBeforeInList(ruleTargetPage, list, pageIndex)):
                                return False
    return True 

total = 0
for u in updates:
    incorrect = not correctlyOrderedList(u)

    for pageIndex in range(0, len(u)):
        neededPage = u[pageIndex]
        for ruleIndex in range(0, len(rules)):
            if rules[ruleIndex][0] == neededPage:
                targetPage = rules[ruleIndex][1]

                # If the target of the rule isn't in the list, we don't care
                if not existsInList(targetPage, u):
                   continue

                # if the target of the rule is before the source of the rule, it's incorrect
                if existsBeforeInList(targetPage, u, pageIndex):
                   incorrect = True

                # if the target of the rule is after the source, we need to check its rules
                if existsAfterInList(targetPage, u, pageIndex+1):
                   for targetRuleIndex in range(0, len(rules)):
                       if (rules[targetRuleIndex][0] == targetPage):
                           ruleTargetPage = rules[targetRuleIndex][1]
                           # If the target of the rule is before the source, its incorrect
                           if (existsBeforeInList(ruleTargetPage, u, pageIndex)):
                               incorrect = True 

    # only count the middle number if the list is correctly ordered
    if (not incorrect):
        total += middleNumber(u)

print(f"Part 1 Total {total}")


# Part 2
total = 0
for u in updates:
    # Check the trivial case where the list is already correctly ordered
    incorrect = not correctlyOrderedList(u)
    if not incorrect:
       continue

    # Keep going until it is correctly ordered (assumes no conflict in the ruleset)
    while (incorrect):
        for pageIndex in range(0, len(u)):
            neededPage = u[pageIndex]
            for ruleIndex in range(0, len(rules)):
                if rules[ruleIndex][0] == neededPage:
                    targetPage = rules[ruleIndex][1]

                    # if the target of the rule isn't in the list, we don't care
                    if not existsInList(targetPage, u):
                       continue

                    # If the rule says its incorrect order, swap target and source of the rule
                    if existsBeforeInList(targetPage, u, pageIndex):
                        swap(targetPage, neededPage, u)

                    if existsAfterInList(targetPage, u, pageIndex+1):
                        for targetRuleIndex in range(0, len(rules)):
                            if (rules[targetRuleIndex][0] == targetPage):
                                ruleTargetPage = rules[targetRuleIndex][1]

                                # If the rule says its incorrect order, swap target and source of the rule
                                if (existsBeforeInList(ruleTargetPage, u, pageIndex)):
                                    swap(ruleTargetPage, targetPage, u)
        incorrect = not correctlyOrderedList(u)

    total += middleNumber(u)

print(f"Part 2 Total {total}")
