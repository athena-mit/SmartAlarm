<template>
  <div class="alarmList">
    <div class="alarm" v-for="a in alarms">
        <span> {{ a.time }} </span>
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
  margin-top: -1px; /* Prevent double borders */
  background-color: #f6f6f6;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: block;
  position: relative;
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