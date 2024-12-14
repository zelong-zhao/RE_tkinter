import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os,io,sys
from RE_Wrangler.bs4_goofish_clean import clean_downloaded_files,sync_to_wix,load_file,make_csv


# 示例同步函数
def sync_to_wix_wrapper(data_dir, wix_credential_path, wix_media_dir):
    print(f"Syncing {data_dir} to WIX with credentials {wix_credential_path} and media dir {wix_media_dir}...")
    # Your sync logic here
    work_dir=data_dir

    wix_credential=load_file(wix_credential_path)
    wix_media={'filePath':wix_media_dir}
    sync_to_wix(work_dir,wix_credential,wix_media)

# 示例保存 CSV 函数
def save_to_csv(work_dir,csv_path):
    print(f"Saving to CSV: {csv_path}...")
    make_csv(work_dir,csv_path)
    # Your CSV saving logic here

class DataSyncPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.data_dir = tk.StringVar()
        self.wix_credential_path = tk.StringVar()
        self.wix_media_dir = tk.StringVar(value='/RE_BOT')
        self.is_cleaning = False

        # Title
        title = ttk.Label(self, text="Sync to WIX Cloud", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        title = ttk.Label(self, text="Data cleaning", font=("Arial", 14))
        title.pack(pady=10)

        # Data Directory Selection
        ttk.Label(self, text="Data Directory:").pack(anchor="w", padx=10)
        data_dir_entry = ttk.Entry(self, textvariable=self.data_dir, width=50,style='Custom.TEntry')
        data_dir_entry.pack(anchor="w", padx=10, pady=5)
        ttk.Button(self, text="Browse", command=self.select_data_dir).pack(anchor="w", padx=10, pady=5)

        # Clean Button
        self.clean_button = ttk.Button(self, text="Start Cleaning", command=self.toggle_cleaning)
        self.clean_button.pack(anchor="w", padx=10, pady=5)

        title = ttk.Label(self, text="Sync to WIX", font=("Arial", 14))
        title.pack(pady=10)

        # WIX Credential File Selection
        ttk.Label(self, text="WIX Credential File:").pack(anchor="w", padx=10)
        wix_cred_entry = ttk.Entry(self, textvariable=self.wix_credential_path, width=50,style='Custom.TEntry')
        wix_cred_entry.pack(anchor="w", padx=10, pady=5)
        ttk.Button(self, text="Browse", command=self.select_wix_credential).pack(anchor="w", padx=10, pady=5)

        # WIX Media Directory Input
        ttk.Label(self, text="WIX Media Directory:").pack(anchor="w", padx=10)
        wix_media_entry = ttk.Entry(self, textvariable=self.wix_media_dir, width=50,style='Custom.TEntry')
        wix_media_entry.pack(anchor="w", padx=10, pady=5)

        # Sync Button
        ttk.Button(self, text="Start Sync", command=self.start_sync).pack(anchor="w", padx=10, pady=5)

        # Save to CSV

        title = ttk.Label(self, text="Save to CSV", font=("Arial", 14))
        title.pack(pady=10)
        ttk.Button(self, text="Save to CSV", command=self.save_to_csv).pack(anchor="w", padx=10, pady=20)

    #     # Create a Text widget to act as a console
    #     ttk.Label(self, text="Terminal Output:").pack(anchor="w", pady=5)
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
        
    #     sys.stdout = ConsoleStream(self.console_output, self)
    #     sys.stderr = ConsoleStream(self.console_output, self)


    def select_data_dir(self):
        """Select data directory."""
        folder = filedialog.askdirectory(title="Select Data Directory")
        if folder:
            self.data_dir.set(folder)

    def toggle_cleaning(self):
        """Toggle the cleaning process."""
        if not self.data_dir.get():
            messagebox.showerror("Error", "Please select a data directory first.")
            return

        if not self.is_cleaning:
            self.clean_button.config(text="Stop Cleaning")
            self.is_cleaning = True
            clean_downloaded_files(self.data_dir.get())
        else:
            self.clean_button.config(text="Start Cleaning")
            self.is_cleaning = False
            print("Cleaning stopped.")

    def select_wix_credential(self):
        """Select WIX credential file."""
        file = filedialog.askopenfilename(title="Select WIX Credential File", filetypes=[("Text Files", "*.json")])
        if file:
            self.wix_credential_path.set(file)
            self.validate_wix_credential(file)

    def validate_wix_credential(self, file_path):
        """Validate the WIX credential file."""
        required_keys = ["wix-site-id", "Account-ID", "Authorization"]
        try:
            with open(file_path, "r") as file:
                content = file.read()
            missing_keys = [key for key in required_keys if key not in content]
            if missing_keys:
                messagebox.showerror("Error", f"Missing keys in credential file: {', '.join(missing_keys)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading credential file: {e}")

    def start_sync(self):
        """Start syncing to WIX."""
        if not self.data_dir.get() or not self.wix_credential_path.get():
            messagebox.showerror("Error", "Please select both a data directory and a WIX credential file.")
            return

        sync_to_wix_wrapper(self.data_dir.get(), self.wix_credential_path.get(), self.wix_media_dir.get())

    def save_to_csv(self):
        """Save data to a CSV file."""
        file = filedialog.asksaveasfilename(
            title="Save CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")]
        )
        if file:
            save_to_csv(self.data_dir.get(),file)