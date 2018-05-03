/**
 * Just a hack to serve our app from zeit now hosting
 * withour a basic http auth protected access :
 * if there is package.json, zeit now considers this is a node app
 * and launch this tiny express server instead of directly serving static files
 */
const express = require("express");
const basicAuth = require("express-basic-auth");
const fs = require("fs");
const passport = require("passport");
const Strategy = require("passport-http").BasicStrategy;

passport.use(
  new Strategy((username, password, cb) => {
    if (username === "aides-territoires" && password === "yagupocuni827215") {
      return cb(null, "Worked");
    } else {
      return cb(null, false);
    }
  })
);

const app = express();
app.use(passport.authenticate("basic", { session: false }));

app.get("/", function(request, reponse) {
  reponse.sendFile(__dirname + "/index.html");
  app.use("/static", express.static("static"));
});
app.get("/admin", function(request, reponse) {
  reponse.sendFile(__dirname + "/index.html");
  app.use("/static", express.static("static"));
});
app.listen(3000);
console.log("app listening on port 3000");
