import os
import time
import sqlite3
from multiprocessing import Pool

from utils.list_manipulation import split_list_random
from utils.queries import query_explain, condition_name, condition_winery_name
from utils.time_utils import compute_eta, format_seconds


def _find_node(explanation: dict, correct_description: str):
    """Find stage in explanation where the 'description' field corresponds to `correct_description`."""
    if explanation is None:
        return None

    if explanation['description']==correct_description:
        return explanation['value']

    for detail in explanation['details']:
        result = _find_node(detail, correct_description)
        if result is not None:
            return result


def _get_explanation(word: str, index: str = 'name'):
    explanation = None
    if index == 'name':
        explanation = query_explain(condition_name(word), verbose=False)
    elif index == 'winery_name':
        explanation = query_explain(condition_winery_name(word), verbose=False)
    else:
        raise ValueError("The index must be either 'name' or 'winery_name'")

    if explanation is not None:
        return explanation['explanation']


def get_document_occurrences(word: str, index: str = 'name'):
    """Get number of documents containing the term `word` in the index."""
    explanation = _get_explanation(word, index)
    if explanation is None:
        return 0
    return _find_node(explanation, 'n, number of documents containing term')


def get_total_documents(word: str, index: str = 'name'):
    """Get the total number of documents in the index."""
    explanation = _get_explanation(word, index)
    if explanation is None:
        return 0
    return _find_node(explanation, 'N, total number of documents with field')


def _get_all_occurrences(vocabulary: list):
    """Get number of documents in the index containing each term of the `vocabulary`."""
    occurences = {}

    t0 = time.time()
    t1 = t0
    eta = None
    for i, word in enumerate(vocabulary):
        # ETA
        t = time.time()
        eta = compute_eta(t-t1, len(vocabulary)-i, eta)
        print(f'{i} of {len(vocabulary)}, {word}'.ljust(50) +
              f"T/step: {t-t1:.2f}s, Elapsed: {format_seconds(t-t0)}, ETA: {format_seconds(eta)}.",
              end='\r')
        occurences[word] = get_document_occurrences(word, 'name')
        t1 = t
    return occurences


def get_all_occurrences_db(vocabulary: list, database_name='database.db'):
    """Get number of documents in the index containing each term of the `vocabulary`."""
    occurences = {}

    # Connect to the SQLite database
    conn = sqlite3.connect(database_name)
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS word_frequency (
            word TEXT PRIMARY KEY,
            frequency INTEGER
        )
    ''')

    try:
        t0 = time.time()
        t1 = t0
        eta = None
        for i, word in enumerate(vocabulary):
            # Check if the word is already in the database
            c.execute("SELECT word FROM word_frequency WHERE word = ?", (word,))
            if c.fetchone() is not None:
                continue

            # ETA
            t = time.time()
            eta = compute_eta(t-t1, len(vocabulary)-i, eta)
            print(f'{i} of {len(vocabulary)}, {word}'.ljust(50) +
                f"T/step: {t-t1:.2f}s, Elapsed: {format_seconds(t-t0)}, ETA: {format_seconds(eta)}.",
                end='\r')
            occurences[word] = get_document_occurrences(word, 'name')

            # Insert the data into the table
            c.execute("INSERT OR REPLACE INTO word_frequency VALUES (?,?)", (word, occurences[word]))

            t1 = t
    except KeyboardInterrupt:
        pass

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return occurences


def get_all_occurrences(vocabulary: list, parallel = False, num_jobs: int = None):
    """Get number of documents in the index containing each term of the `vocabulary`.

    Optionally, the download can be parallelized."""
    if not parallel:
        return _get_all_occurrences(vocabulary)

    if num_jobs is None:
        num_jobs = os.cpu_count()
    p = Pool(num_jobs)

    return p.map(_get_all_occurrences, split_list_random(vocabulary, num_jobs))
