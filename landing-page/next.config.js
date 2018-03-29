// next.config.js

// if there is a "env.config.js", load its config
var fs = require("fs");
let envConfig = {};
if (fs.existsSync("./env.config.js")) {
  envConfig = require("./env.config.js");
}

module.exports = {
  distDir: "build",
  publicRuntimeConfig: {
    // Will be available on both server and client
    ...envConfig
  },
  exportPathMap: function() {
    return {
      "/": { page: "/" },
      "/porteur-aide": { page: "/porteur-aide" }
    };
  }
};
