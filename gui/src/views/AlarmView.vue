<template>
  <div class="container">
    <br><br><br>
    <h1> Time: {{dTimer}}</h1>
    <br><br>
    <div>
      <button class="button button3" v-on:click="silenceAlarm">Off</button>
      <button class="button button4" v-on:click="snoozeAlarm">Snooze</button>
    </div>
    <br><br>
    <div>
      <p> Add Alarm: </p>
      <input type="time" v-model="newAlarm">
      <button class="button" v-on:click="createAlarm"> Create </button>
    </div>
    <br><br>
    <AlarmList @refresh-alarms="getAlarms" :alarms="alarms"/>
  </div>
</template>

<script>
  import axios from "axios";
  import AlarmList from "@/components/AlarmList.vue";
  const path = 'http://localhost:5001/alarm'
  export default {
    name: "alarmView",
      components: {AlarmList},
    props: [],
    data(){
      return {
        newAlarm: "",
        dTimer: "",
        alarms: []
      };
    },
    methods: {
      startAlarm: function () {
        axios.post(path, {"action": "start"});
      },
      silenceAlarm: function () {
        axios.post(path, {"action": "silence"});
      },
      snoozeAlarm: function () {
        axios.post(path,
            {"action": "snooze"}
        ).then(() => this.getAlarms());
      },
      createAlarm: function () {
        if (this.newAlarm) {
          axios.post(path, {
            "action": "create",
            "time": this.newAlarm
          }).then(() => this.getAlarms());
          this.newAlarm = ""
        }
      },
      checkTime: function () {
        let thisView = this;
        setInterval(function () {
            let clock = new Date();
            thisView.dTimer = clock.toLocaleTimeString();
        }, 1000);
        setInterval(thisView.startAlarm, 10000);
      },
      getAlarms: function () {
        axios.get(path)
        .then((res) => {
          this.alarms = res.data.alarms;
        })
        .catch((error) => {
          console.error(error);
        });
      }
    },
    mounted: function() {
      this.checkTime();
    },
    created: function () {
      this.getAlarms();
    }
  }
</script>

<style>
.container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.button {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition-duration: 0.4s;
  cursor: pointer;
}

.button3 {
  background-color: white;
  color: black;
  border: 2px solid #f44336;
}

.button3:hover {
  background-color: #f44336;
  color: white;
}

.button4 {
  background-color: white;
  color: black;
  border: 2px solid #e7e7e7;
}

.button4:hover {background-color: #e7e7e7;}
</style>