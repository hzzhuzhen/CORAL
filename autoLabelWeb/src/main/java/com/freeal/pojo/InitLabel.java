package com.freeal.pojo;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class InitLabel {
    private Long id;
    private Long taskId;
    private String inputDataUrl;
    private Long seq;
    private String data;
    private String labeling;
    private Integer status;
    private Long createTime;
    private Long updateTime;
}
