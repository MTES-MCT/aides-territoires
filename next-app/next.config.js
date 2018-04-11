// next.config.js

// if there is a "env.config.js", load its config
var fs = require("fs");
const ecosystemConfig = require("./ecosystem.config");
const propertyName = `env_${process.env.NODE_ENV}`;
const env = ecosystemConfig.apps[0][propertyName];
console.log("==================");
console.log("current NODE_ENV : " + process.env.NODE_ENV);
console.log("Environment variables :");
console.log(JSON.stringify(env, null, 2));
console.log("=================");

module.exports = {
  publicRuntimeConfig: {
    // Will be available on both server and client
    ...env
  },
  exportPathMap: function(defaultPathMap) {
    return {
      "/": { page: "/" },
      "/a-propos": { page: "/a-propos" },
      "/porteurs-aides": { page: "/porteurs-aides" }
    };
  }
};
