<template>
    <!-- <ContentBase> -->
    <div class="row whole-div">
        <div class="row">
            <div class="headline-div">
                <div class="headline">
                    LLM Labeling
                </div>
            </div>
        </div>
        <div class="row">
            <el-steps style="max-width: 1000px; text-align: center" :active="1" align-center finish-status="wait"
                process-status="success" simple>
                <el-step title="Task Configuration" style="min-width: 300px;" />
                <el-step title="LLM Labeling" />
                <el-step title="SLM Filtering" />
                <el-step title="Result Display" style="max-width: 130px;" />
            </el-steps>
        </div>
        <div class="col-md-4 border-end position-relative">
            <div style="text-align: center; font-size: 25px;"><strong>Task
                    Information</strong></div>
            <div style=" margin-top: 1rem;">
                <div style="text-align: left; display: flex; flex-direction: column; justify-content: center; margin-left: 22%;">
                    <p><span style="color: rgb(246,103,11);">Task Name: </span>{{ TaskName }}</p>
                    <p><span style="color: rgb(246,103,11);">LLM Model: </span>{{ GPT }}</p>
                    <p><span style="color: rgb(246,103,11);">SLM Model: </span>{{ BERT }}</p>
                </div>
            </div>
            <div style="margin-top: 2px;">
                <img src="../../images/llm.png" width="350" alt="no pic">
            </div>
            <div style="margin-top: 1rem; font-size: 25px;"><strong>LLM Running Progress</strong></div>
            <div style="margin-top: 10px;">
                <div>
                    <el-progress type="circle" :percentage="percentage" :color="colors" :width="140"></el-progress>
                </div>
            </div>
        </div>
        <div class="col-md-8 position-relative">
            <!-- <div class="table-container">
                <table>
                    <thead>
                        <tr style="background-color: rgb(245,245,245);" class="fixed-width-cell">
                            <th width="40">ID</th>
                            <th>Content</th>
                            <th>LLM Label</th>
                            <th>SLM Label</th>
                            <th>Ranking</th>
                            <th>Confidence</th>
                            <th>Manual Label</th>
                        </tr>
                    </thead>
                    <tbody ref="tableBody">
                        <tr v-for="(row, index) in csvData" :key="row">
                            <td>{{ index }}</td>
                            <td>{{ row[0] }}</td>
                            <td :style="{ color: updatedColumn2[index] === 'labeling..' ? 'rgb(191,191,0)' : 'black' }">
                                {{ updatedColumn2[index] }}</td>
                            <td style="background-color: rgb(215,215,215);"></td>
                            <td style="background-color: rgb(215,215,215);"></td>
                            <td style="background-color: rgb(215,215,215);"></td>
                            <td style="background-color: rgb(215,215,215);"></td>
                        </tr>
                    </tbody>
                </table> -->
            <!-- <div>
                        <button @click="previousPage" :disabled="currentPage === 1">上一页</button>
                        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
                    </div> -->
            <!-- </div> -->

            <el-table :data="tableData" :loading="isLoading" :empty-text="emptyText" border style="width: 100%"
                class="table-container" :header-row-style="{ background: '#f5f7fa' }">
                <el-table-column prop="id" label="ID" width="80" class="custom-header"
                    :header-cell-style="{ background: '#ff9900' }" />
                <el-table-column prop="Content" label="Content" show-overflow-tooltip="true"
                    header-cell-style="background-color: #ff9900;">
                    <template v-slot="scope">
                        <div class="table-cell">
                            <strong>{{ scope.row.Content }}</strong>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column prop="LLMLabel" label="LLM Label" width="180">
                    <template v-slot="scope">
                        <div :style="{ color: updatedColumn2[scope.$index] === 'labeling..' ? 'rgb(191,191,0)' : 'black' }">
                            <strong>{{ updatedColumn2[scope.$index] }}</strong>
                            <!-- {{ scope.row.LLMLabel === 0 ? 'neg' : 'pos' }} -->
                        </div>
                    </template>
                </el-table-column>
                <!-- <el-table-column label="SLM Label" />
                <el-table-column label="Gaussian Ranking" />
                <el-table-column label="Confidence" />
                <el-table-column label="Manual Label">
                    <template #default="{ row }">
                        <el-select v-if="showOptions === 0" v-model="row.selectedOption" placeholder="Select an option">
                            <el-option label="Option 1" value="option1" />
                            <el-option label="Option 2" value="option2" />
                        </el-select>
                    </template>
                </el-table-column> -->
            </el-table>
            <div class="button-container">
                <!-- <button id="NextPage" class="blue-button">
                        Next
                    </button> -->
                <el-button type="primary" id="NextPage" style="width: 200px">Next</el-button>
            </div>
        </div>
    </div>
    <!-- </ContentBase> -->
