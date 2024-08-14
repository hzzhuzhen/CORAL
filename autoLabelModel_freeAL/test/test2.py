from sklearn.decomposition import TruncatedSVD
import numpy as np
def reduce_to_k_dim(M, k=2):
    """ Reduce a co-occurence count matrix of dimensionality (num_corpus_words, num_corpus_words)
        to a matrix of dimensionality (num_corpus_words, k) using the following SVD function from Scikit-Learn:
            - http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html
            【降维一个共生数量矩阵，维度为(语料词数*语料词数) 到矩阵维度为(语料词数*k维度)，使用下述Scikit-Learn的SVD方法】

        Params:
            M (numpy matrix of shape (number of unique words in the corpus , number of unique words in the corpus)): co-occurence matrix of word counts【M矩阵(语料词数*语料词数)】
            k (int): embedding size of each word after dimension reduction【降维后的成分数k】
        Return:
            M_reduced (numpy matrix of shape (number of corpus words, k)): matrix of k-dimensioal word embeddings.
                    In terms of the SVD from math class, this actually returns U * S【降维后的矩阵(词数*k)】
    """
    n_iters = 10     # Use this parameter in your call to `TruncatedSVD`
    M_reduced = None
    print("Running Truncated SVD over %i words..." % (M.shape[0]))

    # ------------------
    # Write your implementation here.
    M_reduced = M.copy()
    svd=TruncatedSVD(n_components=k, n_iter=n_iters, random_state=42)
    M_reduced = svd.fit(M_reduced)
    # ------------------

    print("Done.")
    return M_reduced