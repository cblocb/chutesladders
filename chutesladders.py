import numpy as np

def monte_carlo_simulation(P, num_trials=200000):
    total_turns = []
    
    for _ in range(num_trials):
        current_state = 0
        turns = 0
        while current_state != 100:
            turns += 1
            probs = P[current_state]
            current_state = np.random.choice(len(probs), p=probs)
        total_turns.append(turns)
        
    return np.array(total_turns)

def analytical_solution(P):
    Q = P[:100, :100]
    A = np.eye(100) - Q
    b = np.ones(100)
    E = np.linalg.solve(A, b)
    return E


if __name__ == "__main__":
    import os
    # Ensure we look for the matrix in the same folder as this script, 
    # regardless of where the script is run from.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "transition_matrix.csv")
    
    try:
        P = np.loadtxt(csv_path, delimiter=",")
    except FileNotFoundError:
        # Fallback if csv is in quant/ relative to running dir (legacy)
        P = np.loadtxt("quant/transition_matrix.csv", delimiter=",")

    row_sums = P.sum(axis=1)
    row_sums[row_sums == 0] = 1.0
    P = P / row_sums[:, np.newaxis]
    
    mc_results = monte_carlo_simulation(P)
    
    print(f"Monte Carlo Expected Turns From Start: {mc_results.mean():.4f}")
    print(f"Monte Carlo Std Dev: {mc_results.std():.4f}")
    print(f"Monte Carlo Variance: {mc_results.var():.4f}")
    
    analytical = analytical_solution(P)
    print(f"Analytical Expected Turns From Start: {analytical[0]:.4f}")
    
    print(f"Difference: {abs(mc_results.mean() - analytical[0]):.4f}")

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.hist(mc_results, bins=50, color='skyblue', edgecolor='black')
    plt.title('Game Length Distribution (Chutes and Ladders)')
    plt.xlabel('Turns')
    plt.ylabel('Frequency')
    plt.savefig('game_lengths.png')
    print("Distribution graph saved to 'game_lengths.png'")


