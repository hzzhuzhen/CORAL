<template>
  <!-- 根据当前步骤显示不同的内容 -->
  <!-- <ContentBase> -->
  <div class="row whole-div">
    <!-- <br />
    <h2 style="text-align: left">
      &nbsp; &nbsp; &nbsp; &nbsp;TASK CONFIGURATION
    </h2> -->
    <div class="row">
      <div class="headline-div">
        <div class="headline">
          Task Configuration
        </div>
      </div>
    </div>

    <!--    导航栏-->
    <model-use-step-bar :active="0"/>
    <!--=======-->
    <!--&gt;>>>>>> ecddfcc3e3f82b0a643e122ac9a8043a8a07fdfe-->
    <!--    <div class="row">-->
    <!--      <el-steps style="max-width: 1000px; text-align: center" :active="0" align-center finish-status="wait"-->
    <!--        process-status="success" simple>-->
    <!--        <el-step title="Task Configuration" style="min-width: 300px;" />-->
    <!--        <el-step title="LLM Labeling" />-->
    <!--        <el-step title="SLM Filtering" />-->
    <!--        <el-step title="Result Display" style="max-width: 130px;" />-->
    <!--      </el-steps>-->
    <!--    </div>-->

    <div class="create-task-container bold-label" style="max-height: 630px; overflow-y: auto">
      <el-form :model="taskForm" :rules="rules" ref="taskForm" label-width="120px" label-position="left">
        <!--第一部分-->
        <el-form-item label="Task Type:" label-width="300px" prop="taskType">
          <el-select v-model="taskForm.taskType" placeholder="Select task type" style="width: 400px">
            <el-option label="Sentiment Analysis" value="1"></el-option>
            <el-option label="Part-of-Speech Tagging" value="2"></el-option>
            <el-option label="Text Classification" value="3"></el-option>
            <el-option label="Text Summarization" value="4"></el-option>
            <el-option label="Semantic Role Labeling" value="5"></el-option>
            <!-- <el-option label="Machine Translation" value="6"></el-option> -->
            <el-option disabled style="color: #ccc; font-size: 25px;" label="... ..."></el-option>
          </el-select>
        </el-form-item>
        <!--任务名称-->
        <el-form-item label="Task Name:" label-width="300px" prop="name">
          <el-input v-model="taskForm.name" style="width: 400px"></el-input>
        </el-form-item>
        <!--上传文件-->
        <el-form-item label="Data To Be Annotated:" label-width="300px" prop="file">
          <el-upload class="upload-demo" action="/inputFile/upload" :before-upload="beforeUpload"
                     :on-success="handleUploadSuccess"
                     :on-error="handleUploadError" accept=".txt,.csv" style="width: 400px">
            <el-button size="small" type="primary">Upload</el-button>
          </el-upload>
          <!--          已丢弃-->
          <!--          <el-upload class="upload-demo" action="/llm" :before-upload="beforeUpload" :on-success="handleUploadSuccess"-->
          <!--                     :on-error="handleUploadError" accept=".txt,.csv" style="width: 400px">-->
          <!--            <el-button size="small" type="primary">Upload_direct_to_model(discard)</el-button>-->
          <!--          </el-upload>-->
        </el-form-item>

        <!--        标签-->
        <el-form-item label="Custom Label:" label-width="300px">
          <el-tag :key="tag" v-for="tag in dynamicTags" closable :disable-transitions="false" @close="handleClose(tag)">
            {{ tag }}
          </el-tag>
          <el-input class="input-new-tag" v-if="inputVisible" v-model="inputValue" ref="saveTagInput" size="small"
                    @keyup.enter="handleInputConfirm" @blur="handleInputConfirm">
          </el-input>
          <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Label</el-button>
          <template #label>
            <span>Custom Label:</span>
            <span style="color: #888; font-size: 12px; margin-left: 10px;">(Customize Corpus Labels)</span>
          </template>
        </el-form-item>

        <!--第二部分-->
        <div class="div1">
          <el-form-item label="LLM:" label-width="300px" label-suffix=":" prop="llmId">
            <el-select v-model="taskForm.llmId" placeholder="Please select" style="width: 400px">
              <el-option label="GPT 3.5 Turbo" value="1"></el-option>
              <el-option label="ERNIE Bot" value="2"></el-option>
            </el-select>
            <template #label>
              <span>LLM:</span>
              <span style="color: #888; font-size: 12px; margin-left: 10px;"> (Large Language Model)</span>
            </template>
          </el-form-item>

          <el-form-item label="Prompt Template:" label-width="300px" prop="templateContent1">
            <el-input type="textarea" :rows="8" style="width: 400px" placeholder="Enter Prompt Content"
                      v-model="taskForm.templateContent1"></el-input>
          </el-form-item>
        </div>
        <!--第三部分-->
        <div class="div2">
          <el-form-item label="SLM:" label-width="300px" prop="slmId">
            <el-select v-model="taskForm.slmId" placeholder="Please select" style="width: 400px">
              <el-option label="BERT" value="1"></el-option>
              <el-option label="RoBERTa" value="2"></el-option>
            </el-select>
            <template #label>
              <span>SLM:</span>
              <span style="color: #888; font-size: 12px; margin-left: 10px;">(Small Language Model)</span>
            </template>
          </el-form-item>

          <el-form-item label="Epoch:" label-width="300px">
            <el-input-number v-model="taskForm.epoch" :min="1" style="width: 400px"></el-input-number>
            <template #label>
              <span>Epoch:</span>
              <span style="color: #888; font-size: 12px; margin-left: 10px;"> (Training frequency)</span>
            </template>
          </el-form-item>
        </div>
        <!-- <el-form-item label="" label-width="0px">
          <div style="color: lightgray;">
            ----------------------------------------------------------------------------------
            -------------------------------------------------------------------------------------</div>
        </el-form-item> -->
        <!--第四部分-->
        <el-form-item label="Correction Set Selection Strategy:" label-width="300px" prop="strategy">
          <el-radio-group v-model="taskForm.strategy" style="width: 400px">
            <el-radio :label="1">Correction Set Selection by Gaussian Ranking</el-radio>
            <el-radio :label="2">Correction Set Selection by Confidence</el-radio>
            <!-- <el-radio :label="'Option3'">Option 3</el-radio> -->
          </el-radio-group>
        </el-form-item>
        <!--第五部分-->
        <el-form-item label="Correction Set Selection Threshold:" label-width="300px">
          <el-input-number v-model="taskForm.threshold" :min="0" style="width: 400px"></el-input-number>
        </el-form-item>
        <!--第六部分-->
        <el-form-item style="margin-left: 150px">
          <!-- 提交按钮 -->
          <el-button type="primary" @click="submitForm('taskForm')" style="width: 200px">Submit</el-button>
        </el-form-item>
        <DemoButton/>
      </el-form>
    </div>
  </div>

  <!-- <div v-show="active === 1">
    <div class="center-table">
      <h2>LLm返回结果展示：</h2>
      <el-table :data="taskForm.llmLabels" stripe style="width: 50%">
        <el-table-column prop="str" label="数据条目"></el-table-column>
        <el-table-column label="LLM标注标签" v-slot="scope">
          {{
            scope.row.i === 1
              ? "positive"
              : scope.row.i === 0
              ? "negative"
              : "null"
          }}
        </el-table-column>
      </el-table>
    </div>
    <el-button style="margin-top: 12px" @click="next">下一步</el-button>
  </div> -->

  <!-- 散点图 -->
  <!-- <div style="margin: 0 auto">
    <div id="echartsContainer" style="width: 1000px; height: 500px"></div>
  </div> -->

  <!-- <div v-show="active === 3">
    <h1>显示第3个界面</h1>
    <el-button style="margin-top: 12px" @click="next">下一步</el-button>
  </div> -->

  <!-- 进度条 -->
  <!-- <el-progress
    type="circle"
    :percentage="percentage"
    :color="colors"
  ></el-progress>
  <div>
    <el-button-group>
      <el-button icon="el-icon-minus" @click="decrease"></el-button>
      <el-button icon="el-icon-plus" @click="increase"></el-button>
    </el-button-group>
  </div> -->
  <!-- </ContentBase> -->
