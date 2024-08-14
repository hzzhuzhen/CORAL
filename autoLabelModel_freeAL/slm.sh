cd /home/zjusst/ll/autoLabelModel_freeAL/self_training_slm
# CUDA_VISIBLE_DEVICES=5 sh run_roberta_mr.sh
CUDA_VISIBLE_DEVICES=5 nohup sh run_roberta_mr.sh > slm.log 2>&1 &