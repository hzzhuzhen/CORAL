package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

// 人工标数据存储类
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ManualLabel {
    private Long index; // 数据的ID，定位第几条数据
    private Integer label; // 人工标签
}
