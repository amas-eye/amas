<template>
  <!-- 监控总体 -->
  <div class="generalOverview">
    <div class="generalTop">
      <div class="generalSearch">
        <button>搜索指引</button>
      </div>
      <div class="searchText inputfontwhite phwhite">
        <input class="search" v-model="searchtext" type="text" placeholder="请输入视图名称">
        <el-select v-model="tagsle" class="searchClass" placeholder="请选择标签分类">
          <el-option :label="'不限'" :value="'all'">
          </el-option>
          <el-option v-for="item in tags" :key="item.tag" :label="item.tag" :value="item.tag">
          </el-option>
        </el-select>
      </div>
      <div class="searchBtn">
        <button class='clickable' type='button' @click="searchView();pageactive=1;">搜索</button>
      </div>
      <div class="addView">
        <button class='clickable' type='button' @click="editView();editTitle='新增视图';">添加视图</button>
      </div>
    </div>
    <div class="generalContent">
      <table border="0" cellspacing="0" cellpadding="0">
        <thead>
          <tr>
            <td>序号</td>
            <td>视图名称</td>
            <td>标签</td>
            <td>创建者</td>
            <td>创建时间</td>
            <td>操作</td>
          </tr>
        </thead>
        <tbody>
          <tr :key="item._id" v-for="(item,index) in List">
            <td>{{index+1}}</td>
            <!-- 跳转指定的进程视图 -->
            <td class='clickable viewname' @click="$router.push({ path: '/navBar/monitorView/', query: { viewid: item._id,name:item.name}})">{{item.name}}</td>
            <td>
              <span class="tag" :key="tag" v-for="tag in item.tags">
                                                    {{tag+' '}}
                                                </span>
            </td>
            <td>{{item.creater}}</td>
            <td>{{simdate.TMDTime(item.create_time)}}</td>
            <td class="operation">
              <a class='clickable' @click="editView(item,index);editTitle='编辑视图';" title="编辑"><i class="icon-edit"></i></a>
              <a class='clickable' @click="removeView(item._id)" title="删除"><i class="icon-delete"></i></a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <pageIndicator :value.sync="pageactive" :pagecount="pagecount"></pageIndicator>
    <!--新增，编辑视图,组件-->
    <div class="edit_box">
      <el-dialog :title="editTitle" :visible.sync="dialogEditVisible" size="tiny" :before-close="handleEditClose">
        <div class="edit_content">
          <div class="view_name clearfix">
            <p class="left_title fl">视图名称</p>
            <input class="fl" type="text" v-model="view_data.name" placeholder="请输入名称……">
          </div>
          <div class="tag_box clearfix">
            <p class="left_title fl">标签</p>
            <button class="fl clickable" @click="addTag()" title="添加"><i class="icon-plus"></i></button>
          </div>
          <ul>
            <li class="clearfix" :key="index" v-for="(val,index) in view_data.tags">
              <input type="text" v-model="view_data.tags[index]" class="fl" placeholder="请输入标签名">
              <button class="fl clickable" @click="delTag(index)" title="删除"><i class="icon-delete"></i></button>
            </li>
          </ul>
        </div>
        <div class="bottom_btnBox">
          <button v-if="editboxtype=='新增'" class="sureBtn clickable" @click="addView">确定</button>
          <button v-if="editboxtype=='编辑'" class="sureBtn clickable" @click="updateView">确定</button>
          <button class="cancleBtn clickable" @click="dialogEditVisible = false">取消</button>
        </div>
      </el-dialog>
    </div>
    <!--新增，编辑视图,组件-->
  </div>