</template>

<script>
// import ContentBase from "../components/ContentBase";
import axios from "axios";
// import echarts from 'echarts';
import Cookies from 'js-cookie';
import ModelUseStepBar from "@/components/ModelUseStepBar.vue";
import DemoButton from "@/components/DemoButton.vue";

export default {
  components: {
    DemoButton,
    ModelUseStepBar
    // ContentBase,
  },
  data() {
    return {
      // dynamicTags: ["negative", "positive"],
      dynamicTags: [],
      inputVisible: false,
      inputValue: "",
      chart: null,
      percentage: 10,
      colors: [
        {color: "#f56c6c", percentage: 20},
        {color: "#e6a23c", percentage: 40},
        {color: "#5cb87a", percentage: 60},
        {color: "#1989fa", percentage: 80},
        {color: "#6f7ad3", percentage: 100},
      ],
      // 示例数据
      scatterData: [
        // [-20,-20,1],
        // [20,20,0]
      ],
      currentIndex: 0, // 跟踪当前显示的数组索引
      totalData: [],
      active: 0,
      taskForm: {
        strategy: 0,
        taskType: "",
        name: "",
        epoch: 1,
        inputDataUrl: "",
        llmId: "",
        slmId: "",
        threshold: 0,
        remark: "",
        selectedTemplate1: "",
        templateContent1: "",
        taskId: null,
        // fileList: [], // 新增的 fileList 字段用于存储已选择的文件
        // llmLabels: [],
      },
      templateOptions1: [
        {value: "1", label: "Template1"},
        {value: "2", label: "Template2"},
        // 添加更多模版选项
      ],
      rules: {
        taskType: [
          {required: true, message: '请选择一个选项', trigger: 'change'}
        ],
        name: [
          {required: true, message: '请输入', trigger: 'blur'}
        ],
        file: [
          {required: true, message: '请上传文件', trigger: 'change'}
        ],
        llmId: [
          {required: true, message: '请选择一个选项', trigger: 'change'}
        ],
        templateContent1: [
          {required: true, message: '请输入', trigger: 'blur'}
        ],
        slmId: [
          {required: true, message: '请选择一个选项', trigger: 'change'}
        ],
        strategy: [
          {required: true, message: '请选择一个选项', trigger: 'change'}
        ]
      }
    };
  },


  //选择类型type后的显示
  watch: {
    'taskForm.taskType': function (newVal) {
      if (newVal === "1") {
        this.taskForm.templateContent1 = `You are a helpful assistant for the task of text classification on the MR (Movie Review) dataset. You reply with brief, to-the-point answers with no elaboration as truthfully as possible. MR (Movie Review) dataset is used in sentiment-analysis experiments and this dataset contains movie-review documents labeled with respect to their overall sentiment polarity (positive or negative). Your task is to a binary classification to classify a movie review as positive or negative according to their overall sentiment polarity. The category is divided into two types: 'positive' and 'negative'.
Given the movie review as follows:
Enigma is well-made, but it's just too dry and too placid.
The weakest of the four harry potter books has been transformed into the stronger of the two films by the thinnest of margins.
How do you feel about the sentiment polarity of the given movie review, is this positive or negative? Please provide a list of phrases indicating the sentiment polarity for each review.
`;
      } else {
        this.taskForm.templateContent1 = 'Default text for other task types';
      }
    },
  },
  // mounted() {
  //   // 发起 GET 请求获取数据
  //   // axios
  //   //   .get("/python/sdt")
  //   //   .then((response) => {
  //   //     // 请求成功时将数据存储到 scatterData 中
  //   //     console.log(response.data);
  //   //     console.log(this.scatterData);
  //   //     this.totalData = response.data;
  //   //     console.log(this.totalData);
  //   //     // setInterval(() => {
  //   //     //   // 更新当前显示的数组索引
  //   //     //   this.currentIndex = (this.currentIndex + 1) % this.scatterData.length;
  //   //     // }, 5000);
  //   //     this.initECharts();
  //   //     // this.addScatterDataSlowly1(); // 开始添加数据
  //   //   })
  //   //   .catch((error) => {
  //   //     console.error("Error fetching data:", error);
  //   //   });
  // },

  methods: {
    handleClose(tag) {
      this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
    },

    showInput() {
      this.inputVisible = true;
      this.$nextTick(() => {
        this.$refs.saveTagInput.$refs.input.focus();
      });
    },

    handleInputConfirm() {
      let inputValue = this.inputValue;
      if (inputValue) {
        this.dynamicTags.push(inputValue);
      }
      this.inputVisible = false;
      this.inputValue = "";
    },

    // increase() {
    //   this.percentage += 1;
    //   if (this.percentage > 100) {
    //     this.percentage = 100;
    //   }
    // },
    // decrease() {
    //   this.percentage -= 1;
    //   if (this.percentage < 0) {
    //     this.percentage = 0;
    //   }
    // },
    initECharts() {
      // 初始化图表
      this.chart = this.$echarts.init(
          document.getElementById("echartsContainer")
      );

      // 使用this.chart设置图表的配置和数据
      this.setScatterChart();
    },
    setScatterChart() {
      // 设置散点图配置
      this.chart.setOption({
        xAxis: {
          type: "value",
          min: -15, // x 轴最小值
          max: 18, // x 轴最大值
        },
        yAxis: {
          type: "value",
          min: -10, // x 轴最小值
          max: 15, // x 轴最大值
        },
        series: [
          {
            type: "scatter",
            // progressive: 1000, // 开启渐进渲染
            // progressiveThreshold: 500, // 阈值，大于该值的数据才会采用渐进渲染

            // data: this.scatterData.map((item) => ({
            //   value: item,
            // })),

            data: this.totalData,
            symbolSize: 10, // 设置点的大小
            itemStyle: {
              color: (params) => {
                // 设置颜色的函数
                // 根据颜色属性判断颜色
                const color = params.data[2];
                return color === 0 ? "#f56c6c" : "#67c23a"; // 假设0为红色，1为绿色
              },
            },
          },
        ],
      });
    },
    addScatterDataSlowly1() {
      let index = 0;
      let batchSize = 100; // 每次增加的数据量
      let timer = setInterval(() => {
        // 计算本次要添加的数据范围
        let start = index;
        let end = Math.min(index + batchSize, this.totalData.length);
        // 将要添加的数据批量添加到 scatterData 中
        let newData = [];
        for (let i = start; i < end; i++) {
          newData.push(this.totalData[i]);
        }
        // 使用 appendData 方法追加数据
        this.chart.appendData({
          seriesIndex: 0,
          data: newData,
        });
        console.log(newData);
        // this.chart.resize();

        // 更新索引
        index = end;
        // 判断是否已添加完所有数据
        if (index >= this.totalData.length) {
          clearInterval(timer); // 数据添加完成后清除定时器
        }
      }, 200); // 间隔时间200毫秒
    },

    addScatterDataSlowly2() {
      let index = 0;
      let interval = 200; // 间隔时间200毫秒
      let batchSize = 100; // 每次增加的数据量
      let timer = setInterval(() => {
        // 计算本次要添加的数据范围
        let start = index;
        let end = Math.min(index + batchSize, this.totalData.length);
        // 将要添加的数据批量添加到 scatterData 中
        for (let i = start; i < end; i++) {
          let newData = this.totalData[i];
          this.scatterData.push(newData);
        }
        // 更新散点图数据
        this.chart.setOption({
          series: [
            {
              data: this.scatterData,
            },
          ],
        });
        // 更新索引
        index = end;
        // 判断是否已添加完所有数据
        if (index >= this.totalData.length) {
          clearInterval(timer); // 数据添加完成后清除定时器
        }
      }, interval);
    },

    // next() {
    //   if (this.active++ > 2) this.active = 0;
    // },

    beforeUpload(file) {
      // 文件上传前的处理逻辑
      console.log("文件上传前:", file);
      return true; // 返回 true 允许上传，返回 false 阻止上传
    },
    handleUploadSuccess(response, file) {
      // 处理文件上传成功
      console.log("文件上传成功:", response, file);
      this.taskForm.inputDataUrl = response.data; // 将上传成功后的文件地址赋值给 inputDataUrl
      console.log("url是:", response.data);
    },
    handleUploadError(error, file) {
      // 处理文件上传失败
      console.error("文件上传失败:", error, file);
      // 在这里可以提示用户文件上传失败的信息
      this.$message.error(`文件上传失败`);
      // : ${file.name}. ${error.message}
    },

    //对应的slm
    getSLMName(slmId) {
      if (slmId === "1") {
        return 'BERT';
      } else if (slmId === "2") {
        return 'RoBERTa';
      } else {
        return '';
      }
    },
    //对应的llm
    getLLMName(llmId) {
      if (llmId === "1") {
        return 'GPT 3.5 Turbo';
      } else if (llmId === "2") {
        return 'ERNIE Bot';
      } else {
        return '';
      }
    },
    submitForm(taskForm) {
      // 提交表单逻辑
      console.log("表单已提交:", taskForm);

      // 确保 this.$refs[this.taskForm] 引用的是有效的组件或 DOM 元素
      const formComponent = this.$refs[taskForm];
      if (!formComponent) {
        console.error(`找不到名为 ${taskForm} 的组件或 DOM 元素`);
        return;
      }

      // 调用 validate 方法
      formComponent.validate((valid) => {
        if (valid) {
          //alert('提交成功！');
        } else {
          console.log('表单校验未通过！');
        }
      });
      //表单不能有空
      if (!this.taskForm.taskType || !this.taskForm.name ||
          !this.taskForm.llmId || !this.taskForm.slmId ||
          !this.taskForm.templateContent1 || this.taskForm.strategy === 0 ||
          !this.taskForm.inputDataUrl) {
        this.$message.error('请输入完整');
        return 0;
      }
      // Cookies.set("llm", this.getLLMName(this.taskForm.llmId));
      // Cookies.set("slm", this.getSLMName(this.taskForm.slmId));
      // Cookies.set("TaskName", this.taskForm.name);
      // Cookies.set("strategy", this.taskForm.strategy);
      // Cookies.set("threshold", this.taskForm.threshold);
      // Cookies.set("taskid", this.taskForm.taskId);

      //提交到下一页面并跳转
      // this.$router.push({path: "/LLMView", query: this.dynamicTags});


      // const cookieValue2 = Cookies.get("slm");
      // console.log(cookieValue2);


      // 仅包括需要的字段，不包括 taskType
      // const formDataForRequest = {
      //   taskType: this.taskForm.taskType,
      //   name: this.taskForm.name,
      //   epoch: this.taskForm.epoch,
      //   inputDataUrl: this.taskForm.inputDataUrl,
      //   llmId: this.taskForm.llmId,
      //   slmId: this.taskForm.slmId,
      //   threshold: this.taskForm.threshold,
      //   remark: this.taskForm.remark,
      // };

      // 使用Axios发送POST请求
      // axios
      //   .post("/task/upset", formDataForRequest)
      //   .then((response) => {
      //     console.log("服务器响应:", response.data.data);
      //     // 在这里处理服务器响应，可以更新界面或执行其他操作
      //     // const params = {
      //     //   name: this.taskForm.name,
      //     //   taskType: this.taskForm.taskType,
      //     //   // taskId: this.taskId,
      //     // };

      //     // this.$router.push("/model_setting");
      //     // 使用 $router.push 进行跳转，并携带参数
      //     // this.$router.push({ path: "/model_setting", query: params });

      //     this.taskForm.taskId = response.data.data;
      //     console.log("taskId", this.taskForm.taskId);

      //     const formDataForRequest2 = [
      //       {
      //         content: this.taskForm.templateContent1,
      //         promptType: this.taskForm.selectedTemplate1,
      //         name: this.taskForm.name,
      //         taskType: this.taskForm.taskType,
      //         // taskId: this.taskForm.taskId,
      //         taskId: 1,
      //       },
      //     ];

      //     axios
      //       .post("/prompt/list/save", formDataForRequest2)
      //       .then((response) => {
      //         console.log("服务器响应:", response.data);
      //         // 处理服务器响应，跳转到下一步或其他操作
      //         // this.$router.push("/recommend");
      //         // const params = {
      //         //   // name: this.taskForm.name,
      //         //   // taskType: this.taskForm.taskType,
      //         //   // taskId1: this.taskForm.taskId,
      //         //   llmLabels: this.taskForm.llmLabels
      //         // };

      //         // this.$router.push({ path: "/recommend", query: params });
      //         // this.$router.push({ path: "/welcome", query: params });
      //         // if (this.active++ > 2) this.active = 0;
      //         // this.$router.push("/llmview");
      //       })
      //       .catch((error) => {
      //         console.error("请求失败:", error);
      //         // 处理请求失败的情况，提示用户或其他操作
      //       });
      //   })
      //   .catch((error) => {
      //     console.error("请求失败:", error);
      //     // 在这里处理请求失败的情况，可以提示用户或执行其他操作
      //   });
//     },
// // 新的前端提交代码
//     submitForm2() {
//       // 提交表单逻辑
//       console.log("表单已提交:", this.taskForm);
//       // 加cookie
//       // this.cookieName = "slm"
//       // this.cookieValue = "666"
//
//       Cookies.set("llm", this.getLLMName(this.taskForm.llmId));
//       Cookies.set("slm", this.getSLMName(this.taskForm.slmId));
//       Cookies.set("TaskName", this.taskForm.name);
//       Cookies.set("strategy", this.taskForm.strategy);
//       Cookies.set("threshold", this.taskForm.threshold);

      // const cookieValue2 = Cookies.get("slm");
      // console.log(cookieValue2);

      // 路由到下个页面 并传递数据过去
      // this.$router.push("/llmview");
      //this.$router.push({ path: "/llmview", query: this.dynamicTags });
      // 仅包括需要的字段，不包括 taskType
      if (this.taskForm.taskType == null) {
        this.taskForm.taskType = 0
      }
      const formDataForRequest = {
        taskType: this.taskForm.taskType,
        name: this.taskForm.name,
        epoch: this.taskForm.epoch,
        inputDataUrl: this.taskForm.inputDataUrl,
        llmId: this.taskForm.llmId,
        slmId: this.taskForm.slmId,
        threshold: this.taskForm.threshold,
        remark: this.taskForm.remark,
      };

      //使用Axios发送POST请求
      axios
          .post("/task/upset", formDataForRequest)
          .then((response) => {
            console.log("服务器响应:", response.data.data);
            console.log("remark:" + this.taskForm.remark);
            //在这里处理服务器响应，可以更新界面或执行其他操作
            const params = {
              name: this.taskForm.name,
              taskType: this.taskForm.taskType,
              // taskId: this.taskId,
            };
            console.log("params:", params);

            // this.$router.push("/model_setting");
            // // 使用 $router.push 进行跳转，并携带参数
            // this.$router.push({ path: "/model_setting", query: params });

            this.taskForm.taskId = response.data.data;
            console.log("taskId", this.taskForm.taskId);
            // 加cookie
            Cookies.set("llm", this.getLLMName(this.taskForm.llmId));
            Cookies.set("slm", this.getSLMName(this.taskForm.slmId));
            Cookies.set("TaskName", this.taskForm.name);
            Cookies.set("strategy", this.taskForm.strategy);
            Cookies.set("threshold", this.taskForm.threshold);
            Cookies.set("taskId", this.taskForm.taskId);

            const formDataForRequest2 = [
              {
                content: this.taskForm.templateContent1,
                promptType: this.taskForm.selectedTemplate1,
                name: this.taskForm.name,
                taskType: this.taskForm.taskType,
                taskId: this.taskForm.taskId
              },
            ];

            axios
                .post("/prompt/list/save", formDataForRequest2)
                .then((response) => {
                  console.log("服务器响应:", response.data);
                  // 处理服务器响应，跳转到下一步或其他操作
                  // this.$router.push("/recommend");
                  // const params = {
                  //   // name: this.taskForm.name,
                  //   // taskType: this.taskForm.taskType,
                  //   // taskId1: this.taskForm.taskId,
                  //   llmLabels: this.taskForm.llmLabels
                  // };

                  // this.$router.push({ path: "/recommend", query: params });
                  // this.$router.push({ path: "/welcome", query: params });
                  // if (this.active++ > 2) this.active = 0;
                  //this.$router.push({ path: "/llmview", query: this.dynamicTags });
                  this.$router.push("/llmview");

                })
                .catch((error) => {
                  console.error("请求失败:", error);
                  // 处理请求失败的情况，提示用户或其他操作
                });
          })
          .catch((error) => {
            console.error("请求失败:", error);
            // 在这里处理请求失败的情况，可以提示用户或执行其他操作
          });
    },
  },
};
</script>

