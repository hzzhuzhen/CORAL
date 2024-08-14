package com.freeal.pojo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Epoch {
    private Long taskId;
    private Integer epoch;
    private Integer currentEpoch;
}
