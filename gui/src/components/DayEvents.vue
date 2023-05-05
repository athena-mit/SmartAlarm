<template>
  <div class="dayWindow">
    <div class="dayContent">
       <ul>
         <li v-for="e in events">
           {{formatEvent(e)}}
         </li>
       </ul>
       <p v-if="!events">Nothing Scheduled Yet!</p>
      <br><br>
      <button v-on:click="$emit('closeWindow')"> Back </button>
    </div>
  </div>
</template>

<script>
  export default {
    name: "DayEvents",
    props: ['events'],
    methods: {
      formatEvent: function(e){
        let tStart = new Date(e.start_time + "-400");
        let tEnd = new Date(e.end_time + "-400");
        let tInterval = tStart.toLocaleTimeString() + " - " + tEnd.toLocaleTimeString();
        let tWarn = new Date(e.warn_time + "-400")
        return tInterval + ": " + e.name + " (" + e.importance + ") - wake up by: " + tWarn.toLocaleTimeString();
      }
    }
  }
</script>

<style>
  .dayWindow {
    display: block; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    text-align: center;

  }

    /* Modal Content/Box */
  .dayContent{
    background-color: #fefefe;
    margin: 15% auto; /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: 50%; /* Could be more or less, depending on screen size */
  }
</style>