import main


option = int(input("Select an option \n1. Conway's Game of Life\n2. Rule x CA\nOption: "))

if option == 1:
    dimensions = int(input("Select a number of cells (for both width and height) (recommended: 100): "))
    gol = main.GOL(dimensions, dimensions)
    gol.game()
elif option == 2:
    iterations = int(input("Select a number of iterations (recommended: 100): "))
    ruleX = main.RuleX(iterations * 2 + 3, iterations)
    rule = int(input("Select a rule: "))
    ruleX.set_rule(rule)
    ruleX.game()

