import numpy as np
import itertools

def build_matrix_3d4():
    # Calculate 3d4 distribution
    # Rolls: 3 dice, each 1-4
    combinations = list(itertools.product(range(1, 5), repeat=3))
    sums = [sum(combo) for combo in combinations]
    
    # Map sum to count
    counts = {}
    for s in sums:
        counts[s] = counts.get(s, 0) + 1
        
    print(f"3d4 Counts: {counts}")
    
    # Total combinations = 4*4*4 = 64
    total_combos = 64.0
    
    probs = np.zeros(12)
    for s, count in counts.items():
        probs[s-1] = count / total_combos
        
    print(f"Probabilities (indices correspond to roll-1): {probs}")

    num_states = 101
    P = np.zeros((num_states, num_states))
    
    # Chutes and Ladders configuration
    jumps = {
        1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100,
        16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78
    }

    for state in range(num_states - 1):
        for roll_idx, prob in enumerate(probs):
            if prob == 0:
                continue
                
            roll = roll_idx + 1
            next_square = state + roll
            
            if next_square > 100:
                final_state = state # Must land exactly? Usually yes, or bounce back. 
                # Standard rules often say "if > 100, stay put". The previous code did "final_state = state".
            else:
                final_state = jumps.get(next_square, next_square)
            
            P[state, final_state] += prob
            
    P[100, 100] = 1.0
    return P

if __name__ == "__main__":
    print("Building transition matrix for 3d4...")
    P = build_matrix_3d4()
    
    output_filename = "quant/transition_matrix_3d4.csv"
    np.savetxt(output_filename, P, delimiter=",", fmt="%.4f")
    print(f"Saved to {output_filename}")
