import tkinter as tk

root = tk.Tk()
root["title"] = "Radio button"

opcion = tk.StringVar(value="Opcio0")
radio1 = tk.Radiobutton(root, text="Opcio 1", variable=opcion, value="Opcio1")
radio2 = tk.Radiobutton(root, text="Opcio2", variable=opcion, value="Opcio2")
radio3 = tk.Radiobutton(root, text="Opcio3", variable=opcion, value="Opcio3")

radio1.pack()
radio2.pack()
radio3.pack()
root.mainloop()