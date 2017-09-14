"""
    Stefjord Todolli
    October 14, 2017
"""

import numpy as np


def radius_gyration(protein_frames):
    protein_centers = np.array([p[0] for p in protein_frames])
    rm = np.mean(protein_centers)
    rg_sq = sum(map(lambda x: (np.linalg.norm(x-rm))**2, protein_centers)) * (1.0/len(protein_centers))
    return np.sqrt(rg_sq)

