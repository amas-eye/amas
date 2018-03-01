<template>
    <!--分页器-->
    <div class="pageIndicator">
        <div class="page">共{{pagecount}}页,当前为第{{ value }}页</div>
        <ul class="pageBtnBox">
            <li class="pageBtn" v-if="value>1" @click="pageClick(1)">首页</li>
            <li class="pageBtn" v-if="value>1" @click="pageClick(value-1)">上一页</li>
            <li class="pageBtn" v-if="value>1" @click="pageClick(value-1)" >{{value-1}}</li>
            <li class="pageBtn actvie" @click="pageClick(value)" >{{value}}</li>
            <li class="pageBtn" v-if="value<pagecount" @click="pageClick(value+1)" >{{value+1}}</li>
            <li class="pageBtn" v-if="value<pagecount-1" >...</li>
            <li class="pageBtn" v-if="value<pagecount" @click="pageClick(value+1)">下一页</li>
            <li class="pageBtn" v-if="value<pagecount" @click="pageClick(pagecount)">尾页</li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: 'pageIndicator',
        props: {
            value: { //分页器值 当前页号
                type: Number,
                default: 1
            },
            pagecount: { //总页数
                type: Number,
                default: 0
            }
        },
        data() {
            return {}
        },
        methods: {
            pageClick: function(index) { 

                this.$emit('update:value',index)
            },
        }
    }
</script>

<style scoped>
    .pageIndicator {
        margin-top: 1.5rem;
        font-size: 0.7rem;
    }
    .pageBtnBox {
        list-style-type: none;
        float: right;
        overflow: hidden;
        color: #f5f5f5;
    }
    .pageBtnBox li {
        float: left;
        background: rgba(12, 17, 37, 0.25);
        margin-left: 0.25rem;
        height: 1.15rem;
        line-height: 1.15rem;
        border-radius: 0.075rem;
        cursor: pointer;
    }
    .page {
        float: left;
        height: 1.15rem;
        line-height: 1.15rem;
        color: #3e3d44;
    }
    .pageBtn {
        padding: 0 0.65rem
    }
    .pageBtn.actvie {
        background: rgba(12, 17, 37, 0.5) !important;
    }
</style>
