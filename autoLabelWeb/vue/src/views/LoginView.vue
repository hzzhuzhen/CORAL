<template>
  <div class="LoginView">
    <div class="header">
      <router-link to="/HomeView" class="header-link">网页首站</router-link>
      <router-link to="/" class="header-link">联系我们</router-link>
    </div>
    <div class="body">
      <div class="background">
        <div class="login-container">
          <h2>Login</h2>
          <form @submit.prevent="login">
            <div class="form-group">
              <label for="username">
                <span class="icon">👤</span> Username:
              </label>
              <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
              <label for="password">
                <span class="icon">🔒</span> Password:
              </label>
              <input type="password" id="password" v-model="password" required>
            </div>
            <div v-if="loginError" class="error-message">
              {{ errorMessage }}
            </div>
            <button type="submit">Login</button>
          </form>

          <router-link to="/register" class="register-link">Register</router-link>
          <button @click="test">test</button>
          <LogoutTokenButton/>
        </div>
      </div>
    </div>
    <div class="footer">
      <router-link to="/" class="footer-link">关于我们</router-link>
      <router-link to="/" class="footer-link">法律声明</router-link>
      <router-link to="/" class="footer-link">隐私政策</router-link>
      <router-link to="/" class="footer-link">廉政举报</router-link>
      <router-link to="/" class="footer-link">联系我们</router-link>
      <router-link to="/" class="footer-link">加入我们</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from "js-cookie";
import {inject} from "vue";
import CryptoJS from 'crypto-js';
import LogoutTokenButton from "@/components/LogoutTokenButton.vue";

export default {
  components: {LogoutTokenButton},
  data() {
    return {
      username: '',
      password: '',
      loginError: false,
      errorMessage: '', // 新增错误信息变量
      token: '',
      demoApi: inject('demoApi')
    };
  },
  methods: {
    // md5Encrypt(text) {
    //   return CryptoJS.MD5(text).toString();
    // },
    test() {
      axios
          .get(this.demoApi + '/test/hello', {
            headers: {
              CORAL_token: Cookies.get('token')
            }
          })
          .then(response => {
            alert(response.data.code);
            console.log(response);
          })
          .catch(error => {
            // 处理其他登录失败的逻辑
            console.error('Login failed:', error);
          });


    },
    login() {
      console.log("demoApi=" + this.demoApi);
      console.log("password:" + CryptoJS.MD5(this.password));
      // 发送登录请求
      axios.post(this.demoApi + '/users/login', {
        name: this.username,
        password: CryptoJS.MD5(this.password).toString()//this.password
      })
          .then(response => {
            if (response.data.code === 200) {
              //存token
              Cookies.set("token", response.data.data.CORAL_token);
              // 处理登录成功的逻辑
              console.log('Login successful:' + response.data.message);
              this.$router.push('/createtask');
            } else {
              // 处理登录失败的逻辑
              console.error('Login failed:', response.data.message);
              this.loginError = true;
              this.errorMessage = response.data.message;
            }
          })
          .catch(error => {
            // 处理其他登录失败的逻辑
            console.error('Login failed:', error);
            this.loginError = true;
            this.errorMessage = 'An unexpected error occurred.';
          });
    }
  }
};
</script>

<style scoped>
.LoginView {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: flex-end;
  padding: 10px 20px;
  background-color: #f5f5f5;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-link {
  margin-left: 20px;
  color: #757575; /* 默认灰色 */
  font-size: 16px;
  text-decoration: none;
  transition: color 0.3s, text-shadow 0.3s;
}

.header-link:hover {
  color: #1e88e5; /* 鼠标悬浮时颜色 */
  text-shadow: 0 0 6px rgba(30, 136, 229, 0.5); /* 悬浮时增加光晕效果 */
}

.body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background {
  background-image: url('@/assets/LoginView-background.png');
  background-size: cover;
  width: 100vw;
  height: calc(100vh - 44px - 61px); /* header 44px  footer 61px */
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  max-width: 450px;
  margin: auto;
  min-width: 400px;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #e3f2fd, #f9f9f9);
  background: rgba(255, 255, 255, 0.85);
  text-align: center;
  animation: fadeIn 1s ease-in-out;
}

h2 {
  margin-bottom: 30px;
  color: #333;
  font-size: 28px;
  font-weight: 700;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
  position: relative;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
  font-size: 14px;
}

.icon {
  margin-right: 8px;
}

input {
  width: 100%;
  padding: 10px;
  padding-left: 32px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
  outline: none;
  font-size: 16px;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
  border-color: #42a5f5;
  box-shadow: 0 0 8px rgba(66, 165, 245, 0.5);
}

button {
  width: 100%;
  padding: 12px;
  background-color: #42a5f5;
  border: none;
  border-radius: 5px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
  margin-top: 10px;
}

button:hover {
  background-color: #1e88e5;
  box-shadow: 0 4px 12px rgba(30, 136, 229, 0.3);
}

.error-message {
  color: #e53935;
  margin-top: 10px;
  font-size: 14px;
}

.register-link {
  display: block;
  margin-top: 20px;
  color: #42a5f5;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.register-link:hover {
  color: #1e88e5;
  text-decoration: underline;
}

.footer {
  display: flex;
  justify-content: center; /* 链接居中对齐 */
  padding: 20px 0;
  background-color: #f5f5f5;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
}

.footer-link {
  margin: 0 15px;
  color: #757575; /* 默认灰色 */
  font-size: 14px;
  text-decoration: none;
  transition: color 0.3s, text-shadow 0.3s;
}

.footer-link:hover {
  color: #FF4500; /* 悬浮时橙红色 */
  text-shadow: 0 0 6px rgba(255, 69, 0, 0.5); /* 橙红色光晕效果 */
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

