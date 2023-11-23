import numpy as np

def tumour_size_over_time(traj):
    return [sum(point) for point in traj]

def dead(traj, max_tumour_size):
    size = tumour_size_over_time(traj)
    return any([s > max_tumour_size for s in size])

def pointwise_change(traj):
    size = tumour_size_over_time(traj)
    return [size[i+1] - size[i] for i in range(len(size)-1)]

def stationary(traj, epsilon):
    last_ten_perc = pointwise_change(traj)[int(len(traj) * 0.9):] 
    return all([ abs(s) < epsilon for s in last_ten_perc ])

def classify_steady_state(traj, min_size):
    S_end, R_end = traj[-1]

    if S_end < min_size and R_end < min_size:
        return 'cure'
    elif R_end < min_size and S_end > min_size:
        return 'S only'
    elif S_end < min_size and R_end > min_size:
        return 'R only'
    else:
        return 'mixed tumour'
    
def periodic(traj):
    size = tumour_size_over_time(traj)

    # calculate autocorrelation
    autocorr = np.correlate(size, size, mode='full')
    # bias correction (correct for decay due to decreasing overlap)
    N = len(size)
    bias_factors = [N/np.abs(N-i) for i in range(N)]
    bias_factors = bias_factors[::-1] + bias_factors[1:]
    ub_autocorr = list(autocorr * bias_factors)

    # check if the peak in the autocorrelation recurs at any point
    peak_value = max(ub_autocorr)
    recurrences = sum(np.isclose(peak_value, ub_autocorr))

    return recurrences > 1

def classify_trajectory(traj, max_tumour_size, min_tumour_size, eps_ss, eps_orbit):
    if dead(traj, max_tumour_size):
        return 'dead'
    elif stationary(traj, eps_ss):
        return classify_steady_state(traj, min_tumour_size)
    elif periodic(traj, eps_orbit):
        return 'periodic'
    else:
        return 'not reached limiting behaviour'
    

# TODO: these functions have not been throughly tested yet!!!