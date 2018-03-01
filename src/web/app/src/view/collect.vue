<template>
    <!-- 采集 -->
    <div class="collect">
        <div class="generalTop">
            <div class="generalSearch">
                <button>搜索指引</button>
            </div>
            <div class="searchText inputfontwhite phwhite">
                <input class="search" v-model="searchtext" type="text" placeholder="请输入搜索文本">
                <el-select v-model="tagsle" class="searchClass" placeholder="请选择标签分类">
                    <el-option :label="'不限'" :value="'all'">
                    </el-option>
                    <el-option v-for="item in tags" :key="item.tag" :label="item.tag" :value="item.tag">
                    </el-option>
                </el-select>
            </div>
            <div class="searchBtn">
                <button class='clickable' type='button' @click="searchData();pageactive=1;">搜索</button>
            </div>
            <!-- <div class="addView">
                                <button class='clickable' type='button' @click="editView();editTitle='批量添加标签分类';">批量添加标签分类</button>
                            </div> -->
            <div class="addView">
                <button class='clickable' type='button' @click="updateData">保存</button>
            </div>
        </div>
        <div class="generalContent">
            <table border="0" cellspacing="0" cellpadding="0">
                <thead>
                    <tr>
                        <td class=" clickable">
                            <label class="clickable" style="display:block;width:100%;">
                                 <!-- <input class="check clickable" type="checkbox" /> -->
                                 序号
                                 </label>
                        </td>
                        <td>指标</td>
                        <td>说明</td>
                        <!-- <td>标签分类</td> -->
                        <td>更新时间</td>
                    </tr>
                </thead>
                <tbody>
                    <tr :key="item._id" v-for="(item,index) in List">
                        <td class=" clickable">
                            <label class="clickable" style="display:block;width:100%;">
                                     <!-- <input class="check clickable" type="checkbox" /> -->
                                     {{index+1}} 
                                </label>
                        </td>
                        <td>{{item.metric_name}}</td>
                        <td class="phwhite"><input class="text" type="text" placeholder="请输入说明..." v-model="item.description" :value="item.description" /></td>
                        <!-- <td>
                                            <span class="tag" v-for="tag in item.tags">
                                                                                                      {{tag+' '}}
                                                                                                  </span>
                                        </td> -->
                        <td>{{ item.last_update>0?(simdate.SJCtoTime(item.last_update)):'无更新'}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <pageIndicator :value.sync="pageactive" :pagecount="pagecount"></pageIndicator>
        <!--批量添加标签分类-->
        <div class="edit_box">
            <el-dialog :title="editTitle" :visible.sync="dialogEditVisible" size="tiny" :before-close="handleEditClose">
                <div class="edit_content">
                    <div class="view_name clearfix">
                        <div class="formtext">
                            <input type="text" v-model="newTagName" placeholder="请输入名称……">
                            <div class="signtext">
                                <span class="formsign">*</span>请选择要批量添加的行
                            </div>
                        </div>
                    </div>
                </div>
                <div class="bottom_btnBox">
                    <!-- <button class="sureBtn clickable" @click="bulkaddtag">确定</button> -->
                    <button class="cancleBtn clickable" @click="dialogEditVisible = false">取消</button>
                </div>
            </el-dialog>
        </div>
        <!--批量添加标签分类-->
    </div>
</template>
<script>
    import http from 'service/myhttp'
    import urls from 'service/url'
    import pageIndicator from 'components/pageIndicator' //分页器
    import simdate from 'service/simdate'
    export default {
        name: 'collect', //采集
        components: {
            pageIndicator
        },
        data() {
            return {
                simdate: simdate,
                pageactive: 1, //当前页码
                itemcount: 0, // 数据总数
                onepagecount: 10, //一页显示个数
                editTitle: '', //编辑视图弹窗标题
                dialogEditVisible: false, //编辑视图显示隐藏
                tags: [], //所有标签数组
                searchtext: '', //搜索关键字
                tagsle: '', //tag选择刷选（搜索）
                editboxtype: '', //编辑框类型（新增/编辑）
                newTagName: '', //新增标签tag名 
                List: [ //表格列表数据数组
                    {
                        description: '',
                        last_update: -1,
                        metric_name: '',
                        tags: []
                    }
                ]
            }
        },
        computed: {
            pagecount: function() {
                //页面总数 （每页10个）
                return parseInt(this.itemcount / this.onepagecount) + (parseInt(this.itemcount % this.onepagecount) > 0 ? 1 : 0)
            }
        },
        watch: {
            pageactive: function(val) {
                //页号发生变化
                this.initInfo()
            }
        },
        methods: {
            editView: function() {
                //新增，编辑视图
                this.dialogEditVisible = true;
            },
            handleClose: function() {
                this.dialogVisible = false;
            },
            handleEditClose: function() {
                this.dialogEditVisible = false;
            },
            gettags: function() {
                //获取标签数组
                // http.get(urls.HQBQSZ).then(res => {
                //     let data = res.data
                //     this.tags = data
                // })
            },
            // getitemcount: function() {
            //     //获取数据总数
            //     console.log(this)
            //     http.get(urls.HQCJXX).then(res => {
            //         console.log(res)
            //         this.itemcount = res.total
            //         let data = res.data
            //         // this.itemcount = data.count
            //     })
            // },
            searchData: function() {
                //搜索采集数据
                // console.log(this)
                // let url
                // if(this.searchtext==''){
                //     url=urls.HQCJXX
                // }
                // else{
                //     url=urls.HQCJXX+'/'+this.searchtext
                // }
                http.get(urls.HQCJXX, {
                    search: this.searchtext || '',
                    limit: this.onepagecount,
                    offset: (this.pageactive - 1) * this.onepagecount,
                }).then(res => {
                    // console.log(res)
                    let data = res.data.data
                    this.itemcount = res.data.total
                    this.List = data
                })
            },
            updateData: function() {
                //更新采集用户配置数据
                // console.log(this)
                http.post(urls.GXCJXX,
                    this.List
                ).then(res => {
                    // console.log(res)
                    this.$message({
                        showClose: true,
                        message: '操作成功',
                        type: 'success'
                    })
                })
            },
            // bulkaddtag: function() {
            //     //批量添加tag
            // },
            initInfo: function() {
                //初始化数据
                this.gettags()
                // this.getitemcount()
                this.searchData()
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
    .collect {}
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
        width: 3rem;
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
    .generalContent table .index {
        text-align: left;
        min-width: 0.5rem;
        max-width: 1.8rem;
    }
    .generalContent table input[type="checkbox"] {
        vertical-align: middle;
        width: 0.8rem;
        height: 0.8rem;
        margin-right: 0.8rem;
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
        padding: 0rem 0.5rem;
    }
    .generalContent table tbody td {
        height: 1.9rem;
        line-height: 1.9rem;
        font-size: 0.65rem; // font-weight: lighter;
        color: #fff;
        padding: 0rem 0.5rem;
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
    /*批量添加标签分类*/
    .collect .formtext {
        width: 17rem;
        margin: auto;
        text-align: left;
    }
    .collect .formtext input[type="text"] {
        width: 100% !important;
    }
    .collect .signtext {
        margin-top: 0.5rem;
        font-size: 0.7rem;
    }
    .formsign {
        color: RGB(169, 61, 63);
        font-size: 1.8rem;
        vertical-align: middle;
        position: relative;
        top: 0.36rem;
        margin-right: 0.5rem;
    }
    /*-----*/
    .collect .generalContent table .text {
        width: 10rem;
        padding: 0.2rem 0.4rem;
        border: 0.05rem solid #fff;
        background-color: transparent;
        color: #fff;
        border-radius: 0.2rem;
    }
</style>
