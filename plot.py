import main


option = int(input("Select an option \n1. Conway's Game of Life\n2. Rule x CA\n3. Sum x algorithm\n4. Code x "
                   "algorithm\nOption: "))

if option == 1:
    dimensions = int(input("Select a number of cells (for both width and height) (recommended: 100): "))
    gol = main.GOL(dimensions, dimensions)
    gol.game()
elif option == 2:
    iterations = int(input("Select a number of iterations (recommended: 100): "))
    ruleX = main.RuleX(iterations * 2 + 3, iterations)
    rule = int(input("Select a rule: "))
    ruleX.set_rule(rule)
    ruleX.change_time_step(0)
    ruleX.game()
elif option == 3:
    iterations = int(input("Select a number of iterations (recommended: 100): "))
    multX = main.MultX(iterations * 2 + 3, iterations)
    step = int(input("Select a rule: "))
    multX.set_step(step)
    multX.change_time_step(0)
    multX.game()
elif option == 4:
    dimensions = int(input("Select a number of cells (for both width and height) (recommended: 100): "))
    codeX = main.CodeX(dimensions, dimensions)
    rule = int(input("Select a rule: "))
    codeX.set_rule(rule)
    codeX.game()
else:
    print("Option not available")
