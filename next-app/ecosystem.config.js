/**
 * La configuration de pm2, qui gére le process du serveur node
 */
module.exports = {
  apps: [
    {
      name: "aides-territoires-next-app",
      script: "./index.js",
      instances: 0,
      exec_mode: "cluster",
      env_development: {
        PORT: 3000,
        NODE_ENV: "development",
        GRAPHQL_URL: "http://localhost:8100/graphql",
        GRAPHCMS_API_URL:
          "https://api.graphcms.com/simple/v1/cjfdxg4vd5bmo0176upepcub5"
      },
      env_production: {
        PORT: 3000,
        NODE_ENV: "production",
        API_GRAPHQL_ENDPOINT:
          "http://api.aides-territoires.beta.gouv.fr/graphql",
        GRAPHCMS_GRAPHQL_ENDPOINT:
          "https://api.graphcms.com/simple/v1/cjfdxg4vd5bmo0176upepcub5"
      }
    }
  ]
};
