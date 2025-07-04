import os
import requests
import csv
from collections import defaultdict
from tqdm import tqdm
import json
from config import API_URL, API_KEY, DATASET_DIR, CSV_FILENAME

# Get all subfolders
sources = [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]

results = []
source_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
failed_tests = 0

def test_image(filepath, source):
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f, 'image/jpeg')}
        headers = {'x-api-key': API_KEY}
        try:
            response = requests.post(API_URL, files=files, headers=headers, timeout=30)
            response.raise_for_status()
            try:
                data = response.json()
            except Exception as e:
                return None, f'Could not parse JSON: {str(e)}'
            if 'faces' not in data or not data['faces']:
                return None, json.dumps(data)
            face_detail = data['faces'][0]
            if 'blended_fakeness_score' not in face_detail or face_detail['blended_fakeness_score'] is None:
                return None, json.dumps(data)
            score = face_detail['blended_fakeness_score']
            return score, None
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return None, str(e)

def main():
    global failed_tests
    for source in sources:
        folder = os.path.join(DATASET_DIR, source)
        image_files = [f for f in os.listdir(folder) if f.lower().endswith('.jpg')]
        print(f"\nProcessing folder: {source} ({len(image_files)} images)")
        for filename in tqdm(image_files, desc=f"{source}", unit="img"):
            filepath = os.path.join(folder, filename)
            score, remark = test_image(filepath, source)
            if score is None:
                results.append({
                    'filename': filename,
                    'source': source,
                    'fakeness_score': '',
                    'correctness': 'test failed',
                    'remark': remark
                })
                source_stats[source]['total'] += 1
                failed_tests += 1
                continue
            if source == 'Real':
                correct = score <= 0.5
            else:
                correct = score > 0.5
                results.append({
                'filename': filename,
                'source': source,
                'fakeness_score': score,
                'correctness': 'correct' if correct else 'wrong',
                'remark': ''
            })
            source_stats[source]['total'] += 1
            if correct:
                source_stats[source]['correct'] += 1
    # Write CSV
    with open(CSV_FILENAME, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['filename', 'source', 'fakeness_score', 'correctness', 'remark'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    # Print accuracy
    print('\nAccuracy by source:')
    total_correct = 0
    total = 0
    for source in sources:
        correct = source_stats[source]['correct']
        total_src = source_stats[source]['total']
        acc = (correct / total_src * 100) if total_src else 0
        print(f"{source}: {acc:.2f}% ({correct}/{total_src})")
        total_correct += correct
        total += total_src
    total_acc = (total_correct / total * 100) if total else 0
    print(f"\nTotal accuracy: {total_acc:.2f}% ({total_correct}/{total})")
    print(f"\nNumber of tests with blended fakeness score being None (test failed): {failed_tests}")

if __name__ == '__main__':
    main() 