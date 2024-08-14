package com.freeal.enums;

import lombok.Getter;

@Getter
public enum LanguageModelEnum {
    LLM(1, "LLM"),
    SLM(2, "SLM");

    LanguageModelEnum(Integer type, String modelDesc) {
        this.type = type;
        this.modelDesc = modelDesc;
    }

    private final Integer type;
    private final String modelDesc;
}
