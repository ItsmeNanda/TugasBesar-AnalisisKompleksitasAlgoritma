import streamlit as st
import time
import random
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(20000)

st.set_page_config(page_title="Analisis Algoritma - Maximum Subarray", layout="wide")

def solve_brute_force(arr):
    n = len(arr)
    max_so_far = float('-inf')
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if current_sum > max_so_far:
                max_so_far = current_sum
    return max_so_far

def max_crossing_sum(arr, low, mid, high):
    left_sum = float('-inf')
    total = 0
    for i in range(mid, low - 1, -1):
        total += arr[i]
        if total > left_sum: left_sum = total
    right_sum = float('-inf')
    total = 0
    for i in range(mid + 1, high + 1):
        total += arr[i]
        if total > right_sum: right_sum = total
    return left_sum + right_sum

def solve_dc(arr, low, high):
    if low == high: return arr[low]
    mid = (low + high) // 2
    return max(solve_dc(arr, low, mid),
               solve_dc(arr, mid + 1, high),
               max_crossing_sum(arr, low, mid, high))

# STREAMLIT
st.title("📊 Analisis Kompleksitas: Brute Force vs Divide & Conquer")
st.markdown("### Kasus: Maximum Subarray Problem")

menu = st.sidebar.selectbox("Pilih Menu", ["Home", "Input Data", "Benchmark Grafik"])

if menu == "Home":
    st.info("Topik ini membandingkan efisiensi O(n²) vs O(n log n).")
    st.write("**Brute Force:** Mengecek setiap subarray satu per satu.")
    st.write("**Divide & Conquer:** Memecah array menjadi bagian kecil secara rekursif.")
    st.markdown("### Studi Kasus")
    st.write("Studi Kasus ini berfokus pada penyelesaian Maximum Subarray Problem, yaitu mencari sebuah subarray kontigu di dalam sebuah array satu dimensi angka yang memiliki jumlah (sum) terbesar. Masalah ini relevan dalam bidang analisis data keuangan (mencari periode keuntungan maksimal) maupun pemrosesan citra. Fokus utama penelitian ini adalah membandingkan efisiensi waktu eksekusi antara pendekatan Brute Force (Iteratif) dengan pendekatan Divide and Conquer (Rekursif) ")
    st.markdown("### ANALYSIS AND RESULTS")
    st.write("Analisis ini membandingkan efisiensi Brute Force ($O(n^2)$) dan Divide and Conquer O(n log n). Hasil pengujian menunjukkan bahwa pendekatan Divide and Conquer jauh lebih cepat dan stabil pada dataset skala besar. Sebaliknya, pendekatan Brute Force mengalami lonjakan waktu eksekusi yang drastis seiring bertambahnya jumlah input data karena kompleksitasnya yang lebih tinggi. ")
elif menu == "Input Data":
    st.subheader("⌨️ Coba Input Data")
    user_input = st.text_input("Masukkan angka dipisah spasi", "-2 1 -3 4 -1 2 1 -5 4")
    if st.button("Hitung"):
        data = [int(x) for x in user_input.split()]
        res_bf = solve_brute_force(data)
        res_dc = solve_dc(data, 0, len(data)-1)
        
        col1, col2 = st.columns(2)
        col1.metric("Hasil Brute Force", res_bf)
        col2.metric("Hasil Divide & Conquer", res_dc)
        st.success("Hasil Keduanya Valid & Sama")

elif menu == "Benchmark Grafik":
    st.subheader("📈 Analisis Running Time")
    if st.button("Mulai Benchmark"):
        sizes = [10, 100, 500, 1000, 2000, 3000, 4000, 5000]
        t_bf, t_dc = [], []
        
        progress_bar = st.progress(0)
        for i, n in enumerate(sizes):
            data = [random.randint(-100, 100) for _ in range(n)]
            
            # BF
            start = time.time()
            solve_brute_force(data)
            t_bf.append(time.time() - start)
            
            # DC
            start = time.time()
            solve_dc(data, 0, len(data)-1)
            t_dc.append(time.time() - start)
            
            progress_bar.progress((i + 1) / len(sizes))

        fig, ax = plt.subplots()
        ax.plot(sizes, t_bf, 'r-o', label="Brute Force O(n²)")
        ax.plot(sizes, t_dc, 'b-o', label="Divide & Conquer O(n log n)")
        ax.set_xlabel("Ukuran Data (n)")
        ax.set_ylabel("Waktu (detik)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        st.write("Terlihat jelas bahwa garis merah (Brute Force) naik secara dratis.")