import main

dimensions = int(input("Select a number of cells (for both width and height): "))

gol = main.GOL(dimensions, dimensions)
ruleX = main.RuleX(dimensions, dimensions)

option = int(input("Select an option \n1. Conway's Game of Life\n2. Rule x CA\nOption: "))

if option == 1:
    gol.game()
elif option == 2:
    rule = int(input("Select a rule: "))
    ruleX.set_rule(rule)
    ruleX.game()
