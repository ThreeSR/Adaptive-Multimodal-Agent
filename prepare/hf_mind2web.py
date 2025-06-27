from PIL import Image, ImageDraw
import json
import os
import re
import pdb
from tqdm import tqdm
import random
import argparse

# imgs_dir =  "./datasets/GUI_database/Mind2Web/images"
# anno_dir = "./datasets/GUI_database/Mind2Web/metadata"

parent_dir = "/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets"
imgs_dir =  "/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets/Mind2Web/images"
anno_dir = "/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets/Mind2Web/metadata"
thought_dir = f"{parent_dir}/Mind2Web/metadata"

def data_transform(version='train', mini=False):
    mind2web_train = json.load(open(f"{anno_dir}/mind2web_data_{version}.json", 'r')) # original mind2web data

    total_step = []
    step_i = 0

    for episode in tqdm(mind2web_train):
        annot_id = episode["annotation_id"] # 8f6261cf-d665-4e61-93af-f50f0d366245
        confirmed_task = episode["confirmed_task"] # Find all events taking place in New York City during the month of September.

        step_history = []
        repr_history = []
        for i, (step, step_repr) in enumerate(zip(episode["actions"], episode["action_reprs"])):
            # actions see below
            # action_reprs ["[button]  Change Location -> CLICK", "[searchbox]  Search by city... -> TYPE: New York",.. ]
            filename = annot_id + '-' + step["action_uid"] + '.jpg'
            img_path = os.path.join(imgs_dir, filename)

            step.update({"img_url": filename})  # ! add img_url to step
            
            if not os.path.exists(img_path):
                continue
            image = Image.open(img_path)
            step.update({"img_size": image.size})

            total_step.append({
                            "split": version,
                            "id": "mind2web_{}".format(step_i), 
                            "annot_id": annot_id,
                            "action_uid": step["action_uid"], # "action_uid": "f3ae6144-2f6c-407a-b5c2-bcb9d069ad84"
                            
                            "website": episode["website"],
                            "domain": episode["domain"],
                            "subdomain": episode["subdomain"],

                            "task": confirmed_task,  # task intent
                            "img_url": filename,
                            "img_size": image.size,

                            "step_id": i,
                            "step": step,
                            "step_repr": step_repr,
                            "step_history": step_history.copy(), # copy, then will be updtated
                            "repr_history": repr_history.copy()
                            })

            step_history.append(step)
            repr_history.append(step_repr)

            step_i += 1
            
        if mini and step_i > 1:
            break

    if mini:
        return total_step

    save_url = f"{anno_dir}/hf_{version}.json"
    with open(save_url, "w") as file:
        json.dump(total_step, file, indent=4)
    return total_step

if __name__ == "__main__":
    for version in ['train']:
        data_transform(version=version)

    test_full = []
    for version in ['test_task', 'test_domain', 'test_website']:
        test_full.extend(data_transform(version=version))
    save_url = f"{anno_dir}/hf_test_full.json"
    with open(save_url, "w") as file:
        json.dump(test_full, file, indent=4)

    # miniset
    # test_full = []
    # for version in ['test_task', 'test_domain', 'test_website']:
    #     test_full.extend(data_transform(version=version, mini=True))
    
    # save_url = f"{anno_dir}/hf_test_mini.json"
    # with open(save_url, "w") as file:
    #     json.dump(test_full, file, indent=4)

# {"action_uid": "f3ae6144-2f6c-407a-b5c2-bcb9d069ad84", 
# "operation": {"original_op": "CLICK", "value": "", "op": "CLICK"}, 
# "pos_candidates": [{"tag": "button", "attributes": "{\"backend_node_id\": \"2058\", \"bounding_box_rect\": \"60,1701,146.203125,34\", \"class\": \"Pills__PillContainer-sc-b74366a9-31 kSozeC\", \"data_pw_testid_buckeye_candidate\": \"1\"}", "is_original_target": false, "is_top_level_target": true, "backend_node_id": "2058", "score": 0.9039427042007446, "rank": 1, "choice": "(button id=34 (span Change Location ) )"}], 
# "bbox": {"x": 60.0, "y": 163.0, "width": 146.203125, "height": 34.0}}