from multiprocessing import Pool
from datasets import load_dataset
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
import time
import re
import os

POS_WORDS = {"good","great","excellent","wonderful","love","best","amazing","brilliant","perfect"}
NEG_WORDS = {"bad","worst","awful","terrible","hate","boring","waste","poor","horrible"}

def sentiment_score(text: str) -> int:
    """CPU-bound: tokenizuj, policz pozytywne minus negatywne."""
    # TODO Zadanie 2.1: zaimplementuj

    words = re.findall(r"\w+", text.lower())
    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    return pos - neg

# TODO: pobierz 5000 recenzji przez get_imdb_subset
if __name__ == "__main__":
    ds = load_dataset("stanfordnlp/imdb", split="train[:5000]")
    texts = [x["text"] for x in ds]

    # TODO: czas sekwencyjny [s.score(t) for t in texts]

    start = time.time()
    seq_results = [sentiment_score(t) for t in texts]
    seq_time = time.time() - start
    print(f"Sequential: {seq_time:.3f}s")

    # TODO: czas ThreadPool (max_workers=16)

    start = time.time()
    with ThreadPoolExecutor(max_workers=16) as ex:
        thread_results = list(ex.map(sentiment_score, texts))
    thread_time = time.time() - start
    print(f"ThreadPool: {thread_time:.3f}s")

    # TODO: czas multiprocessing.Pool (procesy = os.cpu_count())

    start = time.time()
    with Pool(processes=os.cpu_count()) as pool:
        mp_results = pool.map(sentiment_score, texts, chunksize=100)
    mp_time = time.time() - start
    print(f"Multiprocessing.Pool: {mp_time:.3f}s")

    # TODO: bar plot 3 czasow

    plt.figure(figsize=(8, 5))
    plt.bar(["Sequential", "ThreadPool", "Multiprocessing"],
            [seq_time, thread_time, mp_time],
            color=["gray", "orange", "green"])
    plt.ylabel("Czas [s]")
    plt.title("Porównanie metod przetwarzania 5000 recenzji")

    plt.savefig("wynik_zadanie_2.1.png")
    print("Wykres zapisany jako wynik_zadanie_2.1.png")
