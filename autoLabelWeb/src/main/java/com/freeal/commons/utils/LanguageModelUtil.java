package com.freeal.commons.utils;

public class LanguageModelUtil {
    public static final String FINISH_STATUS = "finish";

    public static boolean isFinishStatus(String status) {
        return FINISH_STATUS.equals(status);
    }
}
