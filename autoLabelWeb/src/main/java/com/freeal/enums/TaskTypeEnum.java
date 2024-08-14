package com.freeal.enums;

import lombok.Getter;
import org.apache.poi.ss.formula.functions.T;

public enum TaskTypeEnum {
    DEFAULT(0, "测试任务"),
    SENTIMENT_ANALYSIS(1, "情感分析"),
    SUBJECTIVITY_CLASSIFICATION(2, "观点分类"),
    TOPIC_CLASSIFICATION(3, "主题分类"),
    NAME_DENTITY_RECOGNITION(101, "命名实体识别"),
    CUSTOM_1001(1001, "自定义1001");

    TaskTypeEnum(Integer type, String desc) {
        this.type = type;
        this.desc = desc;
    }

    @Getter
    private final Integer type;

    @Getter
    private final String desc;
}
