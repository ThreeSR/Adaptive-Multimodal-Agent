deepspeed --num_gpus 1 \
    --module deepspeed.convert_zero_checkpoint \
    --input_dir /mnt/data1/t-rsun/results/mind2web/Long_Context_AMD/Qwen2.5-VL-3B-Instruct-TTTT-2-SFT-AMD/2025-07-07_16-56-01/ckpt_model/global_step8685 \
    --output_file merged-qwen2p5vl-3b-tttt-2-sft-amd.bin
