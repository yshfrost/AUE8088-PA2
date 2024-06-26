import json
import os

# val.txt 파일 경로
val_file = 'val.txt'

# 라벨 파일이 저장된 디렉토리 경로
labels_dir = 'datasets/kaist-rgbt/train/labels'

# JSON 파일로 저장할 경로
output_json_file = 'KAIST_annotation.json'

# JSON 구조 초기화
results = {
    "info": {
        "dataset": "KAIST Multispectral Pedestrian Benchmark",
        "url": "https://soonminhwang.github.io/rgbt-ped-detection/",
        "related_project_url": "http://multispectral.kaist.ac.kr",
        "publish": "CVPR 2015"
    },
    "info_improved": {
        "sanitized_annotation": {
            "publish": "BMVC 2018",
            "url": "https://li-chengyang.github.io/home/MSDS-RCNN/",
            "target": "files in train-all-02.txt (set00-set05)"
        },
        "improved_annotation": {
            "url": "https://github.com/denny1108/multispectral-pedestrian-py-faster-rcnn",
            "publish": "BMVC 2016",
            "target": "files in test-all-20.txt (set06-set11)"
        }
    },
    "images": [],
    "annotations": [],
    "categories": [
        {"id": 0, "name": "person"},
        {"id": 1, "name": "cyclist"},
        {"id": 2, "name": "people"},
        {"id": 3, "name": "person?"}
    ]
}

# val.txt 파일 읽기
with open(val_file, 'r') as f:
    lines = f.readlines()

# 이미지 ID와 어노테이션 ID 초기화
image_id = 0
annotation_id = 0

# 라벨 파일 읽기 함수 정의
def read_label_file(label_file_path):
    with open(label_file_path, 'r') as f:
        return [line.strip().split() for line in f]

# val.txt 내용을 JSON 구조로 변환
for line in lines:
    parts = line.strip().split('/')
    if len(parts) < 2:
        print(f"Warning: Skipping line due to insufficient data: {line.strip()}")
        continue

    image_file_name = parts[-1]  # 'set00_V001_I01491.jpg'
    label_file_name = image_file_name.replace('.jpg', '.txt')
    label_file_path = os.path.join(labels_dir, label_file_name)

    # 이미지 정보 추가
    results["images"].append({
        "id": image_id,
        "im_name": image_file_name,
        "height": 512,  # 실제 이미지 높이로 수정
        "width": 640    # 실제 이미지 너비로 수정
    })

    # 라벨 파일이 존재하는지 확인
    if os.path.exists(label_file_path):
        label_data = read_label_file(label_file_path)

        for label in label_data:
            category_id = int(label[0])
            bbox = [float(coord) for coord in label[1:5]]
            annotation_entry = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": bbox,
                "height": bbox[3],  # Assuming height is the 4th element in bbox
                "occlusion": 0,  # Placeholder, replace with actual occlusion if available
                "ignore": 0  # Placeholder, replace with actual ignore flag if available
            }
            results["annotations"].append(annotation_entry)
            annotation_id += 1
    else:
        print(f"Warning: Label file not found for image: {image_file_name}")

    image_id += 1

# JSON 파일로 저장
with open(output_json_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"결과가 {output_json_file}에 저장되었습니다.")

