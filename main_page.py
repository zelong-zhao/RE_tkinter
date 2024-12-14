import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .pages import DataWranglePage,DataSyncPage
from .app_wrappers import ScrollableWrapper

# Sidebar button action handlers
def show_page(page_name):
    """Switch to the selected page."""
    for frame in pages.values():
        frame.grid_forget()
    pages[page_name].grid(row=0, column=1, sticky="nsew")

# Main Application
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RE Bot")
        self.geometry("800x600")

        # Sidebar
        sidebar = tk.Frame(self, width=200, bg="gray")
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)

        ####
        style = ttk.Style()
        style.configure("TLabel", foreground="black", background="white")  # 黑字白底
        style.configure("TButton", foreground="black", background="white")  # 黑字白底
        # 配置窗口背景颜色
        self.configure(bg="white")
        style.configure("Custom.TEntry", foreground="black", fieldbackground="white")


        ttk.Button(sidebar, text="Data Wrangle", command=lambda: show_page("data_wrangling")).pack(fill="x", pady=5)
        ttk.Button(sidebar, text="Data Sync", command=lambda: show_page("data_sync")).pack(fill="x", pady=5)

        # Pages container
        container = tk.Frame(self,)
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Pages
        global pages
        pages = {
            "data_wrangling": DataWranglePage(container, self),
            "data_sync": DataSyncPage(container, self)
        }


        for page in pages.values():
            page.grid(row=0, column=1, sticky="nsew")

        # Show default page
        show_page("data_wrangling")

# Run the application
if __name__ == "__main__":

    app = MainApp()
    app.mainloop()