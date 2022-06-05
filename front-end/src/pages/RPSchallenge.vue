<template>
  <div id="RPSchallenge">
    <div class="container" v-if="!logged">
      <div class="form-group">
        <label for="InputEmail">Username</label>
        <input class="form-control" v-model="username" type="email" placeholder="Email" />
      </div>
      <div class="form-group">
        <label for="InputPassword">Password</label>
        <input class="form-control" v-model="password" type="password" placeholder="Password" />
      </div>
      <div class="form-group" v-if="signup">
        <label for="InputPassword">Repit Password</label>
        <input class="form-control" v-model="repitPassword" type="password" placeholder="Repit Password" />
      </div>
      <button v-if="!signup" @click="login()" type="submit" class="btn btn-primary">Submit</button>
      <button v-if="signup" @click="signUp()" type="submit" class="btn btn-primary">Submit</button>
      <br> <br>
      <a @click="changeForm()">{{formButton}}</a>
    </div>


    <div class="container" v-if="logged">
      <button @click="gameCheck('rock')">Rock</button>
      <button @click="gameCheck('paper')">Paper</button>
      <button @click="gameCheck('scissors')">Scissors</button>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
//import axios from 'axios';

export default {
  data() {
    return {
      choices: ['rock', 'paper', 'scissors'],
      username: "",
      scores: 0,
      machineScores: 0,
      userChoice: 0,
      game_round: 1,
      password: "",
      repitPassword: "",
      logged: false,
      signup: false,
      formButton: "Sign up",
    }
  },
  methods: {
    changeForm() {
      this.signup = !this.signup;
      this.formButton = this.signup ? "Log in" : "Sign up";
    },
    signUp() {
      axios.post(`${process.env.VUE_APP_BACK_URL}/signup`, 
        {
          "username": this.username,
          "password": this.password,
          "repit_password": this.repitPassword
        }, 
        {
          headers: {
              "Content-Type": "application/JSON",
              "Access-Control-Allow-Origin": "*"
          }
        }).then(response => {
          if (response.data.response == "User created successfully") {
            this.signup = !this.signup;
          }
          console.log(response);
        }).catch(error => {
          console.log(error);
        });
    },
    login() {
      if (localStorage.username && localStorage.password) {
        this.username = localStorage.username;
        this.password = localStorage.password;
      }

      if (this.username != "" && this.password != "") {
        axios.post(`${process.env.VUE_APP_BACK_URL}/login`, 
        {
          "username": this.username,
          "password": this.password}, 
        {
          headers: {
              "Content-Type": "application/JSON",
              "Access-Control-Allow-Origin": "*"
          }
        }).then(response => {
          if (response.data.response == "Login successful") {
            this.logged = true;
            localStorage.username = this.username;
            localStorage.password = this.password;
          }
          console.log(response);
        }).catch(error => {
          console.log(error);
        });
      }
    },
    gameCheck(userChoice) {
      this.userChoice = userChoice;
      axios.post(`${process.env.VUE_APP_BACK_URL}/game`, {
        "username": this.username,
        "machine_scores": this.machineScores,
        "user_scores": this.scores,
        "user_choice": this.userChoice,
        "game_round": this.game_round
      })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log(error);
      });
    },
  },
  mounted() {
    this.login();
  },
};
</script>

<style>
.container {
  margin-top: 200px;
  text-align: center;
}
</style>