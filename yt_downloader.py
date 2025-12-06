import customtkinter as ctk
import yt_dlp
import os
import threading
import requests
from PIL import Image, ImageTk
from io import BytesIO

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class YoutubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader")
        self.geometry("800x600")
        self.resizable(True, True)

        # URL input
        self.url_label = ctk.CTkLabel(self, text="YouTube URLs (separate with comma):")
        self.url_label.pack(pady=10)
        self.url_entry = ctk.CTkTextbox(self, height=100)
        self.url_entry.pack(pady=5, padx=20, fill="x")

        # Download type
        self.type_frame = ctk.CTkFrame(self)
        self.type_frame.pack(pady=10, padx=20, fill="x")
        self.type_label = ctk.CTkLabel(self.type_frame, text="Download Type:")
        self.type_label.grid(row=0, column=0, padx=10)
        self.download_type = ctk.StringVar(value="audio")
        self.audio_radio = ctk.CTkRadioButton(self.type_frame, text="Audio (MP3)", variable=self.download_type, value="audio", command=self.update_quality_options)
        self.audio_radio.grid(row=0, column=1, padx=10)
        self.video_radio = ctk.CTkRadioButton(self.type_frame, text="Video (MP4)", variable=self.download_type, value="video", command=self.update_quality_options)
        self.video_radio.grid(row=0, column=2, padx=10)

        # Quality selection
        self.quality_label = ctk.CTkLabel(self, text="Quality:")
        self.quality_label.pack(pady=5)
        self.quality_var = ctk.StringVar(value="best")
        self.quality_dropdown = ctk.CTkOptionMenu(self, values=["best", "720p", "1080p"], variable=self.quality_var)
        self.quality_dropdown.pack(pady=5)
        self.update_quality_options()

        # Output directory
        self.path_label = ctk.CTkLabel(self, text="Output Directory:")
        self.path_label.pack(pady=5)
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(pady=5, padx=20, fill="x")
        self.path_entry = ctk.CTkEntry(self.path_frame, placeholder_text="Select output directory...")
        self.path_entry.insert(0, os.path.expanduser("~\\Downloads"))
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.browse_button = ctk.CTkButton(self.path_frame, text="Browse", command=self.browse_folder, width=80)
        self.browse_button.pack(side="right", padx=10)

        # Download button
        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download, height=50)
        self.download_button.pack(pady=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)

        # Status
        self.status_label = ctk.CTkLabel(self, text="Ready to download", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)

        # Thumbnail display (placeholder)
        self.thumbnail_label = ctk.CTkLabel(self, text="Thumbnail will appear here", width=160, height=90)
        self.thumbnail_label.pack(pady=10)

    def browse_folder(self):
        folder = ctk.filedialog.askdirectory()
        if folder:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder)

    def start_download(self):
        urls = self.url_entry.get("1.0", "end-1c").strip()
        if not urls:
            self.status_label.configure(text="Error: Please enter URLs")
            return
        url_list = [u.strip() for u in urls.split(",") if u.strip()]
        if not url_list:
            self.status_label.configure(text="Error: No valid URLs provided")
            return
        download_type = self.download_type.get()
        quality = self.quality_var.get()
        output_dir = self.path_entry.get()
        if not os.path.isdir(output_dir):
            self.status_label.configure(text="Error: Invalid output directory")
            return
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")
        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Starting download...")
        threading.Thread(target=self.download, args=(url_list, download_type, quality, outtmpl)).start()

    def download(self, urls, download_type, quality, outtmpl):
        try:
            if download_type == "video":
                if quality == "720p":
                    fmt = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif quality == "1080p":
                    fmt = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                else:
                    fmt = 'bestvideo+bestaudio/best'
                ydl_opts = {
                    'format': fmt,
                    'merge_output_format': 'mp4',
                    'outtmpl': outtmpl,
                    'quiet': True,
                    'noplaylist': True
                }
            else:
                # Audio
                if quality != "best":
                    pref_bitrate = int(quality[:-1])   # e.g., 320k -> 320
                    ydl_opts = {
                        'format': f'bestaudio[abr<={pref_bitrate}]/best[abr<={pref_bitrate}]',
                        'outtmpl': outtmpl,
                        'quiet': True,
                        'noplaylist': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': str(pref_bitrate),
                        }]
                    }
                else:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': outtmpl,
                        'quiet': True,
                        'noplaylist': True,
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                        }]
                    }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for i, url in enumerate(urls):
                    self.update_status(f"Downloading {i+1}/{len(urls)}: {url[:50]}...")
                    ydl.download([url])
                    self.progress_bar.set((i+1)/len(urls))
                    # Load thumbnail for the last video or all? Simple for last
                    info = ydl.extract_info(url, download=False)
                    thumb_url = info.get('thumbnail')
                    if thumb_url:
                        self.load_thumbnail(thumb_url)
            self.progress_bar.set(1)
            self.update_status("All downloads completed!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        finally:
            self.download_button.configure(state="normal")

    def update_status(self, text):
        self.status_label.configure(text=text)

    def load_thumbnail(self, url):
        try:
            response = requests.get(url, timeout=10)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((160, 90))
            photo = ImageTk.PhotoImage(img)
            self.thumbnail_label.configure(image=photo, text="")
            self.thumbnail_label.image = photo  # Keep reference
        except Exception as e:
            self.thumbnail_label.configure(text="Failed to load thumbnail")

    def update_quality_options(self):
        if self.download_type.get() == "audio":
            self.quality_dropdown.configure(values=["best", "320k", "128k"])
        else:
            self.quality_dropdown.configure(values=["best", "720p", "1080p"])
        self.quality_var.set("best")

if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
