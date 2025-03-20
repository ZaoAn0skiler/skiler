import numpy as np
import matplotlib.pyplot as plt

# 生成连续信号：余弦信号
t = np.linspace(-2, 2, 1000)
y_continuous = np.cos(2 * np.pi * t)

# 生成离散信号：单位阶跃信号
n = np.arange(-5, 6)
y_discrete = np.where(n >= 0, 1, 0)

# 绘制图形
plt.figure(figsize=(10, 4))

# 连续信号子图
plt.subplot(1, 2, 1)
plt.plot(t, y_continuous, 'b')
plt.title('Continuous Signal: Cosine Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# 离散信号子图
plt.subplot(1, 2, 2)
markerline, stemlines, baseline = plt.stem(n, y_discrete, linefmt='gray', markerfmt='D', basefmt=' ')
plt.setp(stemlines, 'linewidth', 2)
plt.setp(markerline, 'markersize', 8, 'color', 'r')
plt.title('Discrete Signal: Unit Step')
plt.xlabel('Sample Index (n)')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()