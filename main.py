import tkinter as tk
from dashboard import Dashboard

def main():
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
