package com.freeal.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Prompt {
    private Long id;
    private String name;
    private Long taskId;
    private Integer taskType;
    private Integer promptType;
    private String content;
    private Long createTime;
    private Long updateTime;
}
