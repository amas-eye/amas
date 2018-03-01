<template>
  <div class="login">
    <div class="form">
      <div class='headtab'>
        <div class="ch-title">
          登录
        </div>
        <!-- <div class="en-title">
              WiFi Bid Data Platform
            </div> -->
      </div>
      <!-- <div class="welcom">
            欢迎使用WiFi大数据平台</br>请输入用户信息
          </div> -->
      <div class="login-form">
        <div class="login-text">
          <input v-model="login_info.account" type='text' placeholder="请输入邮箱或者手机号" />
        </div>
        <div style='margin-bottom:0;' class="login-text">
          <input v-model="login_info.password" type='password' placeholder="请输入密码" />
        </div>
        <div class="core">
          <div class="core-text">
            <input v-model="login_info.yzm" type='text' placeholder="请输入验证码" />
          </div>
          <img style="width:7rem; height:3rem;" @click="getcore()" :src="coresrc"></img>
          <!-- <span v-on:click="$router.push('forget_password')">忘记密码?</span> -->
        </div>
        <div class="login-buttonground">
          <!--mt-button class='login-button' v-on:click="login">登录</mt-button-->
          <button class='login-button' type="button" v-on:click="login()">登 入</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import http from 'service/myhttp'
  export default {
    name: 'login',
    components: {},
    data() {
      return {
        msg: '登录',
        coresrc: '',
        login_info: {
          account: null,
          password: null,
          yzm: null
        }
      }
    },
    methods: {
      getcore: function() {
        //更改地址获取验证码
        this.coresrc = '/wifi/login_Login_getIdCode?time=' + Math.random()
      },
      login: function() {
        // 登录
        http.post('login_Login_login', this.login_info).then(
          res => {
            //  console.log(res)
            if (res.data.resultCode == '000000') {
              //成功
              // console.log(this)
              this.$router.push('/main/exhibition')
            } else {
              //登录失败
              alert(res.data.resultMsg)
            }
          }
        )
      }
    },
    mounted() {},
    beforeRouteEnter: function(to, from, next) {
      //路由钩子
      // console.log('enter')
      next(vm => {
        //获取验证码
        vm.getcore()
      });
    },
    beforeRouteLeave: function(to, from, next) {
      // console.log('leave')
      next();
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  input::-webkit-input-placeholder {
    color: #fff;
  }
  .headtab {
    background-color: transparent !important;
    color: #fff !important;
    text-align: left;
    padding: 1.5rem 2rem;
    /* border-bottom: 1px solid #ddd !important; */
  }
  .headtab .ch-title {
    border-bottom: 1px solid #ddd !important;
    font-size: 1.8rem;
    padding-bottom: 1.5rem;
  }
  .headtab .en-title {
    font-size: 4rem;
    padding-top: 2px;
  }
  .login-text {
    /* border: 1px solid #999; */
    border-radius: 0rem;
    margin: 0rem 0 2rem 0;
    text-align: center;
    padding: 1px 0%;
    background-color: #3C6792;
    color: #fff;
  }
  .core-text {
    /*border: 1px solid #999; */
    border-radius: 0rem;
    /* margin: 0rem 0 6rem 0; */
    text-align: center;
    /* padding: 1px 0%; */
    width: 12rem;
    float: left;
    background-color: #3C6792;
    color: #fff;
  }
  .core-text input {
    outline: 0;
    border: 0;
    padding: 1rem 1rem;
    width: 10rem;
    background: transparent;
    font-size: 1rem;
  }
  .login-text input,
  .verification_code .text input {
    outline: 0;
    border: 0;
    padding: 1rem 1rem;
    width: 17.7rem;
    font-size: 1rem;
    background-color: #3C6792;
    color: #fff;
  }
  .verification_code {
    display: table;
    width: 100%;
    margin: 0rem 0 6rem 0;
  }
  .verification_code .text input {
    width: 80%;
  }
  .verification_code .text {
    float: left;
    width: 56%;
    padding: 1px;
    border: 1px solid #999;
    border-radius: 2rem;
    text-align: center;
  }
  .verification_code button {
    float: right;
    border: 1px solid #999;
    padding: 3rem 4rem;
    font-size: 4rem;
    border-radius: 2rem;
    color: #999;
    background-color: #fff;
    outline: 0;
  }
  .login {
    background: -webkit-linear-gradient(140deg, #6C8CD9 40%, #50B9E9);
    background: -moz-linear-gradient(140deg, #6C8CD9 40%, #50B9E9);
    background: -o-linear-gradient(140deg, #6C8CD9 40%, #50B9E9);
    background: linear-gradient(140deg, #6C8CD9 40%, #50B9E9);
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .login-form {
    padding: 0% 4rem;
    margin-bottom: 3rem;
    /* margin-top: 6rem; */
  }
  .core {
    text-align: right;
    /* font-size: 3rem; */
    margin-top: 2rem;
    color: #999;
  }
  .login-buttonground {
    margin-top: 5rem;
  }
  .login-button {
    width: 100%;
    font-size: 1.3rem;
    height: 3rem;
    margin-bottom: 0rem;
    background-color: #3B6484;
    color: #fff;
    box-shadow: none;
    border: 0;
    /* padding: 1rem 0rem; */
  }
  .login .form {
    width: 28rem;
    /* height: 76%; */
    background-color: rgba(0, 0, 0, 0.25);
  }
  .welcom {
    margin: 50px 0px;
    text-align: center;
    color: #fff;
    font-size: 4rem;
  }
</style>