</template>
    
<script>

// import ContentBase from '../components/ContentBase';
import { ref, onMounted, computed } from 'vue';
// import { useStore } from 'vuex';
// import router from '@/router/index';
import $ from 'jquery';
// import mitt from 'mitt';
// import Papa from 'papaparse';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie';

export default {
    name: 'LLMView2',
    components: {
        // ContentBase,
    },
    setup() {

        //加cookie
        let BERT = ref('');
        BERT = Cookies.get('slm');
        console.log(BERT);

        let GPT = ref('');
        GPT = Cookies.get('llm');
        console.log(GPT);

        let TaskName = ref('');
        TaskName = Cookies.get('TaskName');
        console.log(TaskName);

        // let loading = ref(true);
        let isLoading = ref(false);
        const emptyText = computed(() => {
            return isLoading.value ? 'Loading Data...' : 'no data';
        });
        let tableData = ref([]);
        // const activeStepDescription = ref(1);
        let percentage = ref(0);
        const colors = [
            { color: "#f56c6c", percentage: 20 },
            { color: "#e6a23c", percentage: 40 },
            { color: "#5cb87a", percentage: 60 },
            { color: "#1989fa", percentage: 80 },
            { color: "#6f7ad3", percentage: 100 },
        ];
        const csvData = ref([]);
        const updatedColumn2 = ref([]);
        let taskId = '1';
        let taskInfo = ref([]);
        let backendData = ref([]);
        let progressInfo = ref([]);
        const currentPage = ref(1);
        const rowsPerPage = 6; // 每页显示的行数

        const displayedData = computed(() => {
            const startIndex = (currentPage.value - 1) * rowsPerPage;
            const endIndex = startIndex + rowsPerPage;
            return csvData.value.slice(startIndex, endIndex);
        });

        const totalPages = computed(() => Math.ceil(csvData.value.length / rowsPerPage));
        function previousPage() {
            if (currentPage.value > 1) {
                currentPage.value--;
            }
        }

        function nextPage() {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
            }
        }

        //获取上个页面数据
        const router = useRouter();
        let raw_dynamicTags = []
        raw_dynamicTags = router.currentRoute.value.query;
        let dynamicTags = ref(Object.values(raw_dynamicTags));

        console.log(dynamicTags)
        console.log(raw_dynamicTags)


        const labelMap = {};
        dynamicTags.value.forEach((tag, index) => {
            labelMap[index] = tag;
        });

        onMounted(async () => {
            document.title = 'LLM Labeling';
            $('#NextPage').click(function () {
                // var url = '/SLMView/';
                // window.location.href = url;
                router.push({ path: "/SLMView", query: Object.values(raw_dynamicTags) });
            });


            let index = 0;
            while (index < tableData.value.length) {
                updatedColumn2.value[index] = ""
                index++;
            }
            index = 0
            updatedColumn2.value[0] = "labeling.."
            // axios.post('/llm')
            //     .then(response => {
            //         const ttpp = response.data.data;
            //         // console.log(ttpp.length);
            //         let idx = 0;
            //         while (idx < 200) {
            //             const confidencePercentage = (ttpp[idx].Confidence * 100).toFixed(2) + "%";
            //             ttpp[idx].Confidence = confidencePercentage;
            //             tableData.value.push(ttpp[idx]);
            //             idx++;
            //         }
            //     })
            //     .catch(error => {
            //         console.error(error);
            //     });
            const interval = 1000;

            let statecode = 0;


            // const askforLLMData = () => {
            //     axios.get('/llm')
            //         .then(response => {
            //             const ttpp = response.data.data;
            //             statecode = response.data.code;
            //             console.log(statecode);
            //             if (statecode === 200) {
            //                 console.log("结束:"+statecode);
            //                 clearInterval(tpm);
            //             }
            //             // console.log(ttpp.length);
            //             let idx = 0;
            //             while (idx < 200) {
            //                 const confidencePercentage = (ttpp[idx].Confidence * 100).toFixed(2) + "%";
            //                 ttpp[idx].Confidence = confidencePercentage;
            //                 tableData.value.push(ttpp[idx]);
            //                 idx++;
            //             }
            //         })
            //         .catch(error => {
            //             console.error(error);
            //         });
            // };
            // let tpm = setInterval(askforLLMData, interval);

            // var interval1 = setInterval(function () {

            console.log("开始" + statecode)
            // if (statecode === '200') {
            //     console.log("结束:" + statecode);
            //     clearInterval(interval1);
            // }
            isLoading.value = true;
            axios.get('/llm/refinery')
                .then(response => {
                    const ttpp = response.data.data;
                    statecode = response.data.code;
                    console.log(statecode);
                    isLoading.value = false;
                    // console.log(ttpp.length);
                    let idx = 0;
                    while (idx < 200) {
                        const confidencePercentage = (ttpp[idx].Confidence * 100).toFixed(2) + "%";
                        ttpp[idx].Confidence = confidencePercentage;
                        tableData.value.push(ttpp[idx]);
                        idx++;
                    }
                    const updateColumn2 = () => {
                        if (index < 200) {
                            // console.log(labelMap[tableData.value[index].LLMLabel]);
                            updatedColumn2.value[index] = labelMap[tableData.value[index].LLMLabel]; // 更新第2列的数据
                            if (index < 100) {
                                updatedColumn2.value[index + 1] = "labeling.."
                            }
                            index++;
                        }
                        // percentage.value = Math.min(parseFloat((percentage.value + 1.15).toFixed(2)), 100);
                    };
                    setInterval(updateColumn2, interval);
                    const updateper = () => {
                        percentage.value = Math.min(parseFloat((percentage.value + 1.15).toFixed(2)), 100);
                    };
                    setInterval(updateper, interval);
                })
                .catch(error => {
                    console.error(error);
                });


            // }, 2000);


            // }
            // try {
            //     const updateColumn2 = () => {
            //         if (index < 200) {
            //             // console.log(labelMap[tableData.value[index].LLMLabel]);
            //             updatedColumn2.value[index] = labelMap[tableData.value[index].LLMLabel]; // 更新第2列的数据
            //             if (index < 100) {
            //                 updatedColumn2.value[index + 1] = "labeling.."
            //             }
            //             index++;
            //         }
            //     };
            //     setInterval(updateColumn2, interval);
            //     const updateper = () => {
            //         percentage.value = Math.min(parseFloat((percentage.value + 0.115).toFixed(2)), 100);
            //     };
            //     setInterval(updateper, interval);
            // } catch (error) {
            //     console.error('Error fetching CSV data:', error);
            // }


        });
        // 接口5
        // $.ajax({
        //     url: 'http://localhost:8082/task/info',
        //     type: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({
        //         taskId: taskId
        //     }),
        //     success(resp) {
        //         // console.log(resp);
        //         taskInfo.value = resp.data;
        //         // console.log(taskInfo.value);
        //     }
        // });
        // $.ajax({
        //     url: 'http://localhost:8082/manual/labeling/correcting/recommend',
        //     type: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({
        //         taskId: 1,
        //         currentEpoch: 1
        //     }),
        //     success(resp) {
        //         backendData.value = resp.data;
        //         // console.log(taskInfo.value);
        //     }
        // });
        // const emitter = mitt();
        // // 接口18
        // $.ajax({
        //     url: 'http://localhost:8082/task/progress/check',
        //     type: 'POST',
        //     contentType: 'application/json',
        //     data: JSON.stringify({
        //         id: 1
        //     }),
        //     success(resp) {
        //         progressInfo.value = resp.data;
        //         if (progressInfo.value.currentModel == "1") {
        //             progressInfo.value.currentModel = "LLM";
        //         }
        //         else if (progressInfo.value.currentModel == "2") {
        //             progressInfo.value.currentModel = "SLM";
        //         }
        //         if (progressInfo.value.isCorrecting == "1") {
        //             progressInfo.value.isCorrecting = "人工修改";
        //         }
        //         else if (progressInfo.value.isCorrecting == "0") {
        //             progressInfo.value.isCorrecting = "执行中";
        //         }
        //     }
        // });
        // 定时轮询
        // const timer = setInterval(() => {
        //     $.ajax({
        //         url: 'http://localhost:8082/task/progress/check',
        //         type: 'POST',
        //         contentType: 'application/json',
        //         data: JSON.stringify({
        //             id: 1
        //         }),
        //         success(resp) {
        //             progressInfo.value = resp.data;
        //             if (progressInfo.value.currentModel == "1") {
        //                 progressInfo.value.currentModel = "LLM";
        //             }
        //             else if (progressInfo.value.currentModel == "2") {
        //                 progressInfo.value.currentModel = "SLM";
        //             }
        //             if (progressInfo.value.isCorrecting == "1") {
        //                 progressInfo.value.isCorrecting = "人工修改";
        //             }
        //             else if (progressInfo.value.isCorrecting == "0") {
        //             }
        //         }
        //     });

        // }, 2000);
        // onBeforeUnmount(() => {
        //     clearInterval(timer);
        // });




        return {
            csvData,
            updatedColumn2,
            taskId,
            taskInfo,
            backendData,
            progressInfo,
            percentage,
            colors,
            displayedData,
            currentPage,
            totalPages,
            previousPage,
            nextPage,
            tableData,
            labelMap, isLoading,
            emptyText,
            // activeStepDescription,
            BERT, GPT, TaskName
        }
    },

}

