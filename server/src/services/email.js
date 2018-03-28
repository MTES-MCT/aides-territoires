const sendInBlueClient = require("./send-in-blue-client");

module.exports.sendContactFormEmail = ({ from, text }) => {
  if (!process.env.CONTACT_FORM_TO) {
    console.log(
      "sendContactFormEmail : Le mail n'a pas été envoyé. La variable d'environnement CONTACT_FORM_TO doit être configurée avec l'adresse mail du destinataire"
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
  console.log(
    "ap/contactForm - sending email with following params : ",
    params
  );
  return api.sendTransacEmail(params);
};
