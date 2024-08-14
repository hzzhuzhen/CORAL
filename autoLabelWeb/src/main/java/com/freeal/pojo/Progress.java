package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.sql.Timestamp;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Progress {
    private  Long id;
    private  Integer currentEpoch = 0;
    private  Integer currentModel = 0;
    private  Integer process = 0;
    private  Integer isCorrecting = 0;
    private  Integer stepOver = 0;
    private  Float loss = 1.0F;
    private  Float labelMatch = 1F;
    private Timestamp startTime;
    private  Timestamp endTime;
    private  Timestamp createTime;
    private  Timestamp updateTime;
}
