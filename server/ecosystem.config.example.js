module.exports = {
  apps: [
    {
      name: "aides-territoires-server",
      script: "./index.js",
      watch: true,
      env: {
        PORT: 8100,
        NODE_ENV: "production",
        SEND_IN_BLUE_API_KEY: "your-key",
        CONTACT_FORM_TO: "yann@yann.fr"
      }
    }
  ]
};
