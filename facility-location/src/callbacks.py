from data import Data
from gurobipy import GRB, quicksum

class Callback:
    """
    Callback class for implementing Benders' decomposition optimality cuts in the
    Capacitated Facility Location Problem (CFLP) with a new cut generation mechanism.
    """

    def __init__(self, dat: Data, y, eta):
        """
        Initialize the Callback object.

        Args:
            dat (Data): The data object containing problem data.
            y (Var): The location variables.
            eta (Var): The cost variable.
        """

        self.dat = dat
        self.y = y
        self.eta = eta
        self.num_cuts = 0  # number of optimality cuts added

    def __call__(self, mod, where):
        """
        Callback entry point: call lazy constraints routine when new
        solutions are found.

        Args:
            mod (Model): The Gurobi model object.
            where (int): The callback event code.

        Returns:
            None
        """

        # Check if an integer feasible solution has been found
        if where == GRB.Callback.MIPSOL:
            # Get the current solution
            y_values = mod.cbGetSolution(self.y)

            # Generate and add the optimality cut
            self.add_optimality_cut(mod, y_values)

    def add_optimality_cut(self, mod, y_values):
        """
        Add the new optimality cut to the model as a lazy constraint.

        Args:
            mod (Model): The Gurobi model to which the optimality cut is added.
            y_values (list): The solution values of the location variables.

        Returns:
            None
        """

        # Initialize the right-hand side for the cut
        rhs = 0

        # Loop over all customers
        for i in self.dat.I:
            # Sort costs for customer i
            sorted_costs = sorted((self.dat.costs[i][j], j) for j in self.dat.J)
            
            # Determine the critical item k_i for the given y_values
            cumulative_y = 0
            k_i = None
            for cost, j in sorted_costs:
                cumulative_y += y_values[j]
                if cumulative_y >= 1:
                    k_i = j
                    break

            # Since k_i is always found, calculate the contribution of customer i to the cut
            c_k_i = self.dat.costs[i][k_i]
            contribution = c_k_i
            for cost, j in sorted_costs:
                if j < k_i:
                    contribution -= (c_k_i - self.dat.costs[i][j]) * y_values[j]
            rhs += contribution

        # Add the cut as a lazy constraint
        mod.cbLazy(self.eta >= rhs)
        self.num_cuts += 1
