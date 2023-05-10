import scipy.sparse as sparse
from scipy.spatial.distance import cosine
from scipy.sparse._arrays import csr_array


def from_dict_to_sparse_array(vector_data: dict[str: int]):
    shape = vector_data['shape']
    indices = vector_data['indices']
    indptr = vector_data['indptr']
    values = vector_data['values']
    return sparse.csr_array((values, indices, indptr), shape=shape)


def calculate_similarity(vector1: csr_array, vector2: csr_array) -> float:
    correlation = 1 - cosine(vector1.toarray().reshape(-1), vector2.toarray().reshape(-1))
    return correlation
