WANDB_KEY="75804c2ef8d16e3c694a4849f75596349142b31c"
_DATA_DIR="/home/ruis/code/Adaptive-Agent/data/datasets"
# _SAVE_DIR="/home/ruis/code/Adaptive-Multimodal-Agent/results/aitw/ShowUI_2B_ZS" # if zero-shot
# _SAVE_DIR="/home/ruis/code/Adaptive-Multimodal-Agent/results/aitw/ShowUI_2B_SFT" # if fine-tuning
_SAVE_DIR="/local3/ruis/Adaptive-Multimodal-Agent/results/aitw/ShowUI_2B_SFT" # if fine-tuning, nlp-14

# Fine-tune ShowUI, some parameters are based on the paper appendix
# deepspeed --include localhost:1,2,3,4,5,6,7 --master_port 1224 train.py \
#   --wandb_key=$WANDB_KEY \
#   --model_id='showlab/ShowUI-2B' \
#   --version='showlab/ShowUI-2B' \
#   --dataset_dir=$_DATA_DIR \
#   --log_base_dir=$_SAVE_DIR \
#   --epochs=50 \
#   --steps_per_epoch=100 \
#   --batch_size=1 \
#   --grad_accumulation_steps=2 \
#   --model_max_length=8192 \
#   --exp_id="debug" \
#   --train_ratio="1"  \
#   --train_dataset="aitw"  \
#   --train_json="hf_train"   \
#   --val_dataset="aitw"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=0 \
#   --lora_r=64 \
#   --lora_alpha=128  \
#   --min_visual_tokens=256  \
#   --max_visual_tokens=1280  \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --random_sample \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing  \
#   --lm_skip_ratio=0.5   \
#   --lm_skip_layer='[1,28,0]' \
#   --interleaved_history="tttt" \
#   --val_json="hf_test" \
#   --num_history=2 \
# last rows are added by rui

# CoT Tuning ShowUI
deepspeed --include localhost:1,2,3,4,5,6,7 --master_port 1224 train.py \
  --wandb_key=$WANDB_KEY \
  --model_id='showlab/ShowUI-2B' \
  --version='showlab/ShowUI-2B' \
  --dataset_dir=$_DATA_DIR \
  --log_base_dir=$_SAVE_DIR \
  --epochs=50 \
  --steps_per_epoch=100 \
  --batch_size=1 \
  --grad_accumulation_steps=2 \
  --model_max_length=8192 \
  --exp_id="debug" \
  --train_ratio="1"  \
  --train_dataset="aitw"  \
  --train_json="hf_train"   \
  --val_dataset="aitw"  \
  --precision="bf16" \
  --attn_imple="sdpa" \
  --workers=0 \
  --lora_r=64 \
  --lora_alpha=128  \
  --min_visual_tokens=256  \
  --max_visual_tokens=1280  \
  --num_turn=100 \
  --crop_min=0.5 \
  --crop_max=1.5 \
  --random_sample \
  --record_sample \
  --lr=0.0001 \
  --uniform_prompt  \
  --ds_zero="zero2" \
  --gradient_checkpointing  \
  --lm_skip_ratio=0.5   \
  --lm_skip_layer='[1,28,0]' \
  --interleaved_history="tttt" \
  --val_json="hf_test" \
  --num_history=2 \

# Fine-tune Qwen2VL, Qwen2.5VL
# deepspeed --include localhost:1 --master_port 5678 train.py \
#   --wandb_key=$WANDB_KEY \
#   --model_id="Qwen/Qwen2.5-VL-3B-Instruct" \
#   --version="Qwen/Qwen2.5-VL-3B-Instruct" \
#   --dataset_dir=$_DATA_DIR \
#   --log_base_dir=$_SAVE_DIR \
#   --epochs=50 \
#   --steps_per_epoch=100 \
#   --batch_size=1 \
#   --grad_accumulation_steps=2 \
#   --model_max_length=8192 \
#   --exp_id="debug" \
#   --train_ratio="1"  \
#   --train_dataset="showui"  \
#   --train_json="hf_train"   \
#   --val_dataset="screenspot"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=4 \
#   --lora_r=32 \
#   --lora_alpha=64  \
#   --min_visual_tokens=256  \
#   --max_visual_tokens=1344  \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --random_sample \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing


# Zero-shot inference Qwen2.5VL
# deepspeed --include localhost:1 --master_port 5678 train.py \
#   --wandb_key=$WANDB_KEY \
#   --model_id="Qwen/Qwen2.5-VL-3B-Instruct" \
#   --version='Qwen/Qwen2.5-VL-3B-Instruct' \
#   --dataset_dir=$_DATA_DIR \
#   --log_base_dir=$_SAVE_DIR \
#   --epochs=50 \
#   --steps_per_epoch=100 \
#   --batch_size=1 \
#   --grad_accumulation_steps=2 \
#   --model_max_length=8192 \
#   --exp_id="Qwen/Qwen2.5-VL-3B-Instruct" \
#   --train_ratio="1" \
#   --train_dataset="showui"  \
#   --train_json="hf_train"   \
#   --val_dataset="screenspot"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=4 \
#   --lora_r=32 \
#   --lora_alpha=64  \
#   --min_visual_tokens=256  \
#   --max_visual_tokens=1344 \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --random_sample \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing \
#   --eval_only

# originally, the num_hostory is 4, and min_visual_tokens is 256, max_visual_tokens=1344

# Zero-shot inference ShowUI-2B
# deepspeed --include localhost:4 --master_port 5678 train.py \
#   --wandb_key=$WANDB_KEY \
#   --model_id="showlab/ShowUI-2B" \
#   --version='showlab/ShowUI-2B' \
#   --dataset_dir=$_DATA_DIR \
#   --log_base_dir=$_SAVE_DIR \
#   --epochs=50 \
#   --steps_per_epoch=100 \
#   --batch_size=1 \
#   --grad_accumulation_steps=2 \
#   --model_max_length=8192 \
#   --exp_id="showlab/ShowUI-2B" \
#   --train_ratio="1" \
#   --train_dataset="showui"  \
#   --train_json="hf_train"   \
#   --val_dataset="aitw"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=4 \
#   --lora_r=0 \
#   --lora_alpha=64  \
#   --min_visual_tokens=1024 \
#   --max_visual_tokens=1344 \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing \
#   --eval_only \
#   --val_json="hf_test" \
#   --num_history=4 \
  # --data_debug

  # --random_sample \