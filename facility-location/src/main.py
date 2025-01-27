from data import generate_random_instance
from master_problem import solve_CFLP

if __name__ == "__main__":
    # Generate a random instance with 100 customers and 10 facilities
    data = generate_random_instance(num_customers=400, num_facilities=200)

    # Solve the Capacitated Facility Location Problem (CFLP) model and obtain the optimal solution
    solution = solve_CFLP(data)

    # Print solution information
    print("Objective value:    ", solution.objective_value)
    print("Open facilities:    ", [j for j in data.J if solution.locations[j] > 0.5])
    print("Solution time (sec):", solution.solution_time)
    print("Number of optimality cuts generated:", solution.num_cuts)
    # Print generated data values
    #print("\nGenerated Data:")
    #print("Demands:")
    #print(data.demands)
    #print("Capacities:")
    #print(data.capacities)
    #print("Fixed Costs:")
    #print(data.fixed_costs)
    #print("Shipment Costs:")
    #print(data.shipment_costs)