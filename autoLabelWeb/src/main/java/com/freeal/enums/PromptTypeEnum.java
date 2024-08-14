package com.freeal.enums;

import lombok.Getter;

public enum PromptTypeEnum {
    INITAL_PROMPT(0, "初始化演示集数据生成prompt"),
    LABELING_PROMPT(1, "重标注提示模版");

    PromptTypeEnum(Integer type, String desc) {
        this.type = type;
        this.desc = desc;
    }

    @Getter
    private final Integer type;

    @Getter
    private final String desc;
}
