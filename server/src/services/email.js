const sendInBlueClient = require("./send-in-blue-client");
const User = require("../mongoose/User");

module.exports = {
  sendContactFormEmail,
  sendEmail
};

function sendContactFormEmail({ from, text }) {
  if (!process.env.CONTACT_FORM_TO) {
    console.log(
      "sendContactFormEmail : Le mail n'a pas pu être envoyé. La variable d'environnement CONTACT_FORM_TO doit être configurée avec l'adresse mail du destinataire"
    );
    return;
  }
  var api = new sendInBlueClient.SMTPApi();
  const params = {
    sender: {
      email: from
    },
    to: [{ email: process.env.CONTACT_FORM_TO }],
    htmlContent: text,
    subject: "Formulaire de contact de Aides-territoires"
  };
  return api.sendTransacEmail(params);
}

function sendEmail({ from, destinataires = [], text, subject }) {
  const to = destinataires.map(destinataire => {
    return { email: destinataire };
  });
  var api = new sendInBlueClient.SMTPApi();
  const params = {
    sender: {
      email: from
    },
    to: to,
    htmlContent: text,
    subject
  };
  return api.sendTransacEmail(params);
}
