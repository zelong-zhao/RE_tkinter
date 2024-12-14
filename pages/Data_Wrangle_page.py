import queue
import re,io,sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..app_wrappers import FlaskServerController

class DataWranglePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.flask_controller = FlaskServerController()
        self.server_status = tk.StringVar(value="Stopped")
        self.log_queue = queue.Queue()

        # Sidebar
        self.folder_path = tk.StringVar()
        self.port_var = tk.StringVar(value="4444")
        self.error_var = tk.StringVar()
        self.is_server_running = False

        title = ttk.Label(self, text="RE EndPoint", font=("Arial", 16, "bold"))
        title.pack(pady=10)


        # Sidebar: Select/Create Folder
        ttk.Label(self, text="Select/Create Folder:").pack(anchor="w", pady=5)
        folder_entry = ttk.Entry(self, textvariable=self.folder_path, width=30,style='Custom.TEntry')
        folder_entry.pack(anchor="w", padx=5)
        ttk.Button(self, text="Browse", command=self.browse_folder).pack(anchor="w", pady=5)

        # Sidebar: Port Selection
        ttk.Label(self, text="Port:").pack(anchor="w", pady=5)
        port_entry = ttk.Entry(self, textvariable=self.port_var, width=10,style='Custom.TEntry')
        port_entry.pack(anchor="w", padx=5)
        ttk.Label(self, textvariable=self.error_var, foreground="red").pack(anchor="w", pady=5)

        port_entry.bind("<FocusOut>", self.validate_port)

        # Sidebar: Start/Stop Server Button
        self.server_button = ttk.Button(self, text="Start Server", command=self.toggle_server)
        self.server_button.pack(anchor="w", pady=5)
        ttk.Label(self, textvariable=self.server_status).pack(anchor="w", pady=5)

        # Main area
        title_label = ttk.Label(self, text="About", font=("Helvetica", 16))
        title_label.pack(pady=10)
        about_text = tk.Text(self, height=5, wrap="word")
        about_text.insert("2.0", "Select Folder (database) to recieve data from port")
        about_text.config(state="disabled")
        about_text.pack(pady=10)

    #     # Terminal output area
    #     ttk.Label(self, text="Terminal Output:").pack(anchor="w", pady=5)
    #     # Create a Text widget to act as a console
    #     self.console_output = tk.Text(self, wrap="word", state="disabled", height=20)
    #     self.console_output.pack(fill="both", expand=True, padx=10, pady=10)
    #     self.redirect_stdout_to_console()


    # def redirect_stdout_to_console(self):
    #     """Redirects the stdout to the Text widget."""
    #     class ConsoleStream(io.StringIO):
    #         def __init__(self, console_widget, app):
    #             super().__init__()
    #             self.console_widget = console_widget
    #             self.app = app

    #         def write(self, s):
    #             # Append text to the console widget and force GUI update
    #             self.console_widget.config(state="normal")
    #             self.console_widget.insert("end", s)
    #             self.console_widget.see("end")
    #             self.console_widget.config(state="disabled")
    #             self.app.update_idletasks()  # Force GUI update to show the text in real-time
        
    #     sys.stdout = ConsoleStream(self.console_output, sys.__stdout__)
    #     sys.stderr = ConsoleStream(self.console_output, sys.__stderr__)



    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select or Create Folder")
        if folder:
            self.folder_path.set(folder)

    def validate_port(self, event=None):
        port = self.port_var.get()
        if re.match(r"^\d{1,5}$", port) and 0 < int(port) <= 65535:
            self.error_var.set("")  # Clear error
        else:
            self.error_var.set("Invalid port. Please enter a valid port number.")

    def toggle_server(self):
        if not self.is_server_running:
            port = self.port_var.get()
            if not self.error_var.get() and self.folder_path.get():  # Only start if port is valid    
                print(f"{port=} or {self.folder_path.get()=} are given")    
                self.flask_controller.start_server(port=port,host='localhost',RE_BOT_word_dir=self.folder_path.get())
                self.server_status.set("Running")
                self.server_button.config(text="Stop Server")
                self.is_server_running = True
            else:
                print(f"{port=} or {self.folder_path.get()=} not given, server failed to start")
        else:
            self.flask_controller.stop_server()
            self.server_status.set("Stopped")
            self.server_button.config(text="Start Server")
            self.is_server_running = False