<template>
<div id="navBarTop">
  <div class="leftBar">
    <div class="logoImg"><img src="../img/logo.png"/></div>
    <div class="logo">{{logo}}</div>
  </div>
  <div class="rightBar">
    <div class="login">
      <i class="icon-mine"></i>
      <div class="loginUser">{{loginUser}}</div>
    </div>
    <div class="exit">
      <i class="icon-exit"></i>
      <div class="exitUser">{{exitUser}}</div>
    </div>

  </div>
</div>
</template>

<script>
    export default {
      name: 'navBarTop',
      data() {
        return {
          logo:'大数据智能监控警告平台',
          loginUser:'登录',
          exitUser:'退出',
        }

      },
    }
</script>

<style scoped>
.logoImg{
    color: #fff;
    float: left;
    padding: 0 0.7rem;
    margin: 0.8rem 0.2rem;
    font-size: 1rem;
    font-weight: bold;
}
.logoImg img{
     width: 2.5rem;
}
.logo{
  float: left;
  font-size: 1rem;
  padding: 0 1.1rem;
  margin: 1.15rem 0;
  color: #fff;
  font-weight: lighter;
  border-left: 1px solid #4a4f50;
}
.rightBar i{
  font-size:1.25rem;
  color:#3f404b;
  float:left;
}
.rightBar{
  float: right;
  overflow: hidden;
  margin: 1.15rem 0;

}
.rightBar>div{
  float:left;
  padding: 0 1.75rem;
}
.rightBar .login{
  border-right: 1px solid #4a4f50;
}
.loginUser,.exitUser{
  display: inline-block;
  float:left;
  margin-left: 0.2rem;
  font-size:0.85rem;
  color:#3f404b;
  font-weight: lighter;
}
</style>
