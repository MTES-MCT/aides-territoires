// next.config.js

// if there is a "env.config.js", load its config
var fs = require("fs");
let envConfig = {};
const fileName = `./env.${process.env.NODE_ENV}.config.js`;
if (fs.existsSync(fileName)) {
  envConfig = require(fileName);
}

module.exports = {
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
