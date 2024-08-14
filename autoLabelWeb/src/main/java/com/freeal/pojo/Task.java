package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Timestamp;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Task {
    private Long id;
    private int taskType;
    private Long ownerId;
    private String name;
    private int epoch;
    private String inputDataUrl;
    private String outputDataUrl;
    private Long llmId;
    private Long slmId;
    private String remark;
    private Long threshold;
    private int status;
    private Timestamp createTime;
    private Timestamp updateTime;
}