</template>
<script>
  import http from 'service/myhttp'
  import urls from 'service/url'
  import pageIndicator from 'components/pageIndicator' //分页器
  import simdate from 'service/simdate'
  export default {
    name: 'generalOverview',
    components: {
      pageIndicator
    },
    data() {
      return {
        simdate: simdate,
        pageactive: 1, //当前页码
        viewcount: 0, // 视图总数
        onepagecount: 10, //一页显示个数
        editViewShow: false,
        editTitle: '', //编辑视图弹窗标题
        dialogEditVisible: false, //编辑视图显示隐藏
        tags: [], //所有标签数组
        searchtext: '', //搜索关键字
        tagsle: '', //tag选择刷选（搜索）
        editboxtype: '', //编辑框类型（新增/编辑）
        editViewId: '', //编辑视图id
        view_data: { //新增或编辑的视图数据
          name: '', //视图名称
          tags: [], //标签数组
          creater: 'admin', //创建者
        },
        List: [ //监控视图数组
          {
            name: '', //视图名称
            tags: [], //标签数组
            creater: 'admin', //创建者
            create_time: '' //创建时间
          }
        ]
      }
    },
    computed: {
      pagecount: function() {
        //页面总数 （每页10个）
        return parseInt(this.viewcount / this.onepagecount) + (parseInt(this.viewcount % this.onepagecount) > 0 ? 1 : 0)
      }
    },
    watch: {
      pageactive: function(val) {
        //页号发生变化
        this.initInfo()
      }
    },
    methods: {
      editView: function(item, index) {
        //新增，编辑视图
        // var _that=this;
        // _that.editViewShow=true;
        // this.dialogVisible = true;
        // console.log(item)
        if (item) { //编辑
          this.editboxtype = '编辑'
          const middleEditItem = JSON.parse(JSON.stringify(item));
          this.view_data.name = middleEditItem.name
          this.view_data.tags = middleEditItem.tags
          this.view_data.creater = middleEditItem.creater
          this.editViewId = middleEditItem._id
        } else { //新增
          this.editboxtype = '新增'
          this.view_data.name = ''
          this.view_data.tags = []
          this.view_data.creater = 'admin'
        }
        this.dialogEditVisible = true;
      },
      handleClose: function() {
        this.dialogVisible = false;
      },
      handleEditClose: function() {
        this.dialogEditVisible = false;
      },
      editViewOk: function() {
        var _that = this;
        _that.editViewShow = false;
      },
      editViewcancel: function() {
        var _that = this;
        _that.editViewShow = false;
      },
      addTag: function() {
        //添加标签数量
        this.view_data.tags.push('')
      },
      delTag: function(index) {
        //删除标签
        this.view_data.tags.splice(index, 1)
      },
      gettags: function() {
        //获取标签数组
        http.get(urls.HQBQSZ).then(res => {
          let data = res.data
          this.tags = data
        })
      },
      getViewcount: function() {
        //获取视图总数
        // console.log(this)
        http.get(urls.HQSTZS, {
          text: this.searchtext,
          tag: this.tagsle
        }).then(res => {
          // console.log(res)
          let data = res.data
          this.viewcount = data.count
        })
      },
      searchView: function() {
        //搜索监控视图
        // console.log(this)
        http.get(urls.CZJKST, {
          text: this.searchtext,
          tag: this.tagsle,
          page: this.pageactive,
          onepagecount: this.onepagecount
        }).then(res => {
          // console.log(res)
          let data = res.data
          this.List = data
        })
      },
      addView: function() {
        //添加监控视图
        // console.log(this)
        http.post(urls.XZJKST, this.view_data).then(res => {
          // console.log(res)
          this.dialogEditVisible = false
          this.initInfo()
          this.$message({
            showClose: true,
            message: '操作成功',
            type: 'success'
          })
        })
      },
      updateView: function() {
        //编辑更新视图
        http.post(urls.GXJKST, {
          id: this.editViewId,
          option: this.view_data //新数据
        }).then(res => {
          // console.log(res)
          this.dialogEditVisible = false
          this.initInfo()
           this.$message({
            showClose: true,
            message: '操作成功',
            type: 'success'
          })
        })
      },
      removeView: function(id) {
        //删除视图
        http.post(urls.SCJKST, {
          id: id,
        }).then(res => {
          // console.log(res)
          this.initInfo()
           this.$message({
            showClose: true,
            message: '操作成功',
            type: 'success'
          })
        })
      },
      initInfo: function() {
        //初始化数据
        this.gettags()
        this.getViewcount()
        this.searchView()
      }
    },
    mounted() {
      //挂载时
      this.initInfo()
    },
  }
</script>
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss" scoped>
  .search input::-webkit-input-placeholder,
  .searchClass input::-webkit-input-placeholder,
  {
    color: #c9e7ee;
    font-size: 0.9rem;
  }
  .generalSearch {
    float: left;
  }
  .generalSearch button {
    background: rgba(68, 67, 80, 0.6);
    width: 5rem;
    height: 1.5rem;
    border-radius: 0.3rem;
    line-height: 1.5rem;
    border-width: 0;
    font-size: 0.7rem;
    color: #fff;
    outline: none;
  }
  .searchText {
    float: left;
    width: 21.2rem;
    margin-left: 0.5rem;
    border-radius: 0.3rem;
    background: rgba(75, 77, 82, 0.31);
    height: 1.5rem;
    line-height: 1.1rem;
    padding: 0.2rem 0;
    box-sizing: border-box;
  }
  .searchText input {
    background: transparent;
    box-sizing: border-box;
    border-width: 0;
    outline: none;
    padding: 0 0.5rem;
    float: left;
    height: 100%;
    font-size: 0.7rem;
  }
  .search {
    width: 13.35rem;
    margin-left: -1px;
    border-right: 1px solid #84c7e2 !important;
  }
  .searchClass {
    width: 7.8rem
  }
  .searchBtn {
    float: left;
  }
  .searchBtn button {
    margin-left: 0.5rem;
    background: #57a0e8;
    width: 3.5rem;
    height: 1.5rem;
    border-radius: 0.3rem;
    line-height: 1.5rem;
    border-width: 0;
    font-size: 0.7rem;
    color: #fff;
    outline: none;
  }
  .addView {
    float: right;
  }
  .addView button {
    background: #53c1b9;
    width: 5rem;
    height: 1.5rem;
    border-radius: 0.3rem;
    line-height: 1.5rem;
    border-width: 0;
    font-size: 0.7rem;
    color: #fff;
    outline: none;
  }
  .generalContent {
    width: 61.5rem;
    height: 21.35rem;
    background: rgba(12, 17, 37, 0.25);
    clear: both;
    border-radius: 0.3rem;
    padding: 0 1rem 1rem 1rem;
    box-sizing: border-box;
  }
  .generalContent table {
    width: 100%;
  }
  .generalContent table .operation a {
    display: inline-block;
    height: 100%;
  }
  .generalContent table .operation i {
    color: #66a5ef;
  }
  .generalContent table .operation a:nth-child(1) {
    text-align: right;
  }
  .generalContent table .operation a:nth-child(2) {
    text-align: left;
  }
  .viewname {
    color: RGB(102, 168, 239) !important;
  }
  .icon-prepared {
    margin-right: 0.15rem;
  }
  .icon-delete {
    margin-left: 0.15rem;
  }
  .generalTop {
    margin-bottom: 0.5rem;
    overflow: hidden;
  }
  .generalContent table thead td {
    height: 1.75rem;
    line-height: 1.75rem;
    font-size: 0.75rem;
    color: #fff;
  }
  .generalContent table tbody td {
    height: 1.9rem;
    line-height: 1.9rem;
    font-size: 0.65rem; // font-weight: lighter;
    color: #fff;
  }
  .generalContent table tbody tr:nth-child(odd) {
    background: #526f8a;
  }
  .generalContent table tbody tr:nth-child(odd) td {
    border-top: 1px solid #3d556c;
    border-bottom: 1px solid #3d556c;
  }
  /*视图组件*/
  .addViewMask,
  .editViewMask {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    z-index: 1000000;
  }
  .editView {
    background: #000;
    width: 27rem;
    padding: 0 2.5rem;
    height: 16.75rem;
    border-radius: 0.3rem;
    margin: 0 auto;
    position: relative;
    box-sizing: border-box;
    top: 50%;
    transform: translateY(-50%);
  }
  .MaskBtn {
    width: 5.8rem;
    height: 2rem;
    border-radius: 0.3rem;
    line-height: 2rem;
    border-width: 0;
    font-size: 0.45rem;
    color: #fff;
    outline: none;
    margin-top: 2.5rem;
  }
  .editViewOk {
    margin-right: 0.95rem;
    border: 1px solid #000;
    background: #57a0e8;
  }
  .editViewcancel {
    margin-left: 0.95rem;
    border: 1px solid #57a0e8;
    background: transparent;
  }
  .viewTitle {
    font-size: 1rem;
    color: #fff;
    padding: 1.6rem 0;
    text-align: center;
  }
  .viewNameText {
    width: 16.35rem;
    margin-left: 0.5rem;
    display: inline-block;
    line-height: 1.7rem;
    outline: none;
    color: #0da2c3;
    float: left;
    background: rgb(31, 38, 51);
    border: 0;
    font-size: 0.8rem;
    padding-left: 0.5rem;
    box-sizing: border-box;
  }
  .addViewText,
  .addViewLabeled span {
    display: inline-block;
    float: left;
    margin-left: 0.25rem;
    background: rgb(31, 38, 51);
    line-height: 1.7rem;
    width: 1.8rem;
  }
  .editViewMask .viewName {
    width: 5.4rem;
    display: inline-block;
    line-height: 1.7rem;
    text-align: center;
    color: #0da2c3;
    font-size: 0.8rem;
    float: left;
    background: rgb(31, 38, 51);
  }
  .editViewMask span {
    display: inline-block;
    height: 1.7rem;
  }
  .viewNameMask {
    text-align: left;
    overflow: hidden;
  }
  .addViewLabel,
  .addViewLabeled {
    margin-top: 0.25rem;
    overflow: hidden;
  }
  .addViewLabeled {
    margin-left: 5.65rem;
    text-align: left;
  }
  .addViewLabeled span {
    text-align: center;
  }
  .addViewLabeled span i {
    font-size: 0.8rem;
  }
  .addViewLabeled input {
    width: 14.25rem;
    line-height: 1.7rem;
    color: #0da2c3;
    font-size: 0.8rem;
    border-width: 0;
    outline: none;
    float: left;
    padding-left: 0.5rem;
    box-sizing: border-box;
    background: rgb(31, 38, 51);
  }
  .addViewLabeled .icon-delete {
    height: 1.7rem;
    line-height: 1.7rem;
    margin: 0;
    color: #fff;
  }
</style>
