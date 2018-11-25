from tkinter import *

root = Tk()
root.title("A Cube VOXEL")
root.geometry("800x800")

root.fileName = filedialog.askopenfilename \
        (filetypes=(("stl files", ".stl")))

print(root.fileName)









root.mainloop()