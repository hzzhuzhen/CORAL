#!/bin/bash
# 第一轮LLM
pwd
echo -e "第一轮LLM"
cd active_labeling_llm
python active_labeling_llm.py > ../output_data/mr/mr_1st_LLM_llm.log
echo -e "拷贝数据..."
cd ..
cp -rf data/mr/train_.csv output_data/mr
mv output_data/mr/train_.csv output_data/mr/mr_1st_LLM_output_train.csv

# 第二轮SLM
echo -e "第二轮SLM轮"
echo -e "准备SLM数据..."
python data_prepare.py
cd self_training_slm
sh run_roberta_mr.sh > ../output_data/mr/mr_2th_SLM_slm.log 
echo -e "拷贝数据..."
cd ..
cp -rf data/mr/train_chat_bt.csv output_data/mr
mv output_data/mr/train_chat_bt.csv output_data/mr/mr_2th_LLM_output_train_chat_bt.csv
cp -rf self_training_slm/data_out/eval_results.txt output_data/mr
mv output_data/mr/eval_results.txt output_data/mr/mr_2th_SLM_eval_results.txt
cp -rf self_training_slm/data_out/test_results.txt output_data/mr
mv output_data/mr/test_results.txt output_data/mr/mr_2th_SLM_test_results.txt
cp -rf self_training_slm/data_out/logging.log output_data/mr
mv output_data/mr/logging.log output_data/mr/mr_2th_SLM_logging.log
cp -rf data/labels_slm.csv output_data/mr
mv output_data/mr/labels_slm.csv output_data/mr/mr_2th_SLM_labels_slm.csv
cp -rf data/confidence_list.csv output_data/mr
mv output_data/mr/confidence_list.csv output_data/mr/mr_2th_SLM_confidence_list.csv

# 手工更正5%的数据
echo -e "自动标注数据..."
python manual_auto_update_by_train_data.py > output_data/mr/mr_2_5th_auto_update_manual_correction_1.log
cp -rf data/manual_label.csv output_data/mr
mv output_data/mr/manual_label.csv output_data/mr/mr_2_5th_manual_label.csv


# 第三轮LLM
echo -e "第三轮LLM"
cd active_labeling_llm
python active_labeling_llm.py --refinery  > ../output_data/mr/mr_3th_llm_refinery.log
echo -e "拷贝数据..."
cd ..
cp -rf data/mr/train_.csv output_data/mr
mv output_data/mr/train_.csv output_data/mr/mr_3th_LLM_output_train.csv

# 第四轮SLM
echo -e "第四轮SLM轮"
echo -e "准备SLM数据..."
python data_prepare.py
cd self_training_slm
sh run_roberta_mr_refinery.sh > ../output_data/mr/mr_4th_SLM_slm_refinery.log
echo -e "拷贝数据..."
cd ..
cp -rf data/mr/train_chat_bt.csv output_data/mr
mv output_data/mr/train_chat_bt.csv output_data/mr/mr_4th_LLM_output_train_chat_bt.csv
cp -rf self_training_slm/data_out/eval_results.txt output_data/mr
mv output_data/mr/eval_results.txt output_data/mr/mr_4th_SLM_eval_results.txt
cp -rf self_training_slm/data_out/test_results.txt output_data/mr
mv output_data/mr/test_results.txt output_data/mr/mr_4th_SLM_test_results.txt
cp -rf self_training_slm/data_out/logging.log output_data/mr
mv output_data/mr/logging.log output_data/mr/mr_4th_SLM_logging.log
cp -rf data/labels_slm_refinery.csv output_data/mr
mv output_data/mr/labels_slm_refinery.csv output_data/mr/mr_4th_SLM_labels_slm_refinery.csv
cp -rf data/confidence_list_refinery.csv output_data/mr
mv output_data/mr/confidence_list_refinery.csv output_data/mr/mr_4th_SLM_confidence_list_refinery.csv 


