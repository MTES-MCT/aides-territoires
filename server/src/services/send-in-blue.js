/**
 * Instanciate send in blue APIs.
 * you MUST provide a SEND_IN_BLUE_API_KEY key as an environment variable
 */
var SibApiV3Sdk = require("sib-api-v3-sdk");

var defaultClient = SibApiV3Sdk.ApiClient.instance;

// Configure API key authorization: api-key
var apiKey = defaultClient.authentications["api-key"];
if (!process.env.SEND_IN_BLUE_API_KEY) {
  console.error(
    "You must set a SEND_IN_BLUE_API_KEY env variable with your send in blue Api Key to use sendInBlue.js ( see https://account.sendinblue.com/advanced/api )"
  );
}
apiKey.apiKey = process.env.SEND_IN_BLUE_API_KEY;

module.exports = SibApiV3Sdk;
