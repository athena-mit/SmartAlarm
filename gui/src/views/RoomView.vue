<template>
  <div v-bind:style="{backgroundColor:brightness}">
    <img src="../assets/bed.png">
  </div>
</template>

<script>
  import axios from "axios";
  const path = 'http://localhost:5001/room';
  export default {
    name: "roomView",
    data() {
      return {
        brightness: "#000000"
      };
    },
    methods: {
      toggleLighting: function () {
        this.lightSetting = (this.lightSetting + 1) % this.lighting.length
      },
      getSettings: function () {
        axios.get(path)
        .then((res) => {
          this.brightness = res.data.brightness;
        })
        .catch((error) => {
          console.error(error);
        });
      }
    },
    created: function (){
      this.getSettings()
    }
  }
</script>

<style>
</style>