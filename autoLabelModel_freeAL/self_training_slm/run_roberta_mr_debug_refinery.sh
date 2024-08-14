export PYTHONPATH="$PWD"
export CUDA_LAUNCH_BLOCKING=1

setting=${1:-transductive}
dataname=${2:-mr}
numlabels=${3:-2}

python -m debugpy --listen localhost:5678 --wait-for-client main.py \
        --refinery \
        --do_eval \
        --do_train \
        --do_predict \
        --output_dir data_out \
        --data_dir ../data \
        --cache_dir .cache \
        --overwrite_output_dir \
        --model roberta \
        --seed 123 \
        --save_total_limit 3 \
        --learning_rate 3e-5 \
        --weight_decay 0.01 \
        --per_device_train_batch_size 32 \
        --per_device_eval_batch_size 128 \
        --num_train_epochs 50.0 \
        --max_seq_length 128 \
        --task_name $dataname \
        --num_labels $numlabels \
        --eval_steps 10 \
        --logging_steps 10 \
        --save_steps 100 \
        --select_demo_num 10 \
        --gradient_accumulation_steps 1\
        --learning_setting $setting\
        --evaluation_strategy epoch --remove_unused_columns False --overwrite_cache --hidden_dropout_prob 0.3