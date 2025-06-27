WANDB_KEY="75804c2ef8d16e3c694a4849f75596349142b31c"
_DATA_DIR="/home/t-rsun/code/Adaptive-Multimodal-Agent/data/datasets"
# _SAVE_DIR="/home/t-rsun/code/Adaptive-Multimodal-Agent/results/mind2web/ShowUI_2B_ZS"
_SAVE_DIR="/home/t-rsun/code/Adaptive-Multimodal-Agent/results/mind2web/ShowUI_2B_SFT" # nlp-13 -> nlp-14
# _SAVE_DIR="/home/t-rsun/code/Adaptive-Multimodal-Agent/results/mind2web/QwenVL_3B_ZS"

# Fine-tune ShowUI
deepspeed --include localhost:0,1,2,3 --master_port 1224 train.py \
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
  --train_dataset="mind2web"  \
  --train_json="hf_train"   \
  --val_dataset="mind2web"  \
  --precision="bf16" \
  --attn_imple="sdpa" \
  --workers=0 \
  --lora_r=64 \
  --lora_alpha=128  \
  --min_visual_tokens=256  \
  --max_visual_tokens=1344  \
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
  --interleaved_history="vtvt" \
  --num_history=1 \
  # --auto_resume \
# last rows are added by rui

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
# deepspeed --include localhost:0 --master_port 5678 train.py \
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
#   --train_dataset="mind2web"  \
#   --train_json="hf_train"   \
#   --val_dataset="mind2web"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=4 \
#   --lora_r=0 \
#   --lora_alpha=64  \
#   --min_visual_tokens=256  \
#   --max_visual_tokens=1344 \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing \
#   --eval_only

# --random_sample \

# Zero-shot inference ShowUI-2B
# deepspeed --include localhost:0,1,2,3 --master_port 5678 train.py \
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
#   --val_dataset="mind2web"  \
#   --precision="bf16" \
#   --attn_imple="sdpa" \
#   --workers=4 \
#   --lora_r=0 \
#   --lora_alpha=64  \
#   --min_visual_tokens=256  \
#   --max_visual_tokens=1344 \
#   --num_turn=100 \
#   --crop_min=0.5 \
#   --crop_max=1.5 \
#   --record_sample \
#   --lr=0.0001 \
#   --uniform_prompt  \
#   --ds_zero="zero2" \
#   --gradient_checkpointing \
#   --eval_only

  # --random_sample \