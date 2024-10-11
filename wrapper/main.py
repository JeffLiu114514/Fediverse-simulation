from generation import GenerationWrapper
from collections import defaultdict
import numpy as np
import scipy
import math
<<<<<<< HEAD

import itertools
import json

DEBUG = False

def kendallTau(A, B):
    pairs = itertools.combinations(range(0, len(A)), 2)

    distance = 0

    for x, y in pairs:
        a = A[x] - A[y]
        b = B[x] - B[y]

        # if discordant (different signs)
        if (a * b < 0):
            distance += 1

    return distance


def run_tests(n_nodes, n_posts, variances=1):
=======

import itertools

def kendallTau(A, B):
    pairs = itertools.combinations(range(0, len(A)), 2)

    distance = 0

    for x, y in pairs:
        a = A[x] - A[y]
        b = B[x] - B[y]

        # if discordant (different signs)
        if (a * b < 0):
            distance += 1

    return distance


if __name__ == "__main__":
    n_nodes = 500
>>>>>>> 984262a486ae26b52d184a49771aec76c744420e
    user_server_ratio = 0.2
    server_clique_ratio = 1
    clique_size_expectation = 5
    n_servers = int(n_nodes * user_server_ratio)
    n_cliques = int(n_servers * server_clique_ratio)
    
    threshold = 0
    n_mult = n // 3 + 1
    beta3 = 1 / (n_mult**2 + n_mult + 1) # beta1 + beta2 + beta3 = 1, beta1 = (n/3 + 1)beta2 + (n/3 + 1)beta3, beta2 = (n/3 + 1)beta3
    beta2 = beta3 * n_mult
    beta1 = beta2 * n_mult + beta3 * n_mult
    beta_settings = (beta1, beta2, beta3)
    if DEBUG: print("beta settings: ", beta1, beta2, beta3)
    
    posts_hyperparameters = [variances, beta1, beta2, beta3, threshold]
    # variances, beta1, beta2, beta3, engagement_threshold
    
    gw = GenerationWrapper(n_nodes, n_servers, n_cliques, clique_size_expectation, posts_hyperparameters)
    
    true_scores = defaultdict(list)
    discrete_scores = defaultdict(list)
<<<<<<< HEAD
    for i in range(n_posts):
        post = gw.make_post(i)
        scores = gw.post_reactions(post)
        for user, score in scores.items():

=======
    for i in range(50):
        post = gw.make_post(i)
        scores = gw.post_reactions(post)
        for user, score in scores.items():
            
            
>>>>>>> 984262a486ae26b52d184a49771aec76c744420e
            discrete_scores[user].append(score[0])
            true_scores[user].append(score[1])
    
    users_to_search = list(set(discrete_scores.keys()).union(set(true_scores.keys())))
<<<<<<< HEAD
    
    all_upper_bounds = []
    all_raw_distances = []
    all_visbility = []
    all_lengths = []
    all_normalized_distances = []
    all_correlations = []
    for i in users_to_search:
        discrete_score = discrete_scores[i]
        true_score = true_scores[i]
        
        if len(discrete_score) <= 1 or len(true_score) <= 1:
            continue

        user = gw.users[i]
        
        reversible_upper_bound = (len(user.first_visibility) + 1) * (len(user.second_visibility) + 1) * (len(user.third_visibility) + 1) - 1
        if reversible_upper_bound < 2:
            continue
        
        all_upper_bounds.append(reversible_upper_bound)
        
        num_posts_seen = len(discrete_score)
        all_lengths.append(num_posts_seen)
        
=======
    for i in users_to_search:
        discrete_score = discrete_scores[i]
        true_score = true_scores[i]
        if len(discrete_score) == 1 or len(true_score) == 1:
            continue
>>>>>>> 984262a486ae26b52d184a49771aec76c744420e
        discrete_ranking = np.argsort(discrete_score)
        true_ranking = np.argsort(true_score)
        kendall_tau_correlation = scipy.stats.kendalltau(discrete_ranking, true_ranking)
        kendall_tau_distance = kendallTau(discrete_score, true_score)
        # print(discrete_ranking.size)
        # print(len(discrete_ranking))
<<<<<<< HEAD
        if num_posts_seen > reversible_upper_bound:
            kendall_tau_distance_normalized = kendall_tau_distance / math.comb(reversible_upper_bound, 2)
        else:
            kendall_tau_distance_normalized = kendall_tau_distance / math.comb(num_posts_seen, 2)
        
        if DEBUG:
            print(discrete_score, true_score)
            print(discrete_ranking, true_ranking)
            print("Kendall Tau Correlation: ", kendall_tau_correlation)
            print("Kendall Tau Distance: ", kendall_tau_distance)
            print("Kendall Tau Distance Normalized: ", kendall_tau_distance_normalized)
        
        all_correlations.append(kendall_tau_correlation)
        all_raw_distances.append(kendall_tau_distance)
        all_normalized_distances.append(kendall_tau_distance_normalized)
    
    return all_upper_bounds, all_lengths, all_raw_distances, all_normalized_distances, all_correlations, beta_settings

if __name__ == "__main__":
    n_nodes_list = [x for x in range(50, 501, 25)]
    n_posts_list = [x for x in range(50, 501, 25)]
    variances = [x/100 for x in range(10, 101, 10)]
    results = {}
    
    for n in n_nodes_list:
        for p in n_posts_list:
            for v in variances:
                print("Nodes: ", n, "Posts: ", p, "Variances: ", v)
                all_upper_bounds, all_lengths, all_raw_distances, all_normalized_distances, all_correlations, beta_settings = run_tests(n, p, variances=v)
                results[str((n, p, v))] = {
                    "Average_Upper_Bound": np.mean(all_upper_bounds),
                    "Average_Length": np.mean(all_lengths),
                    "Average_Raw_Distance": np.mean(all_raw_distances),
                    "Average_Normalized_Distance": np.mean(all_normalized_distances),
                    "beta_settings": beta_settings
                }
                # print("Average Upper Bound: ", np.mean(all_upper_bounds))
                # print("Average Length: ", np.mean(all_lengths))
                # print("Average Raw Distance: ", np.mean(all_raw_distances))
                # print("Average Normalized Distance: ", np.mean(all_normalized_distances))
                print()
                
    # Save results as JSON
    with open('results.json', 'w') as f:
        json.dump(results, f)
=======
        kendall_tau_distance_normalized = kendall_tau_distance / math.comb(discrete_ranking.size, 2)
        print(discrete_score, true_score)
        print(discrete_ranking, true_ranking)
        print("Kendall Tau Correlation: ", kendall_tau_correlation)
        print("Kendall Tau Distance: ", kendall_tau_distance)
        print("Kendall Tau Distance Normalized: ", kendall_tau_distance_normalized)
        
>>>>>>> 984262a486ae26b52d184a49771aec76c744420e
    
    # print(gw.user_visible_by_follow)
    # gw.visualize_user_graph_networkx()
    # gw.visualize_user_graph_graphviz()
    # # for i in range(5):
    # gw.update_network(5)
    # for post in gw.posts_log:
    #     for positive in post.positive_engagements:
    #         print(positive)
    #     for negative in post.negative_engagements:
    #         print(negative)
    # gw.visualize_user_graph_graphviz(filename="after_posts.gv")