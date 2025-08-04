import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class BatchRenamerApp(tk.Tk):
    """
    A simple GUI application for batch renaming files in a directory.
    """
    def __init__(self):
        super().__init__()
        self.title("Batch File Renamer")
        self.geometry("700x500")

        self.directory = ""
        self.file_list = []
        self.create_widgets()
    
    def create_widgets(self):
        """
        Creates all the widgets for the application window.
        """
        # Main frame for padding
        main_frame = tk.Frame(self, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Directory selection frame
        dir_frame = tk.Frame(main_frame)
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(dir_frame, text="Folder:").pack(side=tk.LEFT)
        self.dir_entry = tk.Entry(dir_frame, width=60)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.dir_entry.insert(0, "Select a directory to start...")
        self.dir_entry.config(state='readonly')

        browse_button = tk.Button(dir_frame, text="Browse", command=self.browse_directory)
        browse_button.pack(side=tk.LEFT)

        # Options frame for renaming rules
        options_frame = tk.LabelFrame(main_frame, text="Renaming Options", padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))

        # Prefix
        prefix_frame = tk.Frame(options_frame)
        prefix_frame.pack(fill=tk.X, pady=5)
        tk.Label(prefix_frame, text="Prefix:").pack(side=tk.LEFT)
        self.prefix_entry = tk.Entry(prefix_frame, width=40)
        self.prefix_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.prefix_entry.bind("<KeyRelease>", self.update_preview)

        # Suffix
        suffix_frame = tk.Frame(options_frame)
        suffix_frame.pack(fill=tk.X, pady=5)
        tk.Label(suffix_frame, text="Suffix:").pack(side=tk.LEFT)
        self.suffix_entry = tk.Entry(suffix_frame, width=40)
        self.suffix_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.suffix_entry.bind("<KeyRelease>", self.update_preview)

        # Find and Replace
        find_replace_frame = tk.Frame(options_frame)
        find_replace_frame.pack(fill=tk.X, pady=5)
        tk.Label(find_replace_frame, text="Replace:").pack(side=tk.LEFT)
        self.find_entry = tk.Entry(find_replace_frame, width=20)
        self.find_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.find_entry.bind("<KeyRelease>", self.update_preview)
        
        tk.Label(find_replace_frame, text="With:").pack(side=tk.LEFT)
        self.replace_entry = tk.Entry(find_replace_frame, width=20)
        self.replace_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.replace_entry.bind("<KeyRelease>", self.update_preview)

        # Preview frame
        preview_frame = tk.LabelFrame(main_frame, text="Preview", padx=10, pady=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.preview_text = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, state='disabled')
        self.preview_text.pack(fill=tk.BOTH, expand=True)

        # Action buttons frame
        actions_frame = tk.Frame(main_frame)
        actions_frame.pack(fill=tk.X)

        self.rename_button = tk.Button(actions_frame, text="Rename Files", command=self.rename_files, state='disabled')
        self.rename_button.pack(side=tk.RIGHT)

        tk.Label(actions_frame, text="Status:").pack(side=tk.LEFT)
        self.status_label = tk.Label(actions_frame, text="Awaiting directory selection.", fg="blue")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))

    def browse_directory(self):
        """
        Opens a file dialog to select the directory and updates the GUI.
        """
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.dir_entry.config(state='normal')
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, self.directory)
            self.dir_entry.config(state='readonly')
            self.list_files()
            self.update_preview()
            self.rename_button.config(state='normal')
            self.status_label.config(text="Directory selected.", fg="green")
        else:
            self.status_label.config(text="Directory selection cancelled.", fg="red")

    def list_files(self):
        """
        Populates a list of files from the selected directory.
        """
        self.file_list = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]
        
    def get_new_filename(self, old_filename):
        """
        Applies all renaming rules to a given filename.
        """
        base_name, extension = os.path.splitext(old_filename)
        
        # Find and Replace
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        if find_text:
            base_name = base_name.replace(find_text, replace_text)
            
        # Prefix and Suffix
        new_name = self.prefix_entry.get() + base_name + self.suffix_entry.get()
        
        # Keep the original extension
        return new_name + extension

    def update_preview(self, event=None):
        """
        Updates the preview text area with old and new filenames.
        """
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        
        if not self.file_list:
            self.preview_text.insert(tk.END, "No files found in the selected directory.")
        else:
            preview_content = ""
            for filename in self.file_list:
                new_filename = self.get_new_filename(filename)
                preview_content += f"{filename} -> {new_filename}\n"
            self.preview_text.insert(tk.END, preview_content)
            
        self.preview_text.config(state='disabled')
        
    def rename_files(self):
        """
        Executes the file renaming based on the current rules.
        """
        if not self.file_list:
            messagebox.showwarning("Warning", "No files to rename.")
            return

        try:
            for filename in self.file_list:
                old_path = os.path.join(self.directory, filename)
                new_filename = self.get_new_filename(filename)
                new_path = os.path.join(self.directory, new_filename)

                if old_path != new_path:
                    os.rename(old_path, new_path)
            
            messagebox.showinfo("Success", f"Successfully renamed {len(self.file_list)} files.")
            self.status_label.config(text="Renaming complete.", fg="green")
            self.list_files()
            self.update_preview()
            
        except OSError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text="Renaming failed.", fg="red")
        
if __name__ == "__main__":
    app = BatchRenamerApp()
    app.mainloop()
