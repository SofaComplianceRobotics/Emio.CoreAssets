from qpsolvers import Problem, solve_problem, available_solvers
import os
import Sofa
# https://pypi.org/project/qpsolvers/
# https://qpsolvers.github.io/qpsolvers/quadratic-programming.html#qpsolvers.solve_qp
# Available solvers:
# >> print(qpsolvers.available_solvers())
# ['clarabel', 'cvxopt', 'daqp', 'ecos', 'highs', 'osqp', 'piqp', 'proxqp', 'qpalm', 'quadprog', 'scs']

import numpy as np
from numpy import linalg as la
from math import pi


def getTorques(W, Hdq_free, iE, iA, q_s, q_t, q_e):
    """

    Args:
        W: compliance matrix (size of 7 by 7)
        Hdq_free: free motion vector (size of 7)
        iE: indices of the effector in the system (W and Hdq_free)
        iA: indices of the actuators in the system (W and Hdq_free)
        q_s: position (x,y,z) of the sensor (real marker)
        q_t: position (x,y,z) of the target
        q_e: position (x,y,z) of the effector in the simulation (simulation marker)

    Returns:
        torques: corresponds to the motor torques to apply

    """
    # Build the inverse problem system using the matrices provided by SOFA.
    #
    # Minimize 1/2 xt*P*x + qt*x
    # subject to G*x <= h,
    #            A*x = b,
    #         and lb <= x <= ub

    # Note that:
    #      1. You can access a block Wii of the matrix W by doing:
    #         Wii = W[indices, :][:, indices]
    #      2. W and Hdq_free are numpy matrices, so the you can use the @ operator
    #         for the matrices product, ex: W @ Hdq_free
    #      3. W.T gives you the transpose of the matrix W
    # todo: build the inverse system matrices
    P = None
    q = None

    # Add an energy term to the minimization.
    # This will help in the case of multiple solutions, the solver will converge to the one that
    # minimize the work of the actuators.
    # todo: uncomment the three following lines
    # weight = 0.01  
    # Waa = W[iA, :][:, iA]
    # P += weight * la.norm(P) / la.norm(Waa) * Waa
    
    # todo: limit the torques
    lb = None
    ub = None

    torques = [0., 0., 0., 0.]
    if P is not None:
        try:
            problem = Problem(P, q, None, None, None, None, lb, ub)
            solution = solve_problem(problem, solver="clarabel")
            torques = solution.x
        except Exception as e:
            Sofa.msg_error(os.path.basename(__file__), str(e))
            raise

    return torques





