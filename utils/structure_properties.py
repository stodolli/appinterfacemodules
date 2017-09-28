"""
    Stefjord Todolli
    October 14, 2017
"""

import numpy as np

S1 = 11.1   # Sedimentation coefficient of nucleosome S20,w
Rn = 55     # Effective radius of nucleosome (5.5 nm or 55 Angstrom), since our distances are in Angstrom

def radius_gyration(protein_frames):
    protein_centers = np.array([p[0] for p in protein_frames])
    rm = np.mean(protein_centers)
    rg_sq = sum(map(lambda x: (np.linalg.norm(x-rm))**2, protein_centers)) * (1.0/len(protein_centers))
    return np.sqrt(rg_sq)

def sedimentation_coefficient(protein_frames, pairwise_distances=None):
    N = len(protein_frames)
    if pairwise_distances is None:
        pcenters = [np.array(p[0]) for p in protein_frames]
        pairwise_distances = [np.linalg.norm(pcenters[i] - pcenters[j]) for i in range(N) for j in range(i+1, N)]
    Sratio = 1 + (2*Rn/N)*sum([1/p for p in pairwise_distances])
    return S1*Sratio

