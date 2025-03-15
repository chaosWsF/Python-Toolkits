# Python Toolkits

A collection of Python-based utilities for password generation, web scraping, and media processing. Detailed documentation, including setup and usage guides, is available in the [Wiki](https://github.com/chaosWsF/Python-Toolkits/wiki).

## Installation

1. **Prerequisites**:
   - Python >= 3.9
   - `ffmpeg` >= 6.0:
     - **macOS**: `brew install ffmpeg`
     - **Windows**: `winget install Gyan.FFmpeg`

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

Verify setup:
- `python --version`
- `ffmpeg -version`

## Tools

### Password Generator
Generate secure passwords with customizable options.
- **Run**: `python pwd_generator.py --length 12 --symbols --lowercase`
- **Details**: [Wiki - Password Generator](https://github.com/chaosWsF/Python-Toolkits/wiki/Password-Generator)

### Instagram Scrapper
Download images from Instagram posts.
- **Structure**:
  ```
  instagram_scrapper/
  ├── downloads/          # Output directory
  ├── photos_combiner.py  # Combines downloaded images
  ├── playwright_scrapper.py  # In development
  ├── public_scrapper.py      # In development
  └── test_login_page.py      # Test script
  ```
- **Details**: [Wiki - Instagram Scrapper](https://github.com/chaosWsF/Python-Toolkits/wiki/Instagram-Scrapper)

### Video Scrapper
A Flask-based web UI for downloading videos.
- **Run**: `python video_scrapper/app.py` (after setup)
- **Setup**: Requires `FLASK_SECRET_KEY` and `FLASK_PORT` in `.env`. See Wiki.
- **Details**: [Wiki - Video Scrapper](https://github.com/chaosWsF/Python-Toolkits/wiki/Video-Scrapper)

### Image Scrapper
Download images from various sources (in progress).
- **Details**: [Wiki - Image Scrapper](https://github.com/chaosWsF/Python-Toolkits/wiki/Image-Scrapper)

### Requirements Generator
Maintain `requirements.txt` for cross-platform compatibility.
- **Clean Requirements**: Convert Conda file URIs to versioned entries:
  ```bash
  python clean_requirements.py
  ```
- **Merge Requirements**: Combine Windows 11 and macOS requirements:
  ```bash
  python merge_requirements.py
  ```
- **Details**: [Wiki - Requirements Generator](https://github.com/chaosWsF/Python-Toolkits/wiki/Requirements-Generator)

## Contributing
Suggestions or issues? Open a [GitHub Issue](https://github.com/chaosWsF/Python-Toolkits/issues).
