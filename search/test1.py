import numpy as np
import scipy.linalg as la

def newton_raphson(f, J, x0, tol=1e-8, max_iter=100):
    """
    Robust Newton-Raphson method with multiple initial guess strategies
    """
    # List of initial guesses to try
    initial_guesses = [
        x0,  # Original guess
        x0 * 1.5,  # Scaled up
        x0 * 0.5,  # Scaled down
        np.random.rand(len(x0)),  # Random guess
    ]
    
    last_error = None
    for guess in initial_guesses:
        x = guess.copy()
        
        for iter_count in range(max_iter):
            try:
                # Compute function values and Jacobian
                f_val = f(x)
                jacobian = J(x)
                
                # Use more robust linear algebra solving
                # Try different methods if standard solve fails
                try:
                    # First try standard solve
                    delta = la.solve(jacobian, -f_val, assume_a='sym')
                except (la.LinAlgError, np.linalg.LinAlgError):
                    try:
                        # Try least squares solution
                        delta = la.lstsq(jacobian, -f_val)[0]
                    except Exception as e:
                        print(f"Solving failed: {e}")
                        # Skip to next guess if this fails
                        break
                
                # Update solution
                x_new = x + delta
                
                # Check convergence
                if np.linalg.norm(delta) < tol:
                    return x_new, iter_count + 1
                
                x = x_new
            
            except Exception as e:
                print(f"Iteration error: {e}")
                last_error = e
                break
    
    raise ValueError(f"Method did not converge. Last error: {last_error}")

def nonlinear_system_functions(x):
    """Define the system of nonlinear equations"""
    return np.array([
        x[0]**2 + x[1]**2 - 4,  # f₁: x² + y² = 4
        x[0] * x[1] - 1          # f₂: x*y = 1
    ])

def nonlinear_system_jacobian(x):
    """Compute the Jacobian matrix"""
    return np.array([
        [2*x[0], 2*x[1]],      # ∂f₁/∂x, ∂f₁/∂y
        [x[1], x[0]]            # ∂f₂/∂x, ∂f₂/∂y
    ])

# Multiple ways to solve
initial_guesses = [
    np.array([1.0, 1.0]),
    np.array([2.0, 0.5]),
    np.array([0.5, 2.0])
]

for guess in initial_guesses:
    print("\nTrying initial guess:", guess)
    try:
        solution, iterations = newton_raphson(
            nonlinear_system_functions, 
            nonlinear_system_jacobian, 
            guess
        )
        
        print("Solution:")
        print(f"x = {solution[0]:.6f}")
        print(f"y = {solution[1]:.6f}")
        print(f"Iterations: {iterations}")
        
        # Verify solution
        print("\nVerification:")
        print(f"x² + y² = {solution[0]**2 + solution[1]**2:.6f}")
        print(f"x*y = {solution[0] * solution[1]:.6f}")
        break
    except ValueError as e:
        print(f"Error: {e}")