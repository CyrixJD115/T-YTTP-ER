# process.py

from PySide6.QtCore import QThread, Signal
import time
from function import read_file_with_fallback

class ProcessingWorker(QThread):
    update_progress = Signal(int, int)  # current, total
    update_text = Signal(str)
    update_status = Signal(str, str)  # message, color

    def __init__(self, parent, video_url):
        super().__init__()
        self.parent = parent
        self.video_url = video_url
        self.cancel = False

    def run(self):
        try:
            self.update_status.emit("Extracting transcript...", "white")
            transcript_file, video_id, video_title = self.parent.handler.extract_and_save_transcript(self.video_url)

            self.parent.processing_screen.video_id = video_id
            self.parent.processing_screen.video_title = video_title

            self.update_status.emit("Splitting transcript...", "white")
            chunk_files = self.parent.handler.split_transcript(transcript_file)
            total_chunks = len(chunk_files)

            for idx, chunk_file in enumerate(chunk_files):
                if self.cancel:
                    self.update_status.emit("Processing cancelled", "#ff7373")
                    return

                self.update_progress.emit(idx + 1, total_chunks)
                self.update_text.emit(f"\n--- Chunk {idx+1} Response ---\n\n")

                generated_text = self.parent.handler.process_single_chunk(chunk_file)
                speed = self.parent.config.settings.get("typewriter_speed", 2)

                for char in generated_text:
                    if self.cancel:
                        break
                    self.update_text.emit(char)
                    time.sleep(speed / 1000.0)

                if self.cancel:
                    self.update_status.emit("Processing cancelled", "#ff7373")
                    return

            self.update_status.emit("Processing complete", "#b5e0a8")

        except Exception as e:
            self.update_status.emit(f"Error: {e}", "#ff7373")


def combine_output(parent, video_id, video_title, status_callback):
    parent.handler.combine_chunks_to_output(video_id, video_title, status_callback)
