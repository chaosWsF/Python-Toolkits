# Online Image Scrapper

## Features

### Multi-threaded Downloading

- Python’s `threading` module or a library like `concurrent.futures` to parallelize image downloads.
- Multi-threading or asynchronous I/O (e.g., with `asyncio` and `aiohttp`)

### Retry Mechanism for Reliability

- Apply a `@retry` decorator (likely from the `retrying` library) to functions like `downloadImg`, with configurable delays (e.g., 1 second). This ensures robustness when fetching resources.

### Image Processing and Storage

- Use `img2pdf` to convert images into PDFs.
- Images are saved to a local directory.
- `Pillow`

### Error Handling and Logging

- `logging`

### Checksum Validation

- It validates downloaded content using checksums to ensure integrity.
