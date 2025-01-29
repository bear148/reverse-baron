import argparse
import hashlib
import json
import numpy as np
from numba import cuda
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 1024

def is_cuda_fully_available():
    # """Check if CUDA is fully available with all required components"""
    # try:
    #     cuda.detect()
    #     # Try to create a simple test kernel to verify CUDA functionality
    #     @cuda.jit
    #     def test_kernel(x):
    #         pass
    #     test_kernel[1, 1](np.array([1]))
    #     return True
    # except Exception as e:
    #     logger.warning(f"CUDA initialization failed: {str(e)}")
    #     return False
    return False

@cuda.jit
def process_chunk_kernel(word_array, result_array):
    idx = cuda.grid(1)
    if idx < word_array.shape[0]:
        for i in range(word_array.shape[1]):
            if word_array[idx, i] > 0:
                result_array[idx, i] = word_array[idx, i]

def load_words(files):
    word_set = set()
    for file in files:
        try:
            # Try UTF-8 first
            with open(file, "r", encoding='utf-8') as f:
                if file.lower().endswith('.json'):
                    try:
                        data = json.load(f)
                        # Handle both dictionary keys and list items
                        if isinstance(data, dict):
                            words = list(data.keys())
                        elif isinstance(data, list):
                            words = data
                        else:
                            logger.warning(f"Unsupported JSON structure in {file}")
                            continue
                        for word in words:
                            if isinstance(word, str) and word.isalpha() and 3 < len(word):
                                word_set.add(word.upper())
                    except json.JSONDecodeError as e:
                        logger.error(f"Error reading JSON file {file}: {str(e)}")
                else:  # Treat as text file
                    for line in f:
                        word = line.strip()
                        if word.isalpha() and 3 < len(word):
                            word_set.add(word.upper())
        except UnicodeDecodeError:
            # Try with different encodings if UTF-8 fails
            encodings = ['latin-1', 'cp1252', 'iso-8859-1']
            success = False
            for encoding in encodings:
                try:
                    with open(file, "r", encoding=encoding) as f:
                        if file.lower().endswith('.json'):
                            try:
                                data = json.load(f)
                                if isinstance(data, dict):
                                    words = list(data.keys())
                                elif isinstance(data, list):
                                    words = data
                                else:
                                    logger.warning(f"Unsupported JSON structure in {file}")
                                    continue
                                for word in words:
                                    if isinstance(word, str) and word.isalpha() and 3 < len(word):
                                        word_set.add(word.upper())
                            except json.JSONDecodeError as e:
                                logger.error(f"Error reading JSON file {file}: {str(e)}")
                        else:
                            for line in f:
                                word = line.strip()
                                if word.isalpha() and 3 < len(word):
                                    word_set.add(word.upper())
                    success = True
                    break
                except UnicodeDecodeError:
                    continue
            if not success:
                logger.error(f"Failed to read file {file} with any supported encoding")
        except Exception as e:
            logger.error(f"Error processing file {file}: {str(e)}")
    return list(word_set)

def hash_words_cpu(words):
    logger.info("No GPU detected. Falling back to CPU...")
    return {word: hashlib.md5(word.encode()).hexdigest() for word in words}

def hash_words_gpu(words):
    logger.info("GPU detected. Using GPU for parallel processing...")


def get_files_from_path(path):
    """Recursively get all files from a path."""
    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    return files

def process_files(input_paths, output_file):
    # Collect all files from the input paths
    all_files = []
    for path in input_paths:
        all_files.extend(get_files_from_path(path))
    
    if not all_files:
        logger.error("No files found in the specified paths")
        return

    words = load_words(all_files)
    logger.info(f"Loaded {len(words)} unique words from {len(all_files)} files.")

    if is_cuda_fully_available():
        try:
            word_hashes = hash_words_gpu(words)
        except Exception as e:
            logger.error(f"GPU processing failed: {str(e)}")
            logger.info("Falling back to CPU processing...")
            word_hashes = hash_words_cpu(words)
    else:
        word_hashes = hash_words_cpu(words)

    with open(output_file, "w") as json_file:
        json.dump(word_hashes, json_file, indent=4)
    word_count = len(word_hashes)
    logger.info(f"Words and their MD5 hashes have been saved to {output_file}")
    logger.info(f"Total words processed and saved: {word_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Merge word files/folders, remove duplicates, and create MD5 hashes."
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs="+",
        required=True,
        help="Input files or folders (e.g., file1.txt folder1 file2.txt).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.json",
        help="Output file name (default: output.json).",
    )
    args = parser.parse_args()

    process_files(args.input, args.output)


if __name__ == "__main__":
    main()
