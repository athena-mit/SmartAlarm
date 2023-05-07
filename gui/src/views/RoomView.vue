<template>
  <div v-bind:style="{backgroundColor:roomSettings.brightness}">
    <img src="../assets/bed.png">
  </div>
</template>

<script>
  export default {
    name: "roomView",
    props: ['roomSettings'],
    data() {
      return {
        lighting: [
          '#000000', '#4d4d00', '#999900', '#e6e600', '#ffff33'
        ],
        lightSetting: 0
      };
    },
    methods: {
      toggleLighting: function () {
        this.lightSetting = (this.lightSetting + 1) % this.lighting.length
      }
    }
  }
</script>

<style>
</style>