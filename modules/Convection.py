def coeff_natural(L: float, T_W: float, T_U: float):
    # values for air at 20 °C, asumed to be constant
    Pr = 0.718
    ny = 13.3 * 10 ** -6 # mm^2/s
    k = 0.0262

    beta_P = 1 / T_U

    Gr = (9.81 * beta_P * L**3 * abs(T_W - T_U)) / ny**2

    Ra = Gr * Pr

    Nu_0 = 1.0
    f_Pr = 0.765 + 0.03 * (Pr - 0.7) / 0.3
    Nu = Nu_0 + 0.668 * f_Pr * Ra**0.25

    alpha = Nu * k / L

    return alpha

def coeff_forced(L: float, u: float):
    # values for air at 20 °C, asumed to be constant
    Pr = 0.718
    ny = 13.3 * 10 ** -6 # mm^2/s
    k = 0.0262

    Re = u*L/ny

    Nu = 0.037 * ( Re ** 0.8 - 23100) * Pr ** (1/3)

    alpha = Nu * k / L

    return alpha
