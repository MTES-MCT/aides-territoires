require("dotenv").config({ silent: true });

const nconf = require("nconf");
nconf.overrides();

/**
 * Expose module.
 */

let envConfig;
try {
  envConfig = require("../../config/config." + process.env.NODE_ENV);
} catch (e) {
  envConfig = {};
}

module.exports = nconf
  .argv()
  .env("__")
  .add("configFileEnv", { type: "literal", store: envConfig })
  .add("configFile", {
    type: "literal",
    store: require("../../config/config")
  });
