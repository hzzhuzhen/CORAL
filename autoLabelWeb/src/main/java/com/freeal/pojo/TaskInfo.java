package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class TaskInfo {
    private long taskId;
    private String name;
    private int epoch;
    private String inputDataUrl;
    private long llmId;
    private long slmId;
    private int threshold;
    private String remark;
    private int status;
}
