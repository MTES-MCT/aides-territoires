module.exports = {
  apps: [
    {
      name: "aides-territoires-server",
      script: "./src/index.js",
      env: {
        MONGODB_URL: "mongodb://localhost/aides-territoires",
        PORT: 8100,
        NODE_ENV: "development",
        SEND_IN_BLUE_API_KEY:
          "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",
        CONTACT_FORM_TO: "yann.boisselier@gmail.com"
      },
      env_production: {
        MONGODB_URL: "mongodb://localhost/aides-territoires",
        PORT: 8100,
        NODE_ENV: "production",
        SEND_IN_BLUE_API_KEY:
          "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",
        CONTACT_FORM_TO: "elise.marion@beta.gouv.fr"
      }
    }
  ]
};
