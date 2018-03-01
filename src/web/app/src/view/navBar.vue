<template>
  <div class="navBar">
    <div class="header-section">
      <navBarTop></navBarTop>
    </div>
    <div class="main-content">
      <div class="left-side sticky-left-side">
        <navBarLeft></navBarLeft>
      </div>
      <div class="wrapper">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
  import navBarLeft from '../components/navBarLeft';
  import navBarTop from '../components/navBarTop'
  export default {
    name: 'navBar',
    components: {
      navBarTop,
      navBarLeft
    },
    data() {
      return {}
    },
    methods: {},
    mounted() {},
  }
</script>
<style scoped>
  .navBar {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 100%;
    /* display: flex; */
  }
  .navBar .left-side {
    top: 4rem;
    /* float:left; */
  }
  .navBar .sticky-left-side {
    /* position: fixed; */
    /* height: 100%; */
    /* z-index: 100; */
  }
  .left-side {
    width: 4.25rem;
    left: 0;
    overflow: hidden;
    outline: none;
    background: rgba(12, 17, 37, 0.4);
    /*flex-shrink: 0;*/
  }
  .navBar .main-content {
    flex: 1;
    /* padding-top: 4rem; */
  }
  .main-content {
    display: flex;
    /* float:right; */
    /* margin-left: 4.25rem; */
  }
  .navBar .header-section {
    /* position: fixed; */
    width: 100%;
    /* z-index: 100; */
    flex-shrink: 0;
  }
  .header-section {
    background: rgba(12, 17, 37, 0.4);
    height: 3.5rem;
  }
  .wrapper {
    padding: 0.5rem;
    width: 62.45rem;
    box-sizing: border-box;
    /*flex-grow: 1;*/
  }
</style>
