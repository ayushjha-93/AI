class MeansEndAnalysis:
    def __init__(self, operators):
        self.operators = operators

    def solve(self, current, goal):
        print(f"Current state: {current}, Goal state: {goal}")

        # Goal achieved
        if self.goal_reached(current, goal):
            return []

        # Find the first difference
        diff = self.find_difference(current, goal)
        if diff is None:
            return []

        # Select an operator
        op = self.select_operator(diff)
        if op is None:
            print(f"No operator found for difference: {diff}")
            return None

        # Satisfy preconditions
        pre_path = self.solve(current.copy(), op["preconditions"])
        if pre_path is None:
            return None

        # Apply operator
        new_state = current.copy()
        new_state.update(op["effect"])

        # Continue towards goal
        remaining_path = self.solve(new_state, goal)
        if remaining_path is None:
            return None

        return pre_path + [op["name"]] + remaining_path

    def goal_reached(self, current, goal):
        for key, value in goal.items():
            if current.get(key) != value:
                return False
        return True

    def find_difference(self, current, goal):
        for key, value in goal.items():
            if current.get(key) != value:
                return (key, value)
        return None

    def select_operator(self, diff):
        key, value = diff
        for op in self.operators:
            if op["effect"].get(key) == value:
                return op
        return None


# ---------------- Example ----------------

if __name__ == "__main__":

    operators = [
        {
            "name": "Buy_car",
            "preconditions": {
                "has_money": True,
                "has_car": False
            },
            "effect": {
                "has_car": True
            }
        },
        {
            "name": "Drive_car",
            "preconditions": {
                "has_car": True,
                "at_home": True
            },
            "effect": {
                "at_work": True,
                "at_home": False
            }
        }
    ]

    current_state = {
        "has_money": True,
        "has_car": False,
        "at_home": True,
        "at_work": False
    }

    goal_state = {
        "at_work": True
    }

    mea = MeansEndAnalysis(operators)
    plan = mea.solve(current_state, goal_state)

    print("\nExecution Plan:", plan)