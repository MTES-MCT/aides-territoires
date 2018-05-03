// this file is for pm2 package
module.exports = {
  apps: [
    {
      name: "aides-territoires-server",
      script: "./src/index.js",
      instances: 0,
      exec_mode: "cluster"
    }
  ]
};
