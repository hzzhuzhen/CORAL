package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ManualEntity {
    private long taskId;
    private long currentEpoch;
    private int id;
    private String inputDataUrl;
    private String outputDataUrl;
    private int seq;
    private String data;
    private String llmLabel;
    private String slmLabel;
    private String manualLabel;
    private float loss;
    private float representation;
    private float confidence;
    private int status;
}
