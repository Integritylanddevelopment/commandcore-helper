#!/usr/bin/env python3

import pyautogui
import mss
import os
import time
from datetime import datetime
import subprocess
from pynput import mouse
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import logging
import re
import concurrent.futures
from google.cloud import vision
import pytesseract

# === CONFIG ===
output_dir = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_logs"
summary_script = r"D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/logs/summary/summary_scripts/summary.py"
tags = ["copilot_multimonitor_scroll"]
scrolls = 500
scroll_pause = 0.2
capture_width = 500

clicked_position = None
region_box = None

# Set up Google Vision API client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "d:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/full_chat/full_chat_scripts/google_service_account_key.json"
client = vision.ImageAnnotatorClient()

# === LOGGING SETUP ===
logging.basicConfig(
    filename=os.path.join(output_dir, "copilot_chat_capture.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def on_click(x, y, button, pressed):
    global clicked_position
    if pressed:
        clicked_position = (x, y)
        logging.info(f"Click detected at position: {clicked_position}")
        return False

def get_mouse_click():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return clicked_position

def find_monitor_containing(x, y):
    with mss.mss() as sct:
        for monitor in sct.monitors:
            left, top, width, height = monitor["left"], monitor["top"], monitor["width"], monitor["height"]
            if left <= x < left + width and top <= y < top + height:
                logging.info(f"Monitor found for position ({x}, {y}): {monitor}")
                return monitor
        logging.warning("No specific monitor found, defaulting to primary monitor.")
        return sct.monitors[0]

def wait_for_bounding_box():
    print("🖱 Click TOP boundary...")
    top_click = get_mouse_click()
    print("🖱 Click LEFT boundary...")
    left_click = get_mouse_click()
    print("🖱 Click RIGHT boundary...")
    right_click = get_mouse_click()
    print("🖱 Click BOTTOM boundary...")
    bottom_click = get_mouse_click()

    global region_box
    region_box = {
        'top': top_click[1],
        'left': left_click[0],
        'width': right_click[0] - left_click[0],
        'height': bottom_click[1] - top_click[1]
    }

    if region_box['width'] <= 0 or region_box['height'] <= 0:
        logging.error(f"Invalid bounding box dimensions: {region_box}")
        raise ValueError("Bounding box dimensions must be positive.")

    logging.info(f"Capture region defined: {region_box}")
    print(f"Bounding box coordinates: {region_box}")

def capture_region():
    try:
        logging.info(f"Capturing region: {region_box}")
        with mss.mss() as sct:
            if region_box['width'] <= 0 or region_box['height'] <= 0:
                raise ValueError("Region dimensions must be positive.")
            img = sct.grab(region_box)
            return Image.open(BytesIO(mss.tools.to_png(img.rgb, img.size)))
    except Exception as e:
        logging.error(f"Error capturing region: {e}")
        raise

def scroll_up():
    try:
        logging.info("Attempting to scroll up...")

        # Validate region_box dimensions
        if not region_box or region_box['width'] <= 0 or region_box['height'] <= 0:
            logging.error(f"Invalid or undefined region_box dimensions: {region_box}")
            raise ValueError("Region dimensions must be positive and defined.")

        # Debugging: Capture region before scrolling
        debug_pre_scroll_path = os.path.join(output_dir, "debug_pre_scroll_capture.png")
        pre_scroll_frame = capture_region()
        pre_scroll_frame.save(debug_pre_scroll_path)
        logging.info(f"Saved pre-scroll region to: {debug_pre_scroll_path}")

        # Perform scrolling
        try:
            pyautogui.scroll(3000)
            logging.info("Scroll action performed successfully.")
        except Exception as scroll_error:
            logging.error(f"Error during scroll action: {scroll_error}")
            raise

        time.sleep(scroll_pause)

        # Debugging: Capture region after scrolling
        debug_post_scroll_path = os.path.join(output_dir, "debug_post_scroll_capture.png")
        post_scroll_frame = capture_region()
        post_scroll_frame.save(debug_post_scroll_path)
        logging.info(f"Saved post-scroll region to: {debug_post_scroll_path}")

        # Verify scroll success
        if not verify_scroll_success():
            logging.warning("Scrolling did not change content. Retrying...")
            pyautogui.scroll(3000)
            time.sleep(scroll_pause)
            if not verify_scroll_success():
                raise RuntimeError("Scrolling failed to change content after retry.")

    except Exception as e:
        logging.error(f"Error during scrolling: {e}")
        raise

previous_text = ""

def verify_scroll_success():
    global previous_text
    try:
        logging.info("Capturing region for scroll verification...")
        current_frame = capture_region()

        # Debugging: Save current frame for verification
        debug_verify_path = os.path.join(output_dir, "debug_verify_capture.png")
        current_frame.save(debug_verify_path)
        logging.info(f"Saved verification region to: {debug_verify_path}")

        try:
            current_text = pytesseract.image_to_string(current_frame).strip()
            logging.info(f"Captured text: {current_text}")
        except Exception as ocr_error:
            logging.error(f"OCR error during verification: {ocr_error}")
            current_text = ""

        if current_text:
            if current_text != previous_text:
                previous_text = current_text
                logging.info("Content changed after scrolling.")
                return True
            else:
                logging.warning("Content did not change after scrolling.")
                return False
        else:
            logging.warning("No text detected in the captured region.")
            return False
    except Exception as e:
        logging.error(f"Error during scroll verification: {e}")
        return False

def preprocess_image(img):
    try:
        logging.info("Starting image preprocessing...")
        if img.mode != "L":
            img = img.convert("L")
        img = img.point(lambda x: 0 if x < 128 else 255, "1")
        img = img.convert("L")
        img = ImageEnhance.Contrast(img).enhance(2.0)
        img = img.filter(ImageFilter.MedianFilter(size=3))
        return img
    except Exception as e:
        logging.error(f"Error during image preprocessing: {e}")
        raise

def extract_chat_ocr():
    collected_text = []
    try:
        for i in range(scrolls):
            logging.info(f"Processing frame {i+1}/{scrolls}")
            img = capture_region()
            img = preprocess_image(img)
            try:
                text = pytesseract.image_to_string(img).strip()
                logging.info(f"Extracted text: {text}")
                if text and text not in collected_text:
                    collected_text.append(text)
            except Exception as e:
                logging.error(f"OCR error frame {i+1}: {e}")
            scroll_up()
        logging.info("OCR extraction complete.")
    except Exception as e:
        logging.error(f"Fatal OCR error: {e}")
        raise
    return "\n\n".join(reversed(collected_text))

def extract_chat_ocr_parallel(click_x, click_y):
    def process_frame(frame_number):
        logging.info(f"Processing frame {frame_number}")
        img = capture_region()
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_content = img_byte_arr.getvalue()
        image = vision.Image(content=img_content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            return texts[0].description.strip()
        return ""

    collected_text = []
    previous_text = None
    frame_number = 0

    logging.info("Starting OCR extraction with dynamic scrolling.")
    while True:
        frame_number += 1
        logging.info(f"Scrolling frame {frame_number}")
        scroll_up()
        try:
            text = process_frame(frame_number)
            if text and text != previous_text:
                collected_text.append(text)
                previous_text = text
            else:
                logging.info("No new text detected, stopping scrolling.")
                break
        except Exception as e:
            logging.error(f"Error processing frame {frame_number}: {e}")
            break

    logging.info("OCR extraction completed.")
    return "\n\n".join(reversed(collected_text))

def generate_title_from_text(text):
    """
    Generate a summary title for the markdown file based on the content.
    Prioritizes lines that contain actual action or speech.
    Args:
        text (str): Extracted text to analyze.
    Returns:
        str: Generated title summarizing the content.
    """
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 10 and not line.strip().isdigit()]
    important = [line for line in lines if "said:" in line or "click" in line.lower()]
    if important:
        title = important[0]
    elif lines:
        title = lines[0]
    else:
        title = "Captured Chat Log"
    return sanitize_filename(title[:100])

def sanitize_filename(filename):
    """
    Sanitize the filename by removing invalid characters.
    Args:
        filename (str): Original filename.
    Returns:
        str: Sanitized filename.
    """
    sanitized = re.sub(r'[\\/:*?"<>|]', '_', filename)
    return sanitized[:100]

def save_markdown(text):
    """
    Save the extracted text into a markdown file with a generated title.
    Args:
        text (str): Extracted text to save.
    Returns:
        str: Path to the saved markdown file.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"log_{chr(97 + (int(timestamp.replace('-', '').replace(':', '').replace('_', '')) % 26))}.md"
        output_path = os.path.join(output_dir, filename)

        os.makedirs(output_dir, exist_ok=True)
        token_count = len(text.split())

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"source: copilot-multi\n")
            f.write(f"timestamp: {timestamp.replace('_', ' ')}\n")
            f.write(f"window_title: {filename}\n")
            f.write("vector_ready: true\n")
            f.write(f"tags: {tags}\n")
            f.write("---\n\n")
            f.write(f"# {filename}\n\n")
            f.write(text + "\n\n")
            f.write(f"---\nEstimated Token Count: {token_count}\n")

        logging.info(f"Log saved to: {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error saving markdown: {e}")
        raise

def sync_to_vector_database(markdown_path):
    logging.info(f"Syncing markdown file to vector database: {markdown_path}")
    # Placeholder for vector database sync logic
    pass

def run_summary():
    logging.info("Running summary script.")
    subprocess.run(["python", summary_script])

def parse_chat_content(raw_text):
    """
    Parse raw text to remove irrelevant metadata and label speakers.

    Args:
        raw_text (str): Raw text extracted from OCR.

    Returns:
        str: Parsed and labeled text.
    """
    cleaned = re.sub(r"^→ .+$", "", raw_text, flags=re.MULTILINE)
    cleaned = re.sub(r"^CommandCore-Hub_v\d{4}\.\d{2}\.\d{2}.*$", "", cleaned, flags=re.MULTILINE)

    # Remove lines that are all uppercase or just symbols
    cleaned = "\n".join(
        line for line in cleaned.splitlines()
        if not re.fullmatch(r"[A-Z\s]+", line.strip()) and not re.fullmatch(r"[-=~*#]+", line.strip())
    )

    # Normalize space, strip leading clutter
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = re.sub(r"\bGPT-\d+\b", "", cleaned)
    cleaned = re.sub(r"^\s*GitHub Copilot\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*✓ Read .+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*Add Context.+", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^\s*4 files changed.+", "", cleaned, flags=re.MULTILINE)

    # Remove Copilot-specific phrases
    cleaned = re.sub(r"\b(Copilot|GPT|Command Palette|Ctrl\+Shift\+P|Alt\+Tab|file tree|sidebar)\b.*", "", cleaned, flags=re.IGNORECASE)

    # Label speakers
    labeled_blocks = []
    for block in cleaned.split("\n\n"):
        if "GitHub Copilot" in block or "Copilot" in block:
            labeled_blocks.append(f"**Copilot said:**\n{block.strip()}")
        elif any(keyword in block for keyword in ["CommandCore", "copilot_chat_capture.py"]):
            labeled_blocks.append(f"**Integrity Land Development said:**\n{block.strip()}")
        else:
            labeled_blocks.append(block.strip())

    return "\n\n".join(labeled_blocks).strip()

def detect_scroll_end():
    """
    Detect if scrolling has reached the top by checking if the captured content remains unchanged.

    Returns:
        bool: True if scrolling has reached the top, False otherwise.
    """
    global previous_text
    unchanged_count = 0
    max_unchanged_threshold = 2  # Stop scrolling after detecting unchanged content twice

    try:
        while True:
            logging.info("Capturing region for scroll end detection...")
            current_frame = capture_region()

            # Debugging: Save current frame for scroll end detection
            debug_scroll_end_path = os.path.join(output_dir, "debug_scroll_end_capture.png")
            current_frame.save(debug_scroll_end_path)
            logging.info(f"Saved scroll end detection region to: {debug_scroll_end_path}")

            current_text = pytesseract.image_to_string(current_frame).strip()
            logging.info(f"Captured text for scroll end detection: {current_text}")

            if current_text == previous_text:
                unchanged_count += 1
                logging.info(f"Unchanged content detected ({unchanged_count}/{max_unchanged_threshold}).")
                if unchanged_count >= max_unchanged_threshold:
                    logging.info("Scrolling has reached the top. Stopping scroll.")
                    return True
            else:
                unchanged_count = 0
                previous_text = current_text

            scroll_up()
    except Exception as e:
        logging.error(f"Error during scroll end detection: {e}")
        return False

def main():
    try:
        # Initialize bounding box
        print("Initializing bounding box...")
        wait_for_bounding_box()

        # Debug log for region_box
        logging.info(f"Region box defined: {region_box}")

        # Test scrolling
        logging.info("Testing scrolling...")
        scroll_up()
        logging.info("Scrolling test completed.")

        # Test OCR capture
        logging.info("Testing OCR capture...")
        captured_text = extract_chat_ocr()
        logging.info(f"Captured text: {captured_text}")

        # Save captured text to markdown
        markdown_path = save_markdown(captured_text)
        logging.info(f"Markdown saved at: {markdown_path}")

        # Trigger the summary script
        print("✅ Chat logging completed. Triggering summary script...")
        run_summary()

    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
