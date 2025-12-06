# YouTube Downloader

A professional, user-friendly GUI application for downloading YouTube videos and audio using yt-dlp. Built with CustomTkinter for a modern dark-mode interface.

## Features

- **Intuitive GUI**: Easy-to-use interface with dark theme for comfortable usage.
- **Multiple Formats**: Download videos as MP4 or audio as MP3.
- **Quality Selection**:
  - Audio: Best, 320kbps, 128kbps
  - Video: Best, 720p, 1080p
- **Batch Downloads**: Enter multiple URLs separated by commas for queue processing.
- **Custom Output Directory**: Choose where to save your downloads.
- **Progress Tracking**: Real-time progress bar and status updates.
- **Thumbnail Preview**: View video thumbnails before downloading.
- **Error Handling**: Clear error messages for invalid URLs or network issues.
- **No CLI Required**: Pure GUI application, no command-line knowledge needed.

## Requirements

- Python 3.7+
- FFmpeg (for video processing and audio extraction)

## Installation

1. **Clone or Download** the repository.
2. **Install Python dependencies**:
   ```bash
   pip install customtkinter yt-dlp requests Pillow
   ```
3. **Install FFmpeg**:
   - Download from [FFmpeg official site](https://ffmpeg.org/download.html).
   - Add to PATH or configure yt-dlp to find it.

4. Run the application:
   ```bash
   python yt_downloader.py
   ```

## Building Standalone Executable

To create a standalone Windows executable (.exe) file:

1. **Install PyInstaller** (if not already installed):
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**:
   - On Windows, execute `build.bat` in the project directory.
   - Alternatively, manually run:
     ```bash
     pyinstaller --onefile --windowed yt_downloader.py
     ```

3. The executable will be created in the `dist` folder as `yt_downloader.exe`.

**Notes:**
- The executable bundles Python and dependencies, but still requires FFmpeg to be installed on the system for audio/video processing.
- Run the .exe file directly - no Python installation needed on the target machine.
- For other platforms, modify the PyInstaller command accordingly (remove `--windowed` on non-Windows if you want console output).

## Usage

1. Launch the application.
2. Enter YouTube URLs in the text box, separated by commas.
3. Select download type: Audio (MP3) or Video (MP4).
4. Choose quality from the dropdown.
5. Set the output directory using the Browse button (defaults to Downloads).
6. Click "Download" to start.
7. Monitor progress via the progress bar and status messages.
8. Thumbnails will appear for downloaded videos.

## Screenshots

*(Add screenshots here if available)*

## Known Limitations

- Requires internet connection for downloads.
- FFmpeg must be installed for proper video merging and audio extraction.
- yt-dlp respects YouTube's terms; only download content you have rights to.

## Troubleshooting

### FFmpeg not found
Ensure FFmpeg is installed and accessible. You can specify the path if needed by modifying the code or using yt-dlp configuration.

### Download fails
- Check internet connection.
- Verify URLs are valid YouTube links.
- Ensure sufficient disk space in output directory.
- For videos, some formats may not be available; try lower quality.

### GUI doesn't start
Run the script and check for error messages in the console.

## Contributing

Contributions welcome! Please fork the repository and submit pull requests with improvements.

## License

This project is open-source under the MIT License.

## Disclaimer

This tool is for educational purposes. Respect copyright laws and YouTube's terms of service. The author is not responsible for misuse.

## Changelog

- v1.0: Initial GUI release with core download functionality.