<style scoped>
.div1 {
  border-width: 0px;
  border-top-width: 2px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
  /* margin-bottom: 10px; */
  padding-top: 10px;
}

.div2 {
  border-width: 0px;
  border-top-width: 2px;
  border-bottom-width: 2px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
  /* margin-bottom: 10px; */
  padding-top: 10px;
}

.whole-div {
  height: auto;
  margin-left: 200px;
  margin-right: 200px;
  border-width: 1px;
  border-style: solid;
  border-color: rgba(242, 242, 242, 1);
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
  font-size: 28px;
  color: #333333;
  text-align: left;
}

.create-task-container {
  /* max-width: 800px; */
  height: auto;
  width: 850px;
  margin: auto;
  padding: 20px;
  /* border: 1px solid #ccc; */
  /* border-radius: 5px; */
  /* box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); */

  justify-content: center;
  /* 水平居中 */
}

.el-form-item__label {
  font-weight: bold;
}

.center-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  /* 使得整个页面高度铺满视窗，视情况而定是否需要 */
}

.el-tag + .el-tag {
  margin-left: 10px;
}

.button-new-tag {
  margin-left: 10px;
  height: 32px;
  line-height: 30px;
  padding-top: 0;
  padding-bottom: 0;
}

.input-new-tag {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}

.bold-label {
  font-weight: bold;
  /* font-size: 140px !important; */
}

.error-input {
  border: 1px solid red;
  transition: border-color 0.3s ease; /* 添加过渡效果 */
}
</style>
   