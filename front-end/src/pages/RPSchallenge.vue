<template>
  <div id="RPSchallenge">
    <div class="container" v-if="!logged">
      <h1>{{formText}}</h1>
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
      <a @click="changeForm()" style="color: blue;text-decoration: underline blue; cursor: pointer;">{{formButton}}</a>
    </div>

  
    <div class="container" v-if="logged">
      <h1>Rock-Paper-Scissors</h1>
      <p style="color: blue">Rock beats scissors, scissors beat paper, paper beats rock.</p>

      <div class="instructions" v-if="!inGame && !gameEnd && !leaderboard">
        <br>
        <p style="margin-top: -15px;">Race to 5 wins. Bonus points for fewer matches to reach 5</p>
        <p style="margin-top: -15px;">wins using the formula 10 - # of matches. If computer gets 5</p>
        <p style="margin-top: -15px;">wins first, you get zero points.</p>
        <br><br>
        <p style="font-size: 22px;">Good luck, {{username}}</p>
        <button @click="startGame()" class="btn btn-primary" style="background-color: green;">Start Game</button>
      </div>

      <div class="game" v-if="inGame">
        <h2 v-if="!gameEnd && !leaderboard">Round #{{game_round}}</h2>
        <p style="font-size: 25px;" v-if="!gameEnd && !leaderboard">Computer {{machineScores}} - {{scores}} {{username}}</p>
        <div v-if="playable && !leaderboard">
          <p>Computer picks</p>
          <p v-if="machineChoice == '?'"><img src="@/assets/qmark.jpeg"/></p>
          <p v-if="machineChoice == 'rock'"><img src="@/assets/rock.jpeg"/></p>
          <p v-if="machineChoice == 'paper'"><img src="@/assets/paper.jpeg"/></p>
          <p v-if="machineChoice == 'scissors'"><img src="@/assets/scissors.jpeg"/></p>
          <p>Pick your weapon</p>
          <img @click="gameCheck('rock')" src="@/assets/rock.jpeg"/>
          <img @click="gameCheck('paper')" src="@/assets/paper.jpeg"/>
          <img @click="gameCheck('scissors')" src="@/assets/scissors.jpeg"/>
        </div>

        <div v-if="!playable && !gameEnd">
          <h3>{{roundResult}}</h3>
          <button @click="continueGame()" class="btn btn-primary" style="background-color: green;">Ok</button>
        </div>

        <div v-if="gameEnd">
          <div v-for="line in finalResult" v-bind:key="line">
            <p>{{line}}</p>
          </div>
          <button @click="startGame()" class="btn btn-primary" style="background-color: green;">Start New Game</button>
          <button @click="goLeaderboard()" class="btn btn-primary" style="background-color: green;">Leaderboard</button>
          <button @click="logout()" class="btn btn-primary">Logout</button>
        </div>
      
        <div class="game" v-if="leaderboard">
          <h2>Leaderboard</h2>
          <p>Only players with minimum of 10 games played are listed here</p>

          <table class="table table-striped">
            <thead>
              <tr>
                <th>Player</th>
                <th>Points</th>
                <th>Games Played</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user,i) in leaderboardlist" :key="i">
                <td>{{ user.username }}</td> 
                <td>{{ user.scores }}</td>
                <td>{{ user.matches }}</td>
              </tr>
            </tbody>
          </table>

          <button @click="startGame()" class="btn btn-primary" style="background-color: green;">Start New Game</button>
          <button @click="logout()" class="btn btn-primary">Logout</button>
        </div>


      </div>
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
      formText: "Log-in",
      inGame: false,
      machineChoice: "?",
      roundResult: "",
      playable: true,
      gameEnd: false,
      finalResult: "",
      leaderboard: false,
      leaderboardlist: []
    }
  },
  methods: {
    goLeaderboard() {
      this.finalResult = "";
      this.roundResult = "";
      this.playable = true;
      this.inGame = true;
      this.gameEnd = false;
      this.leaderboard = true;
      axios.get(`${process.env.VUE_APP_BACK_URL}/leaderboard`)
      .then(response => {
        console.log(response.data);
        this.leaderboardlist = response.data;
      })
      .catch(error => {
        console.log(error);
      });
    },
    continueGame() {
      this.playable = true;
    },
    startGame() {
      this.inGame = true;
      this.gameEnd = false;
      this.finalResult = "";
      this.roundResult = "";
      this.playable = true;
      this.leaderboard = false;
    },
    logout() {
      this.logged = false;
      this.username = "";
      this.password = "";
      this.repitPassword = "";
      this.scores = 0;
      this.machineScores = 0;
      this.game_round = 1;
      localStorage.removeItem('user');
      localStorage.removeItem('password');
      localStorage.removeItem('username');
    },
    changeForm() {
      this.signup = !this.signup;
      this.formText = this.signup ? "Sign up" : "Log-in";
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
          //console.log(response);
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
          //console.log(response);
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
        //console.log(response.data);
        if (response.data.result.includes("5")) {
          this.gameEnd = true;
          this.finalResult = response.data.result.split("\n");
        }
        this.machineChoice = response.data.machine_choice;
        this.game_round = response.data.game_round;
        this.scores = response.data.user_scores;
        this.machineScores = response.data.machine_scores;
        this.roundResult = response.data.result;
        this.playable = false;
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
  margin-top: 2%;
  text-align: center;
}
img {
  width: 5%;
}
</style>