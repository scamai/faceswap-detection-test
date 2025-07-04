# FaceSwap Detection Test

> **NOTE:** For the API_URL, please contact our team to obtain the correct server address. Do not expose your server address in public repositories or shared code.

This project tests a deployed deepfake (faceswap) detection API using a dataset of images. It sends each image (except those in the `Real` folder) to the API, records the detection results, and outputs a CSV file with per-image and per-source accuracy statistics.

## Project Structure

- `dataset/` — Place your images here, organized into subfolders by source:
  - Each subfolder (e.g., `DeepLiveCam/`, `FaceFusion/`, `NeoRefacer/`, `ReSwapper/`, `Roop/`, `Real/`) should contain images from that source.
  - The name of the subfolder is used to indicate the source of the images.
- `test_faceswap_detection.py` — Python script to run the tests
- `faceswap_detection_results.csv` — Output CSV with results (generated after running the script)

## Requirements
- Python 3.7+
- [requests](https://pypi.org/project/requests/)
- [tqdm](https://pypi.org/project/tqdm/)

## Setup

1. **Clone or download this repository.**
2. **Navigate to the project directory:**
   ```bash
   cd /Users/jasperhu/Desktop/ScamAI/faceswap-detection-test
   ```
3. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies:**
   ```bash
   pip install requests tqdm
   ```
5. **Prepare your dataset:**
   - Place your images in the `dataset/` folder.
   - Organize images into subfolders by source. For example:
     - `dataset/DeepLiveCam/`
     - `dataset/FaceFusion/`
     - `dataset/NeoRefacer/`
     - `dataset/ReSwapper/`
     - `dataset/Roop/`
     - `dataset/Real/`
   - The script will use the subfolder name as the source label for each image.
6. **Configure API access:**
   - Edit the `config.py` file to set your API key and dataset directory as needed.
   - **Important:** For the `API_URL`, please contact our team to obtain the correct server address. Do not expose your server address in public repositories or shared code.

## Usage

Run the test script:

```bash
python test_faceswap_detection.py
```

- The script will process all images in each subfolder of `dataset` except `Real`.
- For each image, it sends a POST request to the deployed API with the image as form-data (`file`) and the required API key.
- A progress bar will show the status for each folder.
- Results are saved to `faceswap_detection_results.csv`.
- At the end, per-source and total accuracy are printed to the console.

## Output

- **CSV file:** `faceswap_detection_results.csv` with columns:
  - `filename`: Image filename
  - `source`: Subfolder/source of the image
  - `fakeness_score`: The API's blended fakeness score
  - `correctness`: `correct` if detected as fake (score > 0.5), otherwise `wrong`
- **Console output:**
  - Accuracy for each source (subfolder)
  - Total accuracy

## Customization
- To include the `Real` folder or change the detection logic, modify `test_faceswap_detection.py` as needed.
- To add more dependencies, use `pip install <package>` and update `requirements.txt` with `pip freeze > requirements.txt`.

## License

This project is for research and testing purposes only. 