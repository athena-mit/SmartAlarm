<template>
  <div class="calendarView">
    <div class="month">
      <h1>{{currMonth}}</h1>
      <div class="week" v-for="w in numWeeks">
        <div class="day" v-for="d in weekDates(w)">
          <div v-if="d.getMonth() == firstDay.getMonth()" class="daySchedule" v-on:click="getEvents(d)">
            <h2>{{d.getMonth() + 1}}/{{d.getDate()}}</h2>
            <i>{{getNumEvents(d)}}</i>
          </div>
          <div v-else class="outsideMonth"></div>
        </div>
      </div>
    </div>
    <div class="addEvent">
      <p> Add Event: </p>
      <input type="text" v-model="newEvent.name">
      <div>
        <p>Importance: </p>
        <input v-model="newEvent.importance" type="radio" id="high" value="high">
          <label for="html">High</label><br>
        <input v-model="newEvent.importance" type="radio" id="med" value="medium">
          <label for="html">Medium</label><br>
        <input v-model="newEvent.importance" type="radio" id="low" value="low">
          <label for="html">Low</label><br>
      </div>
      <p>start at: </p>
      <input type="datetime-local" v-model="newEvent.start_time">
      <p>end at: </p>
      <input type="datetime-local" v-model="newEvent.end_time">
      <p>wake me up by: </p>
      <input type="datetime-local" v-model="newEvent.warn_time">
      <br><br>
      <button class="button" v-on:click="createEvent"> Create </button>
      <br><br>
    </div>
    <div v-if="showPopUp">
      <DayEvents :events="eventSched" @close-window="showPopUp=false"/>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  const path = 'http://localhost:5001/event'
  import DayEvents from "@/components/DayEvents.vue";
  export default {
    name: "calendarView",
      components: {DayEvents},
    data(){
      return {
        events: [],
        currMonth: 'May',
        firstDay: new Date('2023-05-01T00:00:00'),
        showPopUp: false,
        newEvent: {
            name: "",
            importance: "low",
            start_time: "",
            end_time: "",
            warn_time: "",
        },
        eventSched: []
      };
    },
    computed: {
      // firstDay: function() {return new Date(this.currMonth + ' 01, 2023');},
      numWeeks: function() {
        let numWeeks = 1;
        let nextWeek = new Date(this.firstDay);
        nextWeek.setDate(this.firstDay.getDate() + 7 + (0 - this.firstDay.getDay()));
        while (nextWeek.getMonth() == this.firstDay.getMonth()){
          numWeeks++;
          nextWeek.setDate(nextWeek.getDate() + 7)
        }
        return numWeeks;
      }
    },
    methods: {
      weekDates: function(weekNum) {
        const week = []
        const day = new Date(this.firstDay);
        day.setDate(day.getDate() + (weekNum-1)*7)
        for (let i = 0 - day.getDay(); i + day.getDay() < 7; i++){
          const weekDay = new Date(day)
          weekDay.setDate(day.getDate() + i)
          week.push(weekDay)
        }
        return week
      },
      getCalendarSummary: function (day){
        axios.get(path + `/summary/${day.toISOString().substring(0, 10)}`)
        .then((res) => {
          this.events = res.data.events;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getEvents: function (day){
        axios.get(path + `/${day.toISOString().substring(0, 10)}`)
        .then((res) => {
          this.eventSched = res.data.events;
          this.showPopUp = true;
        })
        .catch((error) => {
          console.error(error);
        });
      },
      getNumEvents: function (day){
        if (this.events && day.getMonth() == this.firstDay.getMonth()) {
          let numEvents = this.events[day.getDate() - 1];
          if (numEvents == 1){
            return numEvents + " event"
          } else if (numEvents > 0){
            return numEvents + " events"
          }
        }
        return

      },
      createEvent: function () {
        if (this.newEvent.name) {
          axios.post(path, {
            "action": "create",
            'name': this.newEvent.name,
            'importance': this.newEvent.importance,
            'start_time': this.newEvent.start_time,
            'end_time': this.newEvent.end_time,
            'warn_time': this.newEvent.warn_time
          }).then(() => {
              this.events = this.getCalendarSummary(this.firstDay);
              // this.newEvent= {
              //   name: "",
              //   importance: "",
              //   start_time: "",
              //   end_time: "",
              //   warn_time: "",
              // }
              }
          );
        }
      },
    },
    created: function () {
      this.getCalendarSummary(this.firstDay);
    }
  }
</script>

<style>
.calendarView{
  display: flex;
  justify-content: space-around;
}
.week{
  display: flex;
  align-items: center;
  flex-grow: 1;
}
.daySchedule, .outsideMonth {
  background-color: lightgray;
  flex-grow: 1;
  width: 100px;
  height: 100px;
  margin: 5px;
}

.outsideMonth {
  background-color: #e7e7e7;
}

.addEvent {
  display: flex;
  flex-direction: column;
}
</style>