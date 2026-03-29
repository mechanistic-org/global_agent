import os
import time
import logging
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s | Watchdog | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

ENOS_ROOT = Path(__file__).parent.parent.absolute()
INBOX_DIR = ENOS_ROOT / "inbox"
ARCHIVE_DIR = ENOS_ROOT / "archive"
ENV_FILE = ENOS_ROOT / ".env"

INBOX_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

class IngestHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        
        path = Path(event.src_path)
        if path.suffix.lower() not in [".txt", ".md", ".pdf"]:
            return
            
        logger.info(f"Detected new asset: {path.name}")
        # Small delay to ensure the file handle is completely released after copy
        time.sleep(1.5)
        
        # Fire NanoClaw
        logger.info(f"Igniting NanoClaw Ingestion for {path.name}...")
        
        cmd = [
            "docker", "run", "--rm",
            "--env-file", str(ENV_FILE),
            "-e", f"TARGET_ASSET=/inbox/{path.name}",
            "-e", "ROUTER_SSE_URL=http://host.docker.internal:8000/sse",
            "-v", f"{INBOX_DIR}:/inbox",
            "-v", f"{ENOS_ROOT / 'registry'}:/registry",
            "-v", f"{ENOS_ROOT / 'output'}:/output",
            "en-os:latest",
            "--mode", "ingest"
        ]
        
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                logger.info(f"NanoClaw Success for {path.name}.")
                
                # Move to archive
                safe_time = time.strftime("%Y%m%d_%H%M%S")
                dest = ARCHIVE_DIR / f"{safe_time}_{path.name}"
                
                # Handling moves safely (e.g. windows cross-drive or locks)
                try:
                    path.rename(dest)
                except Exception as e:
                    import shutil
                    logger.warning(f"Rename failed across bounds, falling back to shutil: {e}")
                    shutil.move(str(path), str(dest))
                    
                logger.info(f"Archived asset to {dest.name}")
            else:
                logger.error(f"NanoClaw Failed for {path.name} (Exit Code {res.returncode})")
                logger.error(f"Stderr: {res.stderr.strip()}")
                logger.info(f"Leaving {path.name} in inbox/ for human review.")
        except Exception as e:
            logger.error(f"Failed to spawn Docker process for {path.name} - {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(IngestHandler(), str(INBOX_DIR), recursive=False)
    observer.start()
    logger.info(f"Ingest Watchdog active. Monitoring {INBOX_DIR} for [.txt, .md, .pdf] ...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Watchdog shutting down.")
    observer.join()
