// next.config.js

// if there is a "env.config.js", load its config
var fs = require("fs");
let envConfig = {};
const fileName = `./env.config.js`;
if (fs.existsSync(fileName)) {
  envConfig = require(fileName);
}
console.log("evn", envConfig);

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
