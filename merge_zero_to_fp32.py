# this file converts deepspeed ckpts into normal pytorch weights

from deepspeed.utils.zero_to_fp32 import load_state_dict_from_zero_checkpoint
from model.qwen2_5_vl.modeling_qwen2_5_vl import Qwen2_5_VLForConditionalGeneration
import torch, os

# 1) checkpoint 根目录（含 latest、global_step8685 等子文件夹）
CKPT_ROOT = (
    "/mnt/data1/t-rsun/results/mind2web/Long_Context_AMD/"
    "Qwen2.5-VL-3B-Instruct-TTTT-2-SFT-AMD/"
    "2025-07-07_16-56-01/ckpt_model"
)
TAG = "global_step8685"                   # 想加载的最佳权重子目录
OUTPUT_BIN = "merged-qwen2p5vl-3b-tttt-2-sft-amd.bin"

# 2) 创建空骨架模型（放 CPU）
base_id = "Qwen/Qwen2.5-VL-3B-Instruct"
model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
    base_id, device_map="cpu", torch_dtype=torch.bfloat16
)

# 3) 合并 ZeRO 分片 — 指定 root 与 tag
load_state_dict_from_zero_checkpoint(model, CKPT_ROOT, tag=TAG)

# 4) 保存为单一 bf16 权重文件
torch.save({k: v.to(torch.bfloat16) for k, v in model.state_dict().items()},
        OUTPUT_BIN)
print(f"✅  merged weight saved to {OUTPUT_BIN}")
