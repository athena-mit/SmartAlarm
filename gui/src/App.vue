<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navigation from "@/components/Navigation.vue";
</script>

<template>
  <Navigation />
  <RouterView :roomSettings="roomSettings"/>
</template>

<script>
import axios from "axios";
export default{
  name: "app",
  data(){
    return {
      roomSettings: {
        brightness: '#000000'
      }
    };
  }
  // methods: {
  //   getRoomSettings: function () {
  //     axios.get(path + "/room")
  //       .then((res) => {
  //         this.roomSettings.brightness = res.data.brightness
  //       })
  //       .catch((error) => {
  //         console.error(error);
  //       });
  //   }
  // },
  // created: function () {
  //     this.getRoomSettings()
  //   }
}
</script>

<style scoped>
@media (min-width: 1024px) {
}
</style>
