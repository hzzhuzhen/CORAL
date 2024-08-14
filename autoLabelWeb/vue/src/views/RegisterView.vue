<template>
  <div class="Register-view">
    <div class="header">
      <router-link to="/HomeView" class="header-link">网页首站</router-link>
      <router-link to="/" class="header-link">联系我们</router-link>
    </div>
    <div class="body">
      <div class="border">
        <div class="register-wrapper">
          <div class="welcome-container">
            <h2>欢迎注册自动标注系统</h2>
          </div>
          <div class="register-container">
            <h2>Register</h2>
            <form @submit.prevent="register" class="register-form">
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
              <button type="submit">Register</button>
            </form>
            <router-link to="/LoginView" class="back-to-login">Back to Login</router-link>
          </div>
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
import {inject} from "vue";

export default {
  data() {
    return {
      username: '',
      password: '',
      demoApi: inject('demoApi')
    };
  },
  methods: {
    register() {
      console.log("demoApire=" + this.demoApi);
      // 发送注册请求
      axios.post(this.demoApi + '/users/register', {
        name: this.username,
        password: this.password
      })
          .then(response => {
            // 处理注册成功的逻辑
            if (response.data.code === 200) {
              console.log('Registration successful' + response.data);
              this.$router.push('/');
            } else if (response.data.code === 401) {
              alert("用户已存在");
            }

          })
          .catch(error => {
            // 处理注册失败的逻辑
            console.error('Registration failed:', error);
          });
    }
  }
};
</script>

<style scoped>
h2 {
  margin-bottom: 30px;
  color: #333;
  font-size: 28px;
  font-weight: 700;
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

.border {
  width: 100vw;
  height: calc(100vh - 44px - 61px); /* header 44px  footer 61px */
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e3f2fd, #f9f9f9);
}

.register-wrapper {
  text-align: center;
}

.welcome-container {
  margin-bottom: 20px;
}

.welcome-container h2 {
  font-size: 24px;
  color: #333;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.register-container {
  max-width: 450px;
  min-width: 400px;
  margin: auto;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #e3f2fd, #f9f9f9);
  text-align: center;
  font-family: 'Arial', sans-serif;
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
  padding: 10px 10px 10px 32px;
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

.back-to-login {
  display: block;
  margin-top: 20px;
  color: #42a5f5;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.back-to-login:hover {
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
  