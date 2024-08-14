<template>
    <ContentBase>
        <div class="row justify-content-md-center whole-div">
            <div class="col-md-6 border-end position-relative">
                <div class="position-absolute top-10 start-10"><strong>任务基本信息</strong></div>
                <div style="margin-top: 2rem; display: flex; justify-content: space-between;">
                    <div style="width: 45%; text-align: left; padding-left: 30px;">
                        <p><span style="color: rgb(246,103,11);">任务ID：</span>{{ taskInfo.taskId }}</p>
                        <p><span style="color: rgb(246,103,11);">任务名称：</span>{{ taskInfo.name }}</p>
                        <p><span style="color: rgb(246,103,11);">预标注语料：</span>unlabel_ner.txt</p>
                        <p><span style="color: rgb(246,103,11);">预处理方法：</span>process_nyt_1</p>
                    </div>
                    <div style="width: 45%; text-align: left;">
                        <p><span style="color: rgb(246,103,11);">大语言模型：</span>{{ taskInfo.llmId }}</p>
                        <p><span style="color: rgb(246,103,11);">基准标注语料：</span>NYT-2003</p>
                        <p><span style="color: rgb(246,103,11);">提供工程：</span>prompt_bert_nyt_2</p>
                        <p><span style="color: rgb(246,103,11);">小语言模型：</span>{{ taskInfo.slmId }}</p>
                    </div>
                </div>
            </div>

            <div class="col-md-6 position-relative">
                <div class="position-absolute top-10 start-10"><strong>任务执行</strong></div>
                <div style="margin-top: 2rem; display: flex; justify-content: space-between;">
                    <div style="width: 40%; text-align: left; padding-left: 30px;">
                        <p><span style="color: rgb(246,103,11);">状态：</span>{{ progressInfo.isCorrecting }}</p>
                        <p><span style="color: rgb(246,103,11);">epoch：</span>{{ progressInfo.currentEpoch }}/{{
                            progressInfo.epoch
                        }}</p>
                        <p><span style="color: rgb(246,103,11);">进度：</span>{{ progressInfo.process }}%</p>
                        <p><span style="color: rgb(246,103,11);">执行环节：</span>{{ progressInfo.currentModel }}</p>
                    </div>
                    <div style="width: 60%;">
                        <!-- <img src="../../images/llm_or_slm.png" alt="no pic"> -->
                        <div ref="canvasContainer"></div>
                        <div class="button-container">
                            <button id="manual-correction" class="orange-button distance">
                                人工修正
                            </button>
                            <button class="grey-button distance">跳过</button>
                        </div>
                        <label>
                            <input type="checkbox">持续跳过
                        </label>
                    </div>
                </div>
            </div>

            <div class="col-md-12 border-top mt-3">
                <div class="position-absolute top-10 start-10"><strong>统计信息</strong></div>
                <div style="margin-top: 2rem; display: flex; justify-content: space-between;">
                    <div style="width: 25%;">
                        <p><span style="color: rgb(246,103,11);">指标1：</span>80%</p>
                        <p><span style="color: rgb(246,103,11);">指标2：</span>80%</p>
                        <p><span style="color: rgb(246,103,11);">指标3：</span>80%</p>
                    </div>
                    <div style="width: 60%;">
                        <img src="../../images/resinfo.png" alt="no pic" style="width: 500px; height: auto;">
                    </div>
                </div>
            </div>

            <div class="col-md-12 border-top mt-3">
                <div class="position-absolute top-10 start-10"><strong>标注数据检查</strong></div>
                <form @submit.prevent="submitQuery">
                    <div>
                        <button class="orange-button distance" id="csv2user"
                            style="margin-top: 25px; margin-left: 82%; width: 100px; height: 40px;">数据导出</button>
                    </div>
                    <div class="input-container">
                        <div>
                            <label for="certainSeq">数据序号</label>
                            <input v-if="certainSeq !== -1" v-model="certainSeq" type="text" id="certainSeq">
                        </div>
                        <div>
                            <label for="lSeq">开始序号</label>
                            <input v-model="lSeq" type="text" id="lSeq">
                        </div>
                        <div>
                            <label for="rSeq">结束序号</label>
                            <input v-model="rSeq" type="text" id="rSeq">
                        </div>
                    </div>
                    <div class="search-button">
                        <button type="submit" class="white-button">搜索</button>
                        <button class="white-button" id="resetButton">重置</button>
                    </div>
                </form>

                <div class="table-container" style="padding-top: 10px;">
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Content</th>
                                <th>LLM Label</th>
                                <th>SLM Label</th>
                                <th>Manual Label</th>
                                <th>Metric 1</th>
                                <th>Metric 2</th>
                                <th>Metric 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in resList" :key="item.id">
                                <td>{{ item.id }}</td>
                                <td>{{ item.data }}</td>
                                <td>{{ item.llmLabel }}</td>
                                <td>{{ item.slmLabel }}</td>
                                <td>{{ item.manualLabel }}</td>
                                <td>{{ item.loss }}</td>
                                <td>{{ item.representation }}</td>
                                <td>{{ item.confidence }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>

        </div>
    </ContentBase>
</template>
    
<script>

import ContentBase from '../components/ContentBase';
import { ref, onBeforeUnmount, onMounted } from 'vue';
// import { useStore } from 'vuex';
// import router from '@/router/index';
import $ from 'jquery';
import mitt from 'mitt';


export default {
    name: 'TrackBoard',
    components: {
        ContentBase,
    },
    setup() {
        let taskId = '1';
        let taskInfo = ref([]);
        let progressInfo = ref([]);

        const canvasContainer = ref(null);
        let ctx = null;
        let circleColor = ref('rgb(222,93,9)');

        function drawCircle(x, y, color) {
            ctx.beginPath();
            ctx.arc(x, y, 48, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.stroke();
            ctx.fill();
        }

        function drawLine(startX, startY, endX, endY) {
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
        }

        function drawText(text, x, y) {
            ctx.fillStyle = 'black';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(text, x, y);
        }

        onMounted(() => {
            const canvas = document.createElement('canvas');
            canvas.height = 120;
            canvasContainer.value.appendChild(canvas);
            ctx = canvas.getContext('2d');
            drawCircle(50, 50, circleColor.value);
            drawCircle(250, 50, 'white');
            drawLine(100, 50, 200, 50);
            drawText('LLM', 50, 50);
            drawText('SLM', 250, 50);
            const resetButton = document.querySelector('#resetButton');
            resetButton.addEventListener('click', resetForm);

            $('#manual-correction').click(function () {
                var url = '/correctionView/?taskId=' + encodeURIComponent(taskId) + '&currentEpoch=' + encodeURIComponent(progressInfo.value.currentEpoch);
                window.open(url);
            });

            // 这里还要再修修
            $('#csv2user').click(function () {
                var table = document.querySelector('.table-container table');
                if (!table) return;
                var csvContent = "data:text/csv;charset=utf-8,";
                // 处理表头
                var headers = [];
                var headerCells = table.querySelectorAll('thead th');
                headerCells.forEach(function (cell) {
                    headers.push(cell.innerText);
                });
                csvContent += '"' + headers.join('","') + '"\n';
                // 处理表格内容
                resList.value.forEach(function (item) {
                    var rowData = Object.values(item);
                    rowData.forEach(function (value, index) {
                        if (typeof value === 'string') {
                            rowData[index] = '"' + value.replace(/"/g, '""') + '"';
                        }
                    });
                    csvContent += rowData.join(',') + '\n';
                });
                // 创建并下载 CSV 文件
                var encodedUri = encodeURI(csvContent);
                var link = document.createElement("a");
                link.setAttribute("href", encodedUri);
                link.setAttribute("download", "dataset.csv");
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });

            // 接口21
            $('input[type="checkbox"]').on('change', function () {
                // 获取复选框的选中状态
                var isChecked = $('input[type="checkbox"]').prop('checked') ? 1 : 0;
                var manualCorrectionButton = $('#manual-correction');
                if (isChecked) {
                    manualCorrectionButton.removeClass('orange-button');
                    manualCorrectionButton.addClass('grey-button');
                    manualCorrectionButton.prop('disabled', true);
                } else {
                    manualCorrectionButton.removeClass('grey-button');
                    manualCorrectionButton.addClass('orange-button');
                    manualCorrectionButton.prop('disabled', false);
                }
                $.ajax({
                    url: 'http://localhost:8082/task/stepOver',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        taskId: taskId,
                        stepOver: isChecked
                    }),
                    success: function (resp) {
                        // 请求成功处理响应
                        console.log(resp);
                    },
                    error: function () {
                        // 请求失败处理错误
                        console.error('处理失败');
                    }
                });
            });
        });


        // 接口5
        $.ajax({
            url: 'http://localhost:8082/task/info',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                taskId: taskId
            }),
            success(resp) {
                // console.log(resp);
                taskInfo.value = resp.data;
                // console.log(taskInfo.value);
            }
        });
        // const progressInfo = ref([]);
        const emitter = mitt();
        // 接口18
        $.ajax({
            url: 'http://localhost:8082/task/progress/check',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                id: 1
            }),
            success(resp) {
                progressInfo.value = resp.data;
                if (progressInfo.value.currentModel == "1") {
                    progressInfo.value.currentModel = "LLM";
                }
                else if (progressInfo.value.currentModel == "2") {
                    progressInfo.value.currentModel = "SLM";
                }
                if (progressInfo.value.isCorrecting == "1") {
                    progressInfo.value.isCorrecting = "人工修改";
                }
                else if (progressInfo.value.isCorrecting == "0") {
                    progressInfo.value.isCorrecting = "执行中";
                }
            }
        });
        // 定时轮询
        const timer = setInterval(() => {
            $.ajax({
                url: 'http://localhost:8082/task/progress/check',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    id: 1
                }),
                success(resp) {
                    progressInfo.value = resp.data;
                    if (progressInfo.value.currentModel == "1") {
                        progressInfo.value.currentModel = "LLM";
                    }
                    else if (progressInfo.value.currentModel == "2") {
                        progressInfo.value.currentModel = "SLM";
                    }
                    if (progressInfo.value.isCorrecting == "1") {
                        progressInfo.value.isCorrecting = "人工修改";
                    }
                    else if (progressInfo.value.isCorrecting == "0") {
                        progressInfo.value.isCorrecting = "执行中";
                    }
                }
            });

            if (progressInfo.value.currentModel == "LLM") {
                drawCircle(50, 50, circleColor.value);
                drawCircle(250, 50, 'white');
                drawText('LLM', 50, 50);
                drawText('SLM', 250, 50);
            }
            else if (progressInfo.value.currentModel == "SLM") {
                drawCircle(50, 50, 'white');
                drawCircle(250, 50, circleColor.value);
                drawText('LLM', 50, 50);
                drawText('SLM', 250, 50);
            }
        }, 2000);
        onBeforeUnmount(() => {
            clearInterval(timer);
        });
        let certainSeq = ref('');
        let lSeq = ref('');
        let rSeq = ref('');
        let resList = ref([]);
        function resetForm() {
            certainSeq.value = "";
            lSeq.value = "";
            rSeq.value = "";
            resList.value = [];
        }
        const submitQuery = () => {
            // console.log(certainSeq.value, lSeq.value, rSeq.value);
            if (certainSeq.value === "") {
                certainSeq.value = "-1";
            }
            // 接口25
            $.ajax({
                url: 'http://localhost:8082/task/labeling/search',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    taskId: taskId,
                    seq: certainSeq.value,
                    lseq: lSeq.value,
                    rseq: rSeq.value,
                }),
                success(resp) {
                    // console.log(certainSeq.value);
                    // console.log(resp);
                    resList.value = resp.data;
                    // console.log(resList.value);
                    certainSeq.value = "";
                    lSeq.value = "";
                    rSeq.value = "";
                }
            });
        }
        return {
            taskId,
            taskInfo,
            progressInfo,
            certainSeq,
            lSeq,
            rSeq,
            submitQuery,
            resList,
            emitter,
            canvasContainer,
        }
    },

}

</script>
<style scoped>
.red {
    background-color: red;
}

#canvasContainer {
    position: relative;
}

canvas {
    position: relative;
}

.distance {
    width: 100px;
    height: 30px;
    font-size: 12px;
    padding: 5px 24px;
}

.orange-button {
    background-color: rgb(246, 103, 11);
    color: white;
}

.grey-button {
    background-color: rgb(170, 170, 170);
    color: white;
}

.white-button {
    background-color: white;
}

.whole-div {
    height: auto;
}

.button-container {
    display: flex;
    justify-content: space-evenly;
    /* z-index: 2; */
}

.search-button {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
    margin-right: 85px;
    /* 调整按钮的右边距 */
}

.search-button button {
    margin-left: 10px;
    /* 调整两个按钮之间的间距 */
}

.input-container {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
}

.input-container div {
    flex: 1;
    margin-right: 10px;
}

.table-container {
    display: flex;
    justify-content: center;
}

table {
    border-collapse: collapse;
}

th,
td {
    border: 1px solid black;
    padding: 8px;
}
</style>