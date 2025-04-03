import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("信号生成器")
        self.root.geometry("1000x700")
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 初始化Matplotlib图形
        self.fig, self.ax = plt.subplots(figsize=(8, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # 控制面板框架
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        
        # --- 信号类型选择 ---
        self.signal_type = tk.StringVar(value="discrete")  # 默认离散信号
        
        type_frame = ttk.LabelFrame(control_frame, text="信号类型")
        type_frame.pack(side=tk.LEFT, padx=10)
        
        # 单选按钮：离散/连续
        ttk.Radiobutton(type_frame, text="离散信号", variable=self.signal_type, 
                       value="discrete", command=self.update_ui).pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="连续信号", variable=self.signal_type,
                       value="continuous", command=self.update_ui).pack(anchor=tk.W)
        
        # --- 离散信号按钮区域 ---
        self.discrete_frame = ttk.LabelFrame(control_frame, text="离散信号选项")
        self.discrete_buttons = [
            ("单位阶跃", self.plot_step),
            ("单位冲激", self.plot_impulse),
            ("矩形信号", self.plot_rect),
            ("正弦离散", self.plot_sin)
        ]
        for text, cmd in self.discrete_buttons:
            ttk.Button(self.discrete_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=2)
        
        # --- 连续信号参数区域 ---
        self.continuous_frame = ttk.LabelFrame(control_frame, text="连续信号参数")
        
        # 正弦/余弦选择
        self.wave_type = tk.StringVar(value="sine")
        ttk.Radiobutton(self.continuous_frame, text="正弦", variable=self.wave_type,
                       value="sine").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(self.continuous_frame, text="余弦", variable=self.wave_type,
                       value="cosine").pack(side=tk.LEFT, padx=5)
        
        # 幅值输入
        ttk.Label(self.continuous_frame, text="幅值:").pack(side=tk.LEFT, padx=5)
        self.amplitude = ttk.Entry(self.continuous_frame, width=5)
        self.amplitude.insert(0, "1.0")  # 默认幅值
        self.amplitude.pack(side=tk.LEFT)
        
        # 周期输入
        ttk.Label(self.continuous_frame, text="周期:").pack(side=tk.LEFT, padx=5)
        self.period = ttk.Entry(self.continuous_frame, width=5)
        self.period.insert(0, "1.0")  # 默认周期
        self.period.pack(side=tk.LEFT)
        
        # 生成连续信号按钮
        ttk.Button(self.continuous_frame, text="生成", 
                  command=self.plot_continuous).pack(side=tk.LEFT, padx=10)
        
        # 初始UI更新
        self.update_ui()
    
    def update_ui(self):
        """根据信号类型显示/隐藏控件"""
        if self.signal_type.get() == "discrete":
            self.continuous_frame.pack_forget()
            self.discrete_frame.pack(side=tk.LEFT, padx=10)
        else:
            self.discrete_frame.pack_forget()
            self.continuous_frame.pack(side=tk.LEFT, padx=10)
    
    def on_close(self):
        plt.close(self.fig)
        self.root.destroy()
    
    def clear_plot(self):
        self.ax.clear()
        self.ax.grid(True)
    
    # --------------------------
    # 离散信号生成函数（保持不变）
    # --------------------------
    def plot_step(self):
        n = np.arange(-5, 6)
        y = np.where(n >= 0, 1, 0)
        self._plot_discrete(n, y, "Unit Step Signal")
    
    def plot_impulse(self):
        n = np.arange(-5, 6)
        y = np.where(n == 0, 1, 0)
        self._plot_discrete(n, y, "Unit Impulse Signal")
    
    def plot_rect(self):
        n = np.arange(-5, 6)
        y = np.where((n >= -2) & (n <= 2), 1, 0)
        self._plot_discrete(n, y, "Rectangular Signal")
    
    def plot_sin(self):
        n = np.arange(0, 10)
        y = np.sin(2 * np.pi * n / 5)
        self._plot_discrete(n, y, "Discrete Sinusoidal Signal")
    
    def _plot_discrete(self, n, y, title):
        self.clear_plot()
        markerline, stemlines, baseline = self.ax.stem(n, y, linefmt='grey', markerfmt='D', basefmt=' ')
        plt.setp(stemlines, linewidth=1)
        plt.setp(markerline, markersize=6, color='red')
        self.ax.set_title(title)
        self.ax.set_xlabel("Sample Index (n)")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()
    
    # --------------------------
    # 连续信号生成函数
    # --------------------------
    def plot_continuous(self):
        # 获取用户输入参数
        try:
            A = float(self.amplitude.get())  # 幅值
            T = float(self.period.get())      # 周期
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数值！")
            return
        
        # 生成时间序列
        t = np.linspace(-2, 2, 1000)
        freq = 1 / T  # 频率 = 1/周期
        
        # 根据选择的波形类型生成信号
        if self.wave_type.get() == "sine":
            y = A * np.sin(2 * np.pi * freq * t)
            title = f"Sinusoidal signal (A={A}, T={T})"
        else:
            y = A * np.cos(2 * np.pi * freq * t)
            title = f"Cosine signal (A={A}, T={T})"
        
        # 绘图
        self.clear_plot()
        self.ax.plot(t, y, 'b', linewidth=2)
        self.ax.set_title(title)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.ax.grid(True)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()