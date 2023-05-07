<template>
  <div class="navbar">
    <h1>Smart Alarm</h1>
    <div class="pageNav">
      <router-link class="page" to="/">Alarms</router-link>
      <router-link class="page" to="/calendar">Calendar</router-link>
      <router-link class="page" to="/room">Room</router-link>
    </div>
</div>
</template>

<script>
  export default {
    name: "navigation"
  }
</script>

<style>
.navbar {
  background-color: lightblue;
  display: flex;
  justify-content: space-between;
  align-items: center;

}

.page {
  color: black;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
  border-radius: 12px;
  margin: 5px;
}

.page:hover {
  background-color: black;
  color: lightblue;
}
</style>