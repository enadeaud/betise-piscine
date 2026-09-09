import tkinter
from tkinter import ttk
import random
import math

clicks = 0

def click_handler(event):
	global clicks
	if event.num == 1:
		clicks += 1

def move_window():
	global window_x, window_y, x_updater, y_updater

	if clicks == 42:
		root.quit()
		return

	if window_x >= screen_width or window_x <= 0:
		x_updater = -x_updater
	if window_y >= screen_height or window_y <= 0:
		y_updater = -y_updater

	window_x += x_updater
	window_y += y_updater

	window_x_int = int(window_x)
	window_y_int = int(window_y)
	
	root.geometry(f'+{window_x_int}+{window_y_int}')

	healthbar["value"] = 42 - clicks
	root.after(10, move_window)

root = tkinter.Tk()
root.overrideredirect(True)
root.geometry("200x200")
root.bind("<Button-1>", click_handler)

shrek = tkinter.PhotoImage(file=".media/shrek.png")
label = tkinter.Label(root, image=shrek)
label.pack()

screen_width = root.winfo_screenwidth() - 200
screen_height = root.winfo_screenheight() - 200
window_x = random.randint(0, screen_width)
window_y = random.randint(0, screen_height)
theta = random.uniform(0, 2 * math.pi)
v = random.randint(10, 20)
x_updater = v * math.cos(theta)
y_updater = v * math.sin(theta)

s = ttk.Style()
s.configure("red.Horizontal.TProgressbar", troughcolor ='gray', background='red')
healthbar = ttk.Progressbar(root, style="red.Horizontal.TProgressbar", maximum=42, value=42)
healthbar.place(x=0, y=0, width=200)

root.after(10, move_window)
root.mainloop()
