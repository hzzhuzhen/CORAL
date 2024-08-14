package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class LanguageModelFetchForm {
    private Long id;
    private String content;
    private String llmLabel;
    private String slmLabel;
    private Long ranking;
    private Float confidence;
}
