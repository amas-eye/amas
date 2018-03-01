<!--地图组件-->
<template>
<div v-bind:style="mapStyle" class="Bmap">
  <!--<div id="allmap" style="width: 100%; height: {{mapHeight}}px"></div>-->
  <!--<div id="allmap":style="{width: '100%', height: mapHeight + 'px'}"></div>-->
  <div id="allmap" v-bind:style="mapStyle"></div>
</div>
</template>
<script>
export default {
  name: 'Bmap',
  data: function() {
    return {
      // map:null,
      heatmap:null,
      mapStyle: {
        width: '100%',
        height: '100%'
      }
    }
  },
  props: {
    // 地图在该视图上的高度
    location:{
      type: Array,
      default:function(){
        return []
      }
    },
    Points: {
      type: Array,
      default: function() {
        return [{
          "lat": 1.253823,
          "count": 445,
          "lng": 103.822153
        }, {
          "lat": 1.253195,
          "count": 438,
          "lng": 103.825276
        }, {
          "lat": 1.255713,
          "count": 456,
          "lng": 103.823083
        }, {
          "lat": 1.258609,
          "count": 1486,
          "lng": 103.819423
        }, {
          "lat": 1.253336,
          "count": 393,
          "lng": 103.818853
        }, {
          "lat": 1.251313,
          "count": 409,
          "lng": 103.817089
        }, {
          "lat": 1.255364,
          "count": 335,
          "lng": 103.812566
        }]
      }
    }
  },
  methods:{
    mapload:function(location){
      //地图初始化
       console.log(location)
       let map = new BMap.Map("allmap",{minZoom:16,maxZoom:18}); //生成地图实例
      let point = new BMap.Point(location[0], location[1]);
      let mapStyle = {
        //features: ["road", "building", "water", "land"], //隐藏地图上的poi
        // style: "dark" //设置地图风格为高端黑
      }
      map.setMapStyle(mapStyle);

      //var marker = new BMap.Marker(point);
      //map.addOverlay(marker);
      map.centerAndZoom(point, 16);
      // 信息窗的配置信息
      // var opts = {
      //   width: 250,
      //   height: 75,
      //   title: "地址：",
      // }
      /*
      var infoWindow = new BMap.InfoWindow(this.description, opts); // 创建信息窗口对象
      marker.addEventListener("click", function() {
        map.openInfoWindow(infoWindow, point);
      });
      */

      map.enableScrollWheelZoom(true);
      let heatmapOverlay = new BMapLib.HeatmapOverlay({
        "radius": 50
      }); //热点图控制器
      this.heatmap=heatmapOverlay
      map.addOverlay(heatmapOverlay);


    },

    hotinfoload:function(val){
      //地图热力数据加载

      console.log(this.heatmap)
      
      this.heatmap.setDataSet({
        data: this.Points,
        max: 2000
      });
      this.heatmap.show();
    }
  },
  watch: {
    location:function(val){
      //监听地点变化
      this.mapload(val)
    },
    Points: function(val) {
      //监听接口热点的变化从新设热点
      this.hotinfoload(val)

    }
  },
  mounted: function() {


  }
}
</script>
<!--Add"scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
