module.exports = {
  apps: [
    {
      name: "aides-territoires-landing-page",
      script: "./server.js",
      instances: 0,
      exec_mode: "cluster",
      env: {
        PORT: 3000,
        NODE_ENV: "development"
      },
      env_production: {
        PORT: 3000,
        NODE_ENV: "production"
      }
    }
  ]
};
