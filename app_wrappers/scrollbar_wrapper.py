import tkinter as tk
from tkinter import ttk

class ScrollableWrapper(tk.Frame):
    def __init__(self, parent, target_class, *args, **kwargs):
        super().__init__(parent)

        # Create a Canvas widget with a fixed width of 800 and height of 600
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a vertical scrollbar linked to the Canvas
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a Frame inside the canvas
        self.scrollable_frame = tk.Frame(self.canvas)

        # Embed the target class (e.g., DataSyncPage) inside the scrollable frame
        self.target_instance = target_class(self.scrollable_frame, *args, **kwargs)
        self.target_instance.pack(fill="both", expand=True)

        # Add the Frame to the canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Set a default width for the inner frame
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)

        # Ensure the inner frame's width matches the canvas width
        self.canvas.bind("<Configure>", self._fix_inner_width)

    def _update_scroll_region(self, event):
        """Update the scroll region of the canvas to include the entire frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _fix_inner_width(self, event):
        """Fix the inner frame width to match the canvas width."""
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)