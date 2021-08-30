<template>
  <div id="app">
    <h1>Weather Buddy</h1>
    <div id="query-input">
      How is weather in <input type="text" v-model="cityName" @change="searchCity"/> now?
    </div>
    <div v-if="currentEntry"  id="current-entry">
      <CityWeather :city="currentEntry.city" :temperature="currentEntry.temperature" :weather="currentEntry.weather"/>
    </div>
    <div v-if="entries.length > 0" id="entries-box">
      <h3>Latest Results</h3>
      <CityWeather v-for="entry in entries" :key="entry" :city="entry.city" :temperature="entry.temperature" :weather="entry.weather"/>
    </div>
  </div>
</template>

<script>
import CityWeather from "./components/CityWeather.vue";

export default {
  name: "App",
  components: {
    CityWeather,
  },
  data() {
    return {
      cityName: '',
      currentEntry: null,
      entries: [],
    }
  },
  methods: {
    getLatest() {
      this.axios
        .get(`http://${window.location.hostname}:5000/weather?max_entries=5`)
        .then((response) => {
          console.log(response)
          console.log(response.data)
          for( let entry of response.data ) {
            console.log( entry )
            this.entries.push( entry )
          }
        })
      console.log(this.entries)
    },
    searchCity() {
      this.entries = []
      // Fetch database
      this.axios
        .get(`http://${window.location.hostname}:5000/weather/${this.cityName}`)
        .then((response) => {
          console.log(response)
          this.currentEntry = response.data
        })
        .catch((error) => {
          console.log(error)
          this.currentEntry = null
        })
      this.getLatest()
    }
  },
  created() {
    this.getLatest()
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;  
}
#query-input {
  font-size: 30px;
}
input {
  font-size: 30px;
  width: 200px;
  border: 0;
  border-bottom: 2px solid black;
  text-align: center;
}
#current-entry {
  margin: 10px auto;
  margin-top: 50px;
  width: fit-content;
}
#entries-box {
  margin: 20px auto;
  padding: 10px;
  background: lightsteelblue;
  width: fit-content;
  border-radius: 5px;
}
</style>
