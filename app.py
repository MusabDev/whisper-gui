import customtkinter as ctk
from tkinter import filedialog, messagebox
import whisper
import threading
import os

WHISPER_MODELS = {
    "tiny": "39 MB",
    "base": "74 MB",
    "small": "244 MB",
    "medium": "769 MB",
    "large": "1550 MB",
    "large-v2": "1550 MB",
    "large-v3": "1550 MB",
    "turbo": "809 MB"
}

class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Whisper Transcriber")
        self.geometry("1000x600")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.model = None
        self.file_path = ""

        self.setup_ui()
        self.disable_inputs()
        threading.Thread(target=self.load_model).start()

    def setup_ui(self):
        # Main layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="Whisper Transcriber", font=("", 18)).pack(pady=(10, 20))

        ctk.CTkLabel(self.sidebar, text="Model:").pack(fill="x")
        self.model_option = ctk.CTkOptionMenu(
            self.sidebar,
            values=[f"{model} ({size})" for model, size in WHISPER_MODELS.items()],
            command=self.model_selection_changed
        )
        self.model_option.set("turbo (809 MB)")
        self.model_option.pack(pady=10, padx=10, fill="x")

        self.progress_label = ctk.CTkLabel(self.sidebar, text="Loading model...")
        self.progress_label.pack()
        self.progress_bar = ctk.CTkProgressBar(self.sidebar, mode="indeterminate")
        self.progress_bar.pack(pady=5, fill="x", padx=10)
        self.progress_bar.start()

        self.select_button = ctk.CTkButton(self.sidebar, text="Select File", command=self.select_file)
        self.select_button.pack(pady=10, padx=10, fill="x")

        self.file_label = ctk.CTkLabel(self.sidebar, text="", wraplength=200)
        self.file_label.pack(pady=5, padx=10, fill="x")

        self.transcribe_button = ctk.CTkButton(self.sidebar, text="Transcribe", command=self.transcribe_thread)
        self.transcribe_button.pack(pady=10, padx=10, fill="x")

        # Text Frame
        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self.text_frame, wrap="word", font=("Arial", 16))
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Copy/Save Button Row (under the textbox)
        self.button_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="e", padx=10, pady=(0, 10))

        self.copy_button = ctk.CTkButton(self.button_frame, text="Copy Text", command=self.copy_text, width=120)
        self.copy_button.pack(side="left", padx=(0, 10))

        self.save_button = ctk.CTkButton(self.button_frame, text="Save as .txt", command=self.save_text, width=120)
        self.save_button.pack(side="left")

    def disable_inputs(self):
        self.select_button.configure(state="disabled")
        self.transcribe_button.configure(state="disabled")
        self.model_option.configure(state="disabled")
        self.copy_button.configure(state="disabled")
        self.save_button.configure(state="disabled")

    def enable_inputs(self):
        self.select_button.configure(state="normal")
        self.transcribe_button.configure(state="normal")
        self.model_option.configure(state="normal")
        self.copy_button.configure(state="normal")
        self.save_button.configure(state="normal")
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.configure(text="Model loaded.")

    def model_selection_changed(self, _):
        self.disable_inputs()
        self.progress_label.configure(text="Loading model...")
        self.progress_bar.pack(pady=5, fill="x", padx=10)
        self.progress_bar.start()
        threading.Thread(target=self.load_model).start()

    def load_model(self):
        try:
            model_name = self.model_option.get().split(" ")[0]
            self.model = whisper.load_model(model_name, download_root="models/")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {e}")
        self.enable_inputs()

    def select_file(self):
        filetypes = [("Media Files", "*.mp3 *.mp4 *.wav *.m4a *.mov *.avi"), ("All files", "*.*")]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self.file_path = path
            self.file_label.configure(text=os.path.basename(path))
            self.textbox.delete("1.0", "end")

    def transcribe_thread(self):
        thread = threading.Thread(target=self.transcribe)
        thread.start()

    def transcribe(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file.")
            return

        self.transcribe_button.configure(state="disabled", text="Transcribing...")
        self.textbox.delete("1.0", "end")

        try:
            result = self.model.transcribe(self.file_path, verbose=False, language=None)

            for segment in result["segments"]:
                self.textbox.insert("end", segment["text"] + " ")
                self.textbox.see("end")
                self.update()

        except Exception as e:
            messagebox.showerror("Error", f"Transcription failed: {e}")

        self.transcribe_button.configure(state="normal", text="Transcribe")

    def copy_text(self):
        text = self.textbox.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo("Copied", "Text copied to clipboard!")

    def save_text(self):
        text = self.textbox.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Warning", "Nothing to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Transcript saved to {file_path}")


if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()
