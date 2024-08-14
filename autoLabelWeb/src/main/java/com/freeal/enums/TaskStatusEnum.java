package com.freeal.enums;

import lombok.Getter;

public enum TaskStatusEnum {
    NOT_START(0, "未开始"),
    IN_PROCESSING(1, "进行中"),
    WAITING(2, "执行中止等待操作"),
    FINISH(3, "结束"),
    PAUSE(-1, "暂停"),
    EXCEPTION_OCCUR(-2, "异常终止");

    TaskStatusEnum(Integer type, String desc) {
        this.type = type;
        this.desc = desc;
    }

    @Getter
    private final Integer type;

    @Getter
    private final String desc;
}
