import os
import logging
from utils.utils import prediction

logger = logging.getLogger(__name__)

# 执行器，控制流程
class Runner:
    # 初始化：放入model模式类别、训练器trainer、分词器、训练参数、测试数据集、验证数据集
    def __init__(self, model_name, trainer, tokenizer, training_args, test=None, eval=None):
        self.model_name = model_name
        self.trainer = trainer  # 重构的mytrainer
        self.tokenizer = tokenizer
        self.training_args = training_args
        self.test = test
        self.dev = eval
    # 调用执行
    def __call__(self):
        if self.training_args.do_train:
            self.train(self.model_name)  # 执行训练

        if self.training_args.do_eval and self.dev is not None:
            self.eval(self.dev)  # 执行dev上的验证

        if self.training_args.do_predict and self.test is not None:
            self.predict(self.test)  # 执行test集的预测

    # 执行训练
    def train(self, model_name):
        # 执行训练
        self.trainer.train(model_path=model_name if os.path.isdir(model_name) else None)
        # 保存模型
        self.trainer.save_model()
        if self.trainer.is_world_process_zero():
            self.tokenizer.save_pretrained(self.training_args.output_dir)

    # 执行验证
    def eval(self,eval):
        logger.info("*** Evaluate ***")
        result = self.trainer.evaluate(eval_dataset=eval)
        output_eval_file = os.path.join(self.training_args.output_dir, "eval_results.txt")
        if self.trainer.is_world_process_zero():
            with open(output_eval_file, "w") as writer:
                logger.info("***** Eval results *****")
                for key, value in result.items():
                    logger.info("%s = %s", key, value)
                    writer.write("%s = %s\n" % (key, value))

        logger.info("Validation set result : {}".format(result))

    #  测试集上做预测
    def predict(self, test):
        logger.info("*** Test ***")
        predictions = self.trainer.predict(test_dataset=test)
        output_test_file = os.path.join(self.training_args.output_dir, "test_results.txt")
        if self.trainer.is_world_process_zero():
            with open(output_test_file, "w") as writer:
                logger.info("***** Test results *****")
                logger.info("{}".format(predictions))
                writer.write("prediction : \n{}\n\n".format(prediction(predictions.predictions).tolist()))
                if predictions.label_ids is not None:
                    writer.write("ground truth : \n{}\n\n".format(predictions.label_ids.tolist()))
                    writer.write("metrics : \n{}\n\n".format(predictions.metrics))
