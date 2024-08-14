package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LanguageModelRunningStatus {
    private Integer current;
    private Integer total;
    private String status;
    private Integer exit;
}
