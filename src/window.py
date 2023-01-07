import tkinter as tk
from tkinter.filedialog import Open, SaveAs


def do_something():
    print("Doing something")


def open_file():
    filename = Open().show()
    with open(filename, "r") as f:
        print(f.read())


def save_file():
    filename = SaveAs().show()
    with open(filename, "w") as f:
        f.write("Hello World")


def open_window():
    window = tk.Tk()
    window.title("ModernGL Window")
    window.geometry("800x600")

    # Create a canvas
    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()

    # Create a frame
    frame = tk.Frame(window)
    frame.pack()

    # Create a button
    button = tk.Button(frame, text="Quit", command=window.destroy)
    button.pack()

    # Create a label
    label = tk.Label(frame, text="Hello World")
    label.pack()

    # Create a menu
    menu = tk.Menu(window)
    window.config(menu=menu)

    # Create a submenu
    submenu = tk.Menu(menu)
    menu.add_cascade(label="File", menu=submenu)
    submenu.add_command(label="Open", command=open_file)
    submenu.add_command(label="Save", command=save_file)
    submenu.add_separator()
    submenu.add_command(label="Exit", command=window.destroy)

    # Create a toolbar
    toolbar = tk.Frame(window, bg="blue")
    insert_button = tk.Button(toolbar, text="Insert Image", command=do_something)
    insert_button.pack(side=tk.LEFT, padx=2, pady=2)
    print_button = tk.Button(toolbar, text="Print", command=do_something)
    print_button.pack(side=tk.LEFT, padx=2, pady=2)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    # Create a status bar
    status = tk.Label(window, text="Preparing to do nothing...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(side=tk.BOTTOM, fill=tk.X)

    window.mainloop()
