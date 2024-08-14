package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Llm {
    private int taskType;
    private Long llmId;
    private String llmName;
}
