#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# \"\"\"deepseek_uniforce.py
# نسخهٔ تمیز و قابل اجرا از پیاده‌سازی UniForCE (DeepSeek-derived)
# شرح: این اسکریپت یک پیاده‌سازی عملی از الگوریتم UniForCE را ارائه می‌دهد (overclustering + unimodal pair testing)
# همراه با توضیحات فارسی خط‌به‌خط، اجرای آزمایشی روی دیتاست‌های استاندارد، و ذخیرهٔ خروجی‌ها
# \
# Usage:
#     python deepseek_uniforce.py
# تنظیمات خروجی (برای اجرا در ویندوز):
#     پیش‌فرض: OUTPUT_DIR = r\"C:\\Users\\user\\Desktop\\uniforcenew\"
# در محیط لینوکس/سرور، مسیر را به دلخواه تغییر دهید، مثلاً '/mnt/data/uniforce_outputs'
# \"\"\"

from __future__ import annotations
import os
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs, make_moons, load_iris
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import textwrap

# -----------------------------
# تنظیمات پیش‌فرض خروجی -- کاربر ویندوزی شما این مسیر را خواست
# -----------------------------
OUTPUT_DIR = r"C:\Users\user\Desktop\uniforcenew"
# اگر می‌خواهید در مسیر دیگری ذخیره شود، پارامتر --output را استفاده کنید

# -----------------------------
# توابع کمکی و پیاده‌سازی الگوریتم
# -----------------------------

def ensure_dir(path: str):
    # \"\"\"Create directory if not exists.\"\"\"
    os.makedirs(path, exist_ok=True)

def count_peaks_1d(data_1d, bw_method='scott', grid_points=512) -> int:
    # \"\"\"
    # برآورد چگالی 1D با KDE و شمارش قله‌ها.
    # پارامترها:
    #   - data_1d: آرایهٔ 1 بعدی داده‌ها
    #   - bw_method: روش انتخاب پهنای باند برای gaussian_kde ('scott' یا 'silverman' یا عدد)
    #   - grid_points: تعداد نقاط برای محاسبهٔ چگالی روی گرید
    # خروجی: تعداد قله‌ها (کمترین مقدار 1)
    # \"\"\"
    data_1d = np.asarray(data_1d)
    if data_1d.size < 5:
        return 1
    try:
        kde = gaussian_kde(data_1d, bw_method=bw_method)
    except Exception:
        # fallback: add tiny noise if singular
        kde = gaussian_kde(data_1d + 1e-6 * np.random.randn(data_1d.size), bw_method=bw_method)
    xs = np.linspace(data_1d.min(), data_1d.max(), grid_points)
    ys = kde(xs)
    peaks = 0
    for i in range(1, len(ys)-1):
        if ys[i] > ys[i-1] and ys[i] > ys[i+1]:
            peaks += 1
    return max(1, peaks)

def unimodal_pair_test(X: np.ndarray, idxs_a: list, idxs_b: list, bw_method='scott') -> bool:
    # \"\"\"آزمون تک‌وجهی بودن ترکیب دو خوشه:
    # 1. نقاط دو خوشه را می‌گیریم و روی خط واصل مراکز پروجکت می‌کنیم.
    # 2. توزیع 1 بعدی پروژکت‌شده را با KDE برآورد می‌کنیم و تعداد قله‌ها را می‌شماریم.
    # 3. اگر تعداد قله‌ها == 1 => قابل ادغام.
    # \"\"\"
    A = X[np.array(idxs_a)]
    B = X[np.array(idxs_b)]
    combined = np.vstack([A, B])
    ca = A.mean(axis=0)
    cb = B.mean(axis=0)
    direction = cb - ca
    norm = np.linalg.norm(direction)
    if norm < 1e-8:
        # مراکز خیلی نزدیکند — ادغام منطقی است
        return True
    direction = direction / norm
    proj = combined.dot(direction)
    peaks = count_peaks_1d(proj, bw_method=bw_method)
    return peaks == 1

def overcluster_kmeans(X: np.ndarray, k0: int, random_state=0):
    # \"\"\"اجرای KMeans با k0 برای ایجاد overclusters اولیه.
    # خروجی: dict از {cluster_label: [indices]} و مراکز
    # \"\"\"
    km = KMeans(n_clusters=k0, random_state=random_state).fit(X)
    labels = km.labels_
    centers = km.cluster_centers_
    clusters = {}
    for i, lab in enumerate(labels):
        clusters.setdefault(int(lab), []).append(int(i))
    return clusters, centers

