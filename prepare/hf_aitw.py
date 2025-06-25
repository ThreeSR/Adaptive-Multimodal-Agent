import os
import cv2
import re
import pdb
import json
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from IPython.display import display
from PIL import Image, ImageDraw
from data_utils import is_english_simple, bbox_2_point
from tqdm import tqdm

parent_dir = "/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets"
imgs_dir =  f"{parent_dir}/AITW/images"
anno_dir = f"{parent_dir}/AITW/metadata"
thought_dir = f"{parent_dir}/AITW/metadata"

def draw_point_bbox(image_path, point=None, bbox=None, radius=5, line=3):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    if point is not None:
        x, y = point[0] * width, point[1] * height
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill='blue', outline='blue')
    if bbox is not None:
        x1, y1, x2, y2 = bbox[0] * width, bbox[1] * height, bbox[2] * width, bbox[3] * height
        draw.rectangle([x1, y1, x2, y2], outline='red', width=line)

    image_draw = np.array(image)
    return image_draw

def get_thought_anno(thought_data):
    """
    Build a dict mapping each ep_id to the list of assistant 'Thought:' strings
    in the order they appear in the data.
    
    Args:
        thought_data (list): list of entries, each having an 'images' list
                             and a 'messages' list with assistant content.
    Returns:
        dict: { ep_id (str) : [thought1, thought2, ...], ... }
    """
    ep_thoughts = {}
    
    for entry in thought_data:
        # 1) extract ep_id from the first image path:
        #    e.g. "…/general/14492098987308163042_0.png"
        images = entry.get("images", [])
        if not images:
            continue
        first_img = images[0]
        # filename is after the last '/', then split on '_' to isolate ep_id
        filename = first_img.split("/")[-1]           # "14492098987308163042_0.png"
        ep_id = filename.split("_")[0]                # "14492098987308163042"
        
        # 2) extract assistant message content
        assistant_message = next(
            (m["content"] for m in entry.get("messages", []) if m["role"] == "assistant"),
            ""
        )
        
        # 3) parse out the Thought portion
        thought = None
        if "Thought:" in assistant_message and "Action:" in assistant_message:
            thought = (
                assistant_message
                .split("Thought:")[1]
                .split("Action:")[0]
                .strip()
            )
        
        # 4) accumulate into dictionary
        ep_thoughts.setdefault(ep_id, []).append(thought)
    
    return ep_thoughts

def data_transform(version='train', mini=False):
    aitw_data = json.load(open(f"{anno_dir}/aitw_data_{version}.json", 'r'))
    thought_data = None
    # if version == 'train':
    #     thought_data = json.load(open(f"{thought_dir}/aitw-hf_train_v2.json", 'r'))
    #     ep_thoughts = get_thought_anno(thought_data) # dict, key is ep_id, value is the list of thoughts by order

    total_step = []
    step_i = 0
    for scenario in aitw_data:
        aitw_subset = aitw_data[scenario] # 'general'
        for sample in aitw_subset: # list, per sample
            # print(sample)
            confirmed_task = sample[0]['goal']
            ep_id = sample[0]['ep_id'] # ep_id is str itself
            # thoughts = ep_thoughts[ep_id]
    
            step_history = []
            for i, step in enumerate(sample):

                # thought = thoughts[i] # thought per step

                filename = step['img_filename'] # general/14492098987308163042_1
                img_url = os.path.join(imgs_dir, filename) + '.png'
                if not os.path.exists(img_url):
                    print(img_url)
                    continue
                image = Image.open(img_url)
                action_id = step["action_type_id"]
                action_type = step["action_type_text"]
                # if action_id == 4:
                #     if action_type == "click":
                #         touch_point = step['touch']
                #         step_point = step['lift']
                #         click_point = [(touch_point[0] + lift_point[0]) / 2, (touch_point[1] + lift_point[1]) / 2]
                # elif action_type == 3:
                #     typed_text = step["type_text"]
                # print(step)
                total_step.append({
                                "split": version,
                                "id": "aitw_{}".format(step_i), 
                                # "annot_id": annot_id,
                                # "action_uid": step["action_uid"],
                                "domain": scenario,
                                "ep_id": step['ep_id'],
                                "step_id": i,
    
                                "task": confirmed_task,
                                "img_url": filename,
                                "img_size": image.size,
    
                                "action_type_id": action_id,
                                "action_type_text": action_type,
                                "annot_position": step['annot_position'],
                                "touch": step['touch'],
                                "lift": step['lift'],
                                "type_text": step['type_text'],
                                
                                # 'thought': thought,
                                
                                "step": step,
                                # "step_repr": step_repr,
                                "step_history": step_history.copy(),
                                # "repr_history": repr_history.copy()
                                })
                # print(action_type)
                step_history.append(step)
                step_i += 1

                if mini and step_i > 50:
                    break
            if mini and step_i > 50:
                break

    return total_step

if __name__ == "__main__":
    for version in ['train', 'test', 'val']:
    # for version in ['train']:
        data = data_transform(version=version)
        save_url = f"{anno_dir}/hf_{version}.json"
        # save_url = f"{anno_dir}/hf_{version}_thought.json"
        with open(save_url, "w") as file:
            json.dump(data, file, indent=4)