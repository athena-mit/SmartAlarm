<template>
  <div v-bind:style="{backgroundColor:brightness}">
    <img src="../assets/bed.png" alt="">
    <button v-on:click="resetSettings">Reset</button>
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
      getSettings: function () {
        axios.get(path)
        .then((res) => {
          this.brightness = res.data.brightness;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      resetSettings: function () {
        axios.post(path)
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