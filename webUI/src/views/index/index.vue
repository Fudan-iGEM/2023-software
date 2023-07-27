<template>
  <div id="app">
    <div class="home">
        <vue-typed-js
          class="title"
          :strings="['rbs','igem']"
          :loop="true"
          :startDelay="300"
          :typeSpeed="100"
          :backSpeed="50"
          :showCursor="false"
        >
          <h1 class="typing"></h1>
        </vue-typed-js>
        <button class="btn-home" @click="toLogin()"><span>Try it now!</span></button>
        <div class="about">
          <span>About:<a href="https://2023.igem.wiki/fudan/software">iGEM 2023, Fudan Team</a></span>
          <br>
          <span><a href="https://gitlab.igem.org/mistyfield">@mistyfield</a></span>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "index",
  methods:{
    toLogin(){
        window.location.href = '/login';
    }
  },
}
</script>

<style scoped>
#app {
  font-family: HarmonyOS_Sans, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgba(0, 0, 0, .8);
  user-select: none;
}
.home{
  background-color: #fff5f0;
  padding: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
h1 {
  margin-top: 0;
  font-size: 5rem;
  font-weight: 700;
  background-image: linear-gradient(to right, #9795f0 0%, #fbc8d4 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.title {
   position: absolute;
}
.btn-home {
    margin-top: 10rem;
    background-color: #f0ecfc;
    background-image: linear-gradient(315deg, #9795f0 0%, #fbc8d4 100%);
    line-height: 42px;
    padding: 0;
    border: none;
    width: 8rem;
    color: #fff;
    border-radius: 5px;
    font-family: Barlow, Helvetica, Arial, sans-serif;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    display: inline-block;
    box-shadow:inset 2px 2px 2px 0px rgba(255,255,255,.5),
    7px 7px 20px 0px rgba(0,0,0,.1),
    4px 4px 5px 0px rgba(0,0,0,.1);
    outline: none;
}
.btn-home span {
    position: relative;
    display: block;
    width: 100%;
    height: 100%;
}
.btn-home:before,
.btn-home:after {
    position: absolute;
    content: "";
    right: 0;
    bottom: 0;
    background: #fbc8d4;
    /*box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
                -4px -4px 6px 0 rgba(116, 125, 136, .2),
      inset -4px -4px 6px 0 rgba(255,255,255,.5),
      inset 4px 4px 6px 0 rgba(116, 125, 136, .3);*/
    transition: all 0.3s ease;
}
.btn-home:before{
    height: 0%;
    width: 2px;
}
.btn-home:after {
    width: 0%;
    height: 2px;
}
.btn-home:hover:before {
    height: 100%;
}
.btn-home:hover:after {
    width: 100%;
}
.btn-home:hover{
    background: transparent;
}
.btn-home span:hover{
    color: #fbc8d4;
}
.btn-home span:before,
.btn-home span:after {
    position: absolute;
    content: "";
    left: 0;
    top: 0;
    background: #fbc8d4;
    /*box-shadow:  4px 4px 6px 0 rgba(255,255,255,.5),
                -4px -4px 6px 0 rgba(116, 125, 136, .2),
      inset -4px -4px 6px 0 rgba(255,255,255,.5),
      inset 4px 4px 6px 0 rgba(116, 125, 136, .3);*/
    transition: all 0.3s ease;
}
.btn-home span:before {
    width: 2px;
    height: 0%;
}
.btn-home span:after {
    height: 2px;
    width: 0%;
}
.btn-home span:hover:before {
    height: 100%;
}
.btn-home span:hover:after {
    width: 100%;
}
.about{
    position: absolute;
    bottom: 5rem;
}
.about span {
    font-weight: 700;
    font-size: 1rem;
}
.about a{
    color: rgba(0, 0, 0, .8);
}
</style>