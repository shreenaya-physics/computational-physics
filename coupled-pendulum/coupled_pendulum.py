


from tkinter import *
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.state('zoomed')
root.title('Coupled Pendulum Simulation')
root.configure(bg='#0a0f1f')


animation_running = False
time_counter = 0.0


header = Frame(root, bg='#0f162e', height=110, highlightthickness=1, highlightbackground='#1f2a52')
header.pack(fill='x', padx=25, pady=(15, 10))
header.pack_propagate(False)

Label(header, text="Normal Modes of Coupled Pendulum", bg='#0f162e', fg='#5ad1ff',              
      font=('Arial', 30, 'bold')).place(relx=0.5, rely=0.45, anchor='center')


right_panel = Frame(root, bg='#121a33', width=340, highlightthickness=1, highlightbackground='#243566')
right_panel.pack(side='right', fill='y', padx=(0, 30), pady=15)
right_panel.pack_propagate(False)

Label(right_panel, text="FIXED PARAMETERS", bg='#121a33', fg='#4cc9f0', font=('Arial', 15, 'bold')).pack(pady=(35, 15))
Frame(right_panel, bg='#243566', height=1).pack(fill='x', padx=40, pady=(0, 20))

Label(right_panel, text=("•  g  =  9.8  m/s²\n\n•  l  =  0.5  m\n\n•  m  =  1    kg\n\n•  k  =  1    N/m"),
      bg='#121a33', fg='#cfd8ff', font=('Arial', 13), justify='left').pack(padx=40, fill='x')

Label(right_panel, text="INITIAL CONDITIONS", bg='#121a33', fg='#4cc9f0', font=('Arial', 15, 'bold')).pack(pady=(40, 15))
Frame(right_panel, bg='#243566', height=1).pack(fill='x', padx=40, pady=(0, 25))

input_container = Frame(right_panel, bg='#121a33')
input_container.pack(padx=40, fill='x')

def styled_entry(parent, val):
    e = Entry(parent, bg='#1a2447', fg='white', insertbackground='white', relief='flat', font=('Arial', 11))
    e.insert(0, val)
    return e

Label(input_container, text="θ₁ (rad)", bg='#121a33', fg='#e0e6ff', font=('Arial', 11)).grid(row=0, column=0, sticky='w', pady=8)
theta1_entry = styled_entry(input_container, "0.5")
theta1_entry.grid(row=0, column=1, pady=8, ipadx=8, ipady=4)

Label(input_container, text="θ₂ (rad)", bg='#121a33', fg='#e0e6ff', font=('Arial', 11)).grid(row=1, column=0, sticky='w', pady=8)
theta2_entry = styled_entry(input_container, "0.0")
theta2_entry.grid(row=1, column=1, pady=8, ipadx=8, ipady=4)


left_container = Frame(root, bg='#0a0f1f')
left_container.pack(side='left', fill='both', expand=True, padx=(30, 15), pady=15)

sim_canvas = Canvas(left_container, bg='#0d1326', highlightthickness=1, highlightbackground='#243566')
sim_canvas.pack(side='top', fill='both', expand=True)

bottom_half_graph = Frame(left_container, bg='#121a33', height=280, highlightthickness=1, highlightbackground='#243566')
bottom_half_graph.pack(side='bottom', fill='x', pady=(15, 0))
bottom_half_graph.pack_propagate(False)

fig = Figure(figsize=(7, 2.5), facecolor='#121a33')
fig.subplots_adjust(left=0.12, right=0.95, bottom=0.25, top=0.85, wspace=0.35)
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
canvas_plt = FigureCanvasTkAgg(fig, master=bottom_half_graph)
canvas_plt.get_tk_widget().pack(fill='both', expand=True)

def style_axes():
    
    for ax, title, color in [(ax1, "PENDULUM 1", "#5ad1ff"), (ax2, "PENDULUM 2", "#ff5a79")]:
        ax.set_facecolor('#121a33')
        ax.set_title(title, color=color, fontsize=10, fontweight='bold')
        ax.set_xlabel("Time (s)", color='#4cc9f0', fontsize=8)
        ax.set_ylabel("Displacement (rad)", color='#4cc9f0', fontsize=8)
        ax.tick_params(colors='#cfd8ff', labelsize=8)
        ax.grid(True, color='#243566', linestyle='--', alpha=0.3)
        # Ensure box is visible
        for spine in ax.spines.values():
            spine.set_color('#243566')
            spine.set_visible(True)

