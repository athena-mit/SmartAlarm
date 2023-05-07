<template>
  <div class="alarmList">
    <div class="alarm" v-for="a in alarms" v-bind:style="{backgroundColor: getModeColor(a.mode)}">
        <span> {{ formatTime(a.time) }} </span>
      <span class="close" v-on:click="deleteAlarm(a.id)">x</span>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  export default {
    name: "alarmList",
    props: ["alarms"],
    methods: {
      getModeColor: function(mode) {
        if (mode == 'que_sera_sera'){
          return '#cce7ff';
        } else if (mode == 'basic'){
          return '#80c3ff';
        } else if (mode == 'passive_aggressive'){
          return '#ffd700';
        } else if (mode == 'at_all_costs'){
          return '#e60000';
        } return '#d3d3d3';
      },
      formatTime: function(time_string){
        const alarmTime = new Date(time_string + "-400")
        return alarmTime.toLocaleTimeString([], {timeStyle: 'short'})
      },
      deleteAlarm: function (alarm_id) {
        const path = `http://localhost:5001/alarm/${alarm_id}`
        axios.delete(path)
          .then(() => this.$emit("refreshAlarms"));
      }
    }
  }
</script>

<style>
.alarmList{
    display: flex;
    justify-content: center;
}
.alarm {
  border: 1px solid #ddd;
  background-color: #f6f6f6;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block;
  position: relative;
  margin: 5px;
}
.close {
  cursor: pointer;
  top: 50%;
  right: 0%;
  padding: 12px 16px;
  transform: translate(0%, -50%);
}
.close:hover {background: #bbb;}
</style>