// ! config for pm2 node process manager
module.exports = {
  apps: [
    {
      name: "aides-territoires-server",
      script: "./src/index.js"
    }
  ]
};