</script>
<style scoped>
.table-cell {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.last-three {
    background-color: rgb(215, 215, 215);
}

.fixed-width-table {
    table-layout: fixed;
    width: 100%;
}

.fixed-width-cell {
    width: 100px;
    /* 设置你想要的固定宽度 */
    word-wrap: break-word;
    /* 长内容换行显示 */
}

.headline-div {
    border-width: 0px;
    border-bottom-width: 1px;
    border-style: solid;
    border-color: rgba(242, 242, 242, 1);
    margin-bottom: 10px;
}

.headline {
    font-weight: 650;
    font-style: normal;
    font-size: 32px;
    color: #333333;
    text-align: left;
}

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

.blue-button {
    background-color: rgb(22, 155, 213);
    color: white;
    width: 200px;
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
    margin-left: 200px;
    margin-right: 200px;
    border-width: 1px;
    border-style: solid;
    border-color: rgba(242, 242, 242, 1);
}

.button-container {
    margin-top: 10px;
    padding-top: 10px;
    display: flex;
    justify-content: space-evenly;
    padding-bottom: 10px;
    border-width: 0px;
    border-top-width: 1px;
    border-style: solid;
    border-color: rgba(242, 242, 242, 1);
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
    margin-top: 10px;
    display: flex;
    justify-content: center;
    height: 540px;
    /* 设置容器的固定高度 */
    overflow-y: scroll;
    /* 添加垂直滚动条 */
}

table {
    border-collapse: collapse;
}

th,
td {
    border: 1px solid #ccc;
    padding: 8px;
}
</style>