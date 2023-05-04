<template>
  <div class="week">
    <div class="day" v-for="d in weekDates">
      <h2>{{d.getMonth() + 1}}/{{d.getDate()}}</h2>
    </div>
  </div>
</template>

<script>
  export default {
    name: "calendarView",
    computed: {
      weekDates: function () {
        const week = []
        const today = new Date();
        for (let i = 0 - today.getDay(); i + today.getDay() < 7; i++){
          const day = new Date(today)
          day.setDate(day.getDate() + i)
          week.push(day)
        }
        return week
      }
    },
    methods: {
      formatTime: function(time_string){
        const alarmTime = new Date(time_string + "-400");
        return alarmTime.getHours() + ":" + alarmTime.getMinutes();
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
.week{
  display: flex;
  justify-content: space-evenly;
}
</style>