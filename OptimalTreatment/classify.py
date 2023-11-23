# TODO: write test cases!
# TODO: write docstrings!

import numpy as np
import pandas as pd

def dead(traj, max_tumour_size):
    size = np.sum(traj,axis=0)
    return any([s > max_tumour_size for s in size])

def pointwise_changes(series):
    return [series[i+1] - series[i] for i in range(len(series)-1)]

def series_stationary(series, epsilon):
    pw_changes = pointwise_changes(series)
    delta_last_ten_perc = pw_changes[int(len(pw_changes) * 0.9):]
    return all([ abs(delta) < epsilon for delta in delta_last_ten_perc ])
   
def stationary(traj, epsilon):
    s_over_time = [point[0] for point in traj]
    r_over_time = [point[1] for point in traj]
    return series_stationary(s_over_time, epsilon) and series_stationary(r_over_time, epsilon)

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
 
def series_periodic(series, eps_orbit):
    # calculate autocorrelation
    autocorr = np.correlate(series, series, mode='full')
    
    # bias correction (correct for decay due to decreasing overlap)
    N = len(series)
    bias_factors = [N/np.abs(N-i) for i in range(N)]
    bias_factors = bias_factors[::-1] + bias_factors[1:]
    ub_autocorr = list(autocorr * bias_factors)
    
    # check if the peak in the autocorrelation recurs at any point
    peak_value = max(ub_autocorr)
    recurrences = sum(np.isclose(peak_value, ub_autocorr, atol=eps_orbit))

    return recurrences > 1

def periodic(traj, eps_orbit):
    svals, rvals = [point[0] for point in traj], [point[1] for point in traj]
    sper = series_periodic(svals, eps_orbit)
    rper = series_periodic(rvals, eps_orbit)

    return sper and rper

def classify_trajectory(traj, max_tumour_size, min_tumour_size, eps_ss, eps_orbit):
    if dead(traj, max_tumour_size):
        return 'dead'
    elif stationary(traj, eps_ss):
        return classify_steady_state(traj, min_tumour_size)
    
    # problem: we can determine if the signal has periodic components, but we can't actually tell
    # if we're truly on a limit cycle or if we're just in a transient orbit
    # so detecting periodicity is meaningless -> it's just indeterminate limit behaviour (not converged)

    # elif periodic(traj, eps_orbit):
    #     return 'periodic'
    else:
        return 'indeterminate' # no limiting behavour reached (could be periodic)

def score_trajectory(traj, max_tumour_size, min_tumour_size, eps_ss, eps_orbit):
    clfcation = classify_trajectory(traj, max_tumour_size, min_tumour_size, eps_ss, eps_orbit)
    if clfcation == 'dead':
        survival_time = np.where(np.sum(traj,axis=0) < max_tumour_size)[0][-1]
        return 'dead', survival_time,
    elif clfcation == 'indeterminate':
        return 'indeterminate', np.nan
    elif clfcation in ['R only', 'S only', 'mixed tumour', 'cure']:
        final_size = traj[:,-1].sum()
        return 'alive', final_size
    # elif clfcation == 'periodic':
    #     # mean_size = find_mean_size_of_orbit(traj)
    #     # return 'alive', mean_size
    #     pass

def score_gridpoint(trjs, max_tumour_size, min_tumour_size, eps_ss, eps_orbit):
    outcomes = []
    for trj in trjs:
        life_status, score = score_trajectory(trj, max_tumour_size, min_tumour_size, eps_ss, eps_orbit)
        outcomes.append([life_status, score])
    outcomes = pd.DataFrame(outcomes, columns=['life_status', 'score'])
    
    survival_rate = len(outcomes[outcomes['life_status'] in ['alive', 'indeterminate']) / len(outcomes)
    # for the cases that died report the average survival time
    mean_survival_time = outcomes[outcomes['life_status'] == 'dead']['score'].mean()
    # for the cases that survived report the average tumour size
    mean_tumour_size = outcomes[outcomes['life_status'] in ['alive', 'indeterminate']]['score'].mean()

    return survival_rate, mean_survival_time, mean_tumour_size

# score = {'dead'         : 0,        # clearly bad
#          'R only'       : 0,        # adaptive therapy made it worse
#          'mixed tumour' : 0,        # adaptive therapy had no qualitative effect
#          'periodic'     : 0,        # adaptive therapy had no qualitative effect
#          'S only'       : 0.5,      # adaptive therapy made it better (can now hit with chemo)
#          'cure'         : 1,        # clearly good
#          'indeterminate': np.nan    # failed to determine behaviour
# }

# def classify_gridpoint(outcomes):
#     # different outcomes for different initial conditions for the same parameter set (gridpoint)
#     return np.sum([score[outc] for outc in outcomes])/len(outcomes)

def read_gridpoint(gridpoint_path):
    pass