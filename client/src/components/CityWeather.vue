<template>
  <div>
    <h3>{{ city }}</h3>
    <h1>{{ temperature-273 }}°C</h1>
    <h3>{{ weather }}</h3>
  </div>
</template>

<script>
export default {
  name: "CityWeather",
  props: {
    city: String,
    temperature: Number,
    weather: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
div {
  border-bottom: 1px solid black;
  background: lightgrey;
  margin: 5px;
  width: 150px;
  text-align: center;
  border-radius: 5px;
  display: inline-block;
}
h3 {
  margin: 10px;
}
</style>
