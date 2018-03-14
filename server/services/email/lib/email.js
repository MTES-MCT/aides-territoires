const nodemailer = require("nodemailer");

const config = require("../config");

module.exports.sendEmail = ({ from, to, subject, text }) => {
  const transporter = nodemailer.createTransport(config);
  const mailOptions = {
    from,
    to,
    subject,
    text
  };
  transporter.sendMail(mailOptions, function(error, info) {
    if (error) {
      return console.log(error);
    }
    console.log("Message sent: " + info.response);
  });
};
