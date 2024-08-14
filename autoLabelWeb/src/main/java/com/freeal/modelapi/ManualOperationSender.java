package com.freeal.modelapi;

import com.freeal.configs.LanguageModelConfig;
import com.freeal.entity.HttpResponseEntity;
import com.freeal.commons.utils.RequestUtil;
import com.freeal.pojo.ManualLabel;

// 人工操作请求发送到模型端
public class ManualOperationSender {
    /**
     * 将接收到的人工标注发送到模型端
     * @param manualLabel 人工标注封装类
     * @return 请求的结果
     */
    public static HttpResponseEntity sendManualCorrectingLabel(ManualLabel manualLabel) {
        return RequestUtil.postRequest(LanguageModelConfig.MANUAL_LABEL_SAVE_DEMO_URI,
                manualLabel);
    }

    // 发送请求更新人工标注数据
    public static HttpResponseEntity updateManualCorrectingLabel() throws Exception {
        return RequestUtil.getRequest(LanguageModelConfig.MANUAL_LABEL_UPDATE_DEMO_URI);
    }

    public static void main(String[] args) throws Exception {
        //ManualLabel manualLabel = new ManualLabel(12L, 0);
        //System.out.println(updateManualCorrectingLabel());
    }
}