def uniforce_clustering(X: np.ndarray, k0: int=None, bw_method='scott', random_state=0):
    # \"\"\"پیاده‌سازی اصلی UniForCE (رویکرد greedy pairwise merge).
    # پارامترها:
    #   - X: آرایهٔ شکل (n_samples, n_features)
    #   - k0: تعداد خوشه‌های اولیه (اگر None از قاعدهٔ heuristics استفاده می‌شود)
    # خروجی:
    #   - labels: آرایهٔ n_samples از برچسب‌های نهایی
    #   - cluster_list: فهرست خوشه‌ها (هر خوشه لیستی از اندیس‌ها)
    # \"\"\"
    n = X.shape[0]
    if k0 is None:
        k0 = max(5, int(np.sqrt(n))*2)
    clusters_dict, centers = overcluster_kmeans(X, k0, random_state=random_state)
    cluster_list = [clusters_dict[k] for k in sorted(clusters_dict.keys())]

    changed = True
    iter_no = 0
    while changed:
        iter_no += 1
        changed = False
        merged = [False] * len(cluster_list)
        new_clusters = []
        # گرِدی: هر خوشه را با خوشه‌های بعدی امتحان می‌کنیم
        for i in range(len(cluster_list)):
            if merged[i]:
                continue
            a = cluster_list[i]
            for j in range(i+1, len(cluster_list)):
                if merged[j]:
                    continue
                b = cluster_list[j]
                # اگر دو خوشه قابل ادغام باشند، ادغام می‌کنیم
                if unimodal_pair_test(X, a, b, bw_method=bw_method):
                    a = a + b
                    merged[j] = True
                    changed = True
            new_clusters.append(a)
        cluster_list = new_clusters
    # تولید لیبل‌ها
    labels = np.empty(n, dtype=int)
    for idx, cl in enumerate(cluster_list):
        labels[cl] = idx
    return labels, cluster_list

# -----------------------------
# تابع اجرایی آزمایشی: اجرا روی دیتاست‌ها و ذخیرهٔ نتایج
# -----------------------------
def run_experiments(output_dir: str = OUTPUT_DIR, save_plots: bool = True):
    # \"\"\"اجرای آزمایشی روی چند دیتاست و ذخیرهٔ نتایج و تصاویر.\"\"\"
    ensure_dir(output_dir)
    results = []

    # تعریف دیتاست‌ها: blobs, moons, iris
    X1, y1 = make_blobs(n_samples=300, centers=3, cluster_std=0.7, random_state=0)
    X2, y2 = make_blobs(n_samples=500, centers=5, cluster_std=[0.5,1.2,0.3,0.8,0.6], random_state=1)
    X3, y3 = make_moons(n_samples=300, noise=0.08, random_state=2)
    iris = load_iris()
    datasets = [
        ('blobs_3', X1, y1),
        ('blobs_5', X2, y2),
        ('moons', X3, y3),
        ('iris', iris.data, iris.target)
    ]

    for name, X, y_true in datasets:
        print(f'Running dataset: {name} (n={X.shape[0]}, dim={X.shape[1]})')
        labels_uf, clusters_uf = uniforce_clustering(X, k0=min(50, max(10, X.shape[0]//10)), bw_method='scott', random_state=0)
        k_est = len(clusters_uf)
        ari_uf = adjusted_rand_score(y_true, labels_uf)

        # مقایسه با KMeans با k_true
        k_true = len(np.unique(y_true))
        km = KMeans(n_clusters=k_true, random_state=0).fit(X)
        ari_km = adjusted_rand_score(y_true, km.labels_)

        results.append({
            'dataset': name,
            'n_samples': X.shape[0],
            'true_k': k_true,
            'uf_k': k_est,
            'uf_ARI': round(ari_uf, 4),
            'km_ARI': round(ari_km, 4)
        })

        # ذخیره شکل‌ها (استفاده از دو بعد اول اگر بعد بیشتر است)
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        fig.suptitle(f"{name} — UniForCE k={k_est}, ARI={ari_uf:.3f} | KMeans ARI={ari_km:.3f}")
        axes[0].set_title('True labels')
        axes[0].scatter(X[:, 0], X[:, 1] if X.shape[1] > 1 else np.zeros(len(X)), c=y_true, s=12)
        axes[1].set_title('UniForCE')
        axes[1].scatter(X[:, 0], X[:, 1] if X.shape[1] > 1 else np.zeros(len(X)), c=labels_uf, s=12)
        axes[2].set_title('KMeans (true k)')
        axes[2].scatter(X[:, 0], X[:, 1] if X.shape[1] > 1 else np.zeros(len(X)), c=km.labels_, s=12)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        if save_plots:
            figpath = os.path.join(output_dir, f"{name}_comparison.png")
            fig.savefig(figpath, dpi=150, bbox_inches='tight')
            plt.close(fig)
        else:
            plt.show()

    # ذخیره نتایج به CSV
    df = pd.DataFrame(results)
    csv_path = os.path.join(output_dir, 'uniforce_results.csv')
    df.to_csv(csv_path, index=False)
    print('\\nSummary:')
    print(df)
    print(f'Files saved to: {output_dir}')
    return df

# -----------------------------
# Main: پارس آرگومان‌ها و اجرا
# -----------------------------
def parse_args():
    p = argparse.ArgumentParser(description='Run DeepSeek-derived UniForCE experiments')
    p.add_argument('--output', type=str, default=OUTPUT_DIR, help='Output directory for plots and CSV')
    p.add_argument('--no-plots', action='store_true', help='Do not save plots; show instead')
    return p.parse_args()

def main():
    args = parse_args()
    outdir = args.output
    ensure_dir(outdir)
    df = run_experiments(output_dir=outdir, save_plots=not args.no_plots)

if __name__ == '__main__':
    main()