style_axes()


def draw_spring(canvas, x1, y1, x2, y2, nodes=10, width=15):
    points = []
    dx, dy = (x2 - x1), (y2 - y1)
    dist = math.sqrt(dx**2 + dy**2)
    if dist == 0: dist = 1
    for i in range(nodes + 1):
        px = x1 + dx * (i / nodes)
        py = y1 + dy * (i / nodes)
        if 0 < i < nodes:
            offset = width if i % 2 == 0 else -width
            px += (offset * -dy / dist)
            py += (offset * dx / dist)
        points.extend([px, py])
    return canvas.create_line(points, fill="#4cc9f0", width=2)


def update_sim():
    global animation_running, time_counter
    if not animation_running: return
    g, l, m, k = 9.8, 0.5, 1, 1
    L_pix = 190 
    win_w = sim_canvas.winfo_width()
    if win_w < 10: win_w = 800 
    cx1, cx2 = win_w//2 - 130, win_w//2 + 130
    cy = 70 
    try:
        t1_0, t2_0 = float(theta1_entry.get()), float(theta2_entry.get())
        w1, w2 = math.sqrt(g/l), math.sqrt(g/l + 2*k/m)
        C1, C2 = (t1_0 + t2_0)/2, (t1_0 - t2_0)/2
        time_counter += 0.015 
        th1 = C1 * math.cos(w1 * time_counter) + C2 * math.cos(w2 * time_counter)
        th2 = C1 * math.cos(w1 * time_counter) - C2 * math.cos(w2 * time_counter)
        x1, y1 = cx1 + L_pix * math.sin(th1), cy + L_pix * math.cos(th1)
        x2, y2 = cx2 + L_pix * math.sin(th2), cy + L_pix * math.cos(th2)
        sim_canvas.delete("all")
        sim_canvas.create_rectangle(cx1-120, cy-20, cx2+120, cy, fill="#1f2a52", outline="#243566")
        sim_canvas.create_line(cx1, cy, x1, y1, fill="#cfd8ff", width=2) 
        sim_canvas.create_line(cx2, cy, x2, y2, fill="#cfd8ff", width=2) 
        draw_spring(sim_canvas, x1, y1, x2, y2)
        sim_canvas.create_oval(x1-20, y1-20, x1+20, y1+20, fill="#5ad1ff", outline="white") 
        sim_canvas.create_oval(x2-20, y2-20, x2+20, y2+20, fill="#ff5a79", outline="white") 
        root.after(16, update_sim)
    except: animation_running = False

def onclick():
    global animation_running, time_counter
    try:
        g, l, m, k = 9.8, 0.5, 1, 1
        th1_0, th2_0 = float(theta1_entry.get()), float(theta2_entry.get())
        w1, w2 = math.sqrt(g/l), math.sqrt(g/l + 2*k/m)
        C1, C2 = (th1_0 + th2_0)/2, (th1_0 - th2_0)/2
        t_vals = [i * 0.05 for i in range(500)]
        y1 = [C1 * math.cos(w1 * t) + C2 * math.cos(w2 * t) for t in t_vals]
        y2 = [C1 * math.cos(w1 * t) - C2 * math.cos(w2 * t) for t in t_vals]

        
        ax1.clear(); ax2.clear()
        style_axes() 
        ax1.plot(t_vals, y1, color='#5ad1ff', linewidth=1.5)
        ax2.plot(t_vals, y2, color='#ff5a79', linewidth=1.5)
        canvas_plt.draw()

        animation_running = True
        time_counter = 0.0
        update_sim()
    except ValueError: pass

Button(root, text='Simulate', bg="#162a63", fg="white", activebackground="#1f3c88", 
       relief="flat", bd=0, padx=25, pady=12, font=("Arial", 12, "bold"), 
       cursor="hand2", command=onclick).place(x=1270, y=650)

root.mainloop()
