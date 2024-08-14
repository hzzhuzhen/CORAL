package com.freeal.commons.utils;

import com.freeal.enums.PromptTypeEnum;
import com.freeal.enums.TaskTypeEnum;
import com.freeal.pojo.Prompt;
import com.freeal.pojo.Task;
import org.apache.commons.collections4.CollectionUtils;

import java.util.List;

public class MockDataOpt {
    public static Task mockTaskConfigurationData(Task task) {

        //todo 测试代码
//        task.setName("测试任务");
//        long now = System.currentTimeMillis();
//        task.setTaskType(TaskTypeEnum.SENTIMENT_ANALYSIS.getType());
//        task.setOwnerId(0L);
//        task.setEpoch(2);
//        task.setInputDataUrl("./data/test/"+"inputData_"+now);
//        task.setOutputDataUrl("./data/test/"+"outputData_"+now);
//        task.setThreshold(70L);
//        task.setLlmId(0L);
//        task.setSlmId(0L);
//        task.setRemark("测试数据");

        Task task1 = new Task();
        task1.setId(task.getId());
        task1.setName(task.getName());
        long now = System.currentTimeMillis();
        task1.setTaskType(task.getTaskType());
        task1.setOwnerId(1L);
        // task1.setOwnerId(task.getOwnerId());
        task1.setEpoch(task.getEpoch());
        task1.setInputDataUrl(task.getInputDataUrl() + "inputData_" + now);
        task1.setOutputDataUrl(task.getOutputDataUrl() + "outputData_" + now);
        task1.setThreshold(task.getThreshold());
        task1.setLlmId(task.getLlmId());
        task1.setSlmId(task.getSlmId());
        task1.setRemark(task.getRemark());

        return task1;
    }

    public static List<Prompt> createPrompt(List<Prompt> promptList) {
        if (CollectionUtils.isEmpty(promptList)) {
            return promptList;
        }
        for (Prompt prompt : promptList) {
            prompt.setPromptType(PromptTypeEnum.LABELING_PROMPT.getType());
            prompt.setTaskType(TaskTypeEnum.SENTIMENT_ANALYSIS.getType());
            prompt.setName("测试标注模版");
            prompt.setContent("[Task Description] You are a helpful assistant for the task of sentiment analysis. You reply with brief, to-the-point answers with no elaboration as truthfully as possible. Your task is to a binary classification to classify content as positive or negative according to their overall sentiment polarity. The category is divided into two types: ’positive’ and ’negative’.\n" +
                    "[In-Context Demonstration] You can refer to the following labeled samples for prediction: [\"content\": \"enigma is well-made, but it’s just too dry and too placid.\", \"label\": \"negative\"]... [Output Control] Given a content: <QUERY>. How do you feel about the sentiment polarity of the given content? Is this positive or negative? please answer in a single line with ’posi- tive’ or ’negative’.");
        }
        return promptList;
    }
}
