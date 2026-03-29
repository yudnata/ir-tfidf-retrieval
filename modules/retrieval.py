import re
import numpy as np
from modules.preprocessing import preprocess


def natural_sort_key(filename):
    """Key untuk sorting natural: D1, D2, ..., D10."""
    parts = re.findall(r'\d+', filename)
    return int(parts[0]) if parts else 0


def tfidf_query(query_str, vocab, doc_ids, idf, tfidf_matrix):
    """
    Melakukan pencarian query menggunakan TF-IDF.

    Untuk setiap kata dalam query:
    - Cari nilai TF-IDF kata tersebut di setiap dokumen
    - Hitung skor total setiap dokumen = jumlah TF-IDF dari semua query terms
    - Ranking dokumen berdasarkan skor tertinggi
    """

    query_tokens = preprocess(query_str)

    if not query_tokens:
        return [], {}, {}, [], "Query tidak menghasilkan token setelah preprocessing."

    term_scores = {}
    for term in query_tokens:
        term_scores[term] = {}
        if term in vocab:
            idx = vocab.index(term)
            for j, doc_id in enumerate(doc_ids):
                val = tfidf_matrix[idx][j]
                term_scores[term][doc_id] = round(val, 6)
        else:
            for doc_id in doc_ids:
                term_scores[term][doc_id] = 0.0

    doc_scores = {}
    for doc_id in doc_ids:
        total = 0.0
        for term in query_tokens:
            total += term_scores[term].get(doc_id, 0.0)
        doc_scores[doc_id] = round(total, 6)

    ranked_docs = sorted(
        [(doc_id, score) for doc_id, score in doc_scores.items() if score > 0],
        key=lambda x: (-x[1], natural_sort_key(x[0])),
    )

    detail_lines = []
    detail_lines.append(f'Query: "{query_str}"')
    detail_lines.append(f"Token setelah preprocessing: {query_tokens}")
    detail_lines.append("")

    for term in query_tokens:
        idf_val = idf.get(term, 0)
        detail_lines.append(f'IDF("{term}") = {round(idf_val, 6)}')

    detail_lines.append("")
    detail_lines.append("Skor TF-IDF per term per dokumen:")

    for term in query_tokens:
        idf_val = idf.get(term, 0)
        scores_per_doc = term_scores.get(term, {})
        non_zero = [
            (doc_id, val)
            for doc_id, val in scores_per_doc.items()
            if val > 0
        ]
        non_zero.sort(key=lambda x: x[1], reverse=True)

        if idf_val == 0 and term in vocab:
            detail_lines.append(f"  \"{term}\": Skor 0 karena kata ada di SEMUA dokumen (IDF=0)")
        elif non_zero:
            docs_str = ", ".join(
                [f"{d.replace('.txt', '')}={v:.6f}" for d, v in non_zero]
            )
            detail_lines.append(f"  \"{term}\": {docs_str}")
        else:
            detail_lines.append(f"  \"{term}\": (kata tidak ditemukan di database)")

    detail_lines.append("")
    detail_lines.append("Total skor per dokumen (ranking):")
    for doc_id, score in ranked_docs:
        parts = []
        for term in query_tokens:
            val = term_scores[term].get(doc_id, 0.0)
            if val > 0:
                parts.append(f'TF-IDF("{term}")={val:.6f}')
        calc_str = " + ".join(parts) if parts else "0"
        detail_lines.append(f"  {doc_id.replace('.txt', '')}: {calc_str} = {score:.6f}")

    detail_text = "\n".join(detail_lines)

    return query_tokens, term_scores, doc_scores, ranked_docs, detail_text
