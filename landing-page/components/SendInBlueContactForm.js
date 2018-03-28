import React from "react";
import { request } from "graphql-request";
import getConfig from "next/config";
const { publicRuntimeConfig } = getConfig();

const EMAIL_SENDING_STATUS_NOT_STARTED = "not_started";
const EMAIL_SENDING_STATUS_PENDING = "pending";
const EMAIL_SENDING_STATUS_SENT = "sent";
const EMAIL_SENDING_STATUS_ERROR = "error";

export default class ContactForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      message: "",
      emailSendingStatus: EMAIL_SENDING_STATUS_NOT_STARTED
    };
  }
  handleSubmit = event => {
    event.preventDefault();
    this.setState({
      emailSendingStatus: EMAIL_SENDING_STATUS_PENDING
    });
    this.sendEmail()
      .then(r => {
        this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_SENT
        });
      })
      .catch(e => {
        this.setState({
          emailSendingStatus: EMAIL_SENDING_STATUS_ERROR
        });
      });
  };
  onEmailChange = event => {
    this.setState({ email: event.target.value });
  };
  onMessageChange = event => {
    this.setState({ message: event.target.value });
  };
  sendEmail() {
    const query = `
    mutation sendContactFormEmail($from:String!,$text:String!) {
      sendContactFormEmail(from: $from, text:$text) {
        from
        text
      }
    }`;
    const variables = {
      from: this.state.email,
      text: this.state.message
    };
    return request(publicRuntimeConfig.GRAPHQL_URL, query, variables);
  }
  render() {
    return (
      <div>
        <p class="text">
          Vous avez encore des questions ? des suggestions ? N'hésitez pas, nous
          sommes à votre disposition et serons ravis d'échanger avec vous :
          laissez-nous un message !<br />
          <br />
        </p>
        {this.state.emailSendingStatus === EMAIL_SENDING_STATUS_ERROR && (
          <div>
            Désolé nous avons rencontré une erreur lors de l'envoi de l'email.
            Vous pouvez nous contacter à l'addresse suivante :
            <strong>contact@aides-territoires.beta.gouv.fr</strong> ou{" "}
            <strong>elise.marion@beta.gouv.fr</strong>
          </div>
        )}
        {this.state.emailSendingStatus === EMAIL_SENDING_STATUS_SENT && (
          <div className="section message is-success">
            Merci! Votre message a bien été envoyé.
          </div>
        )}
        {/* afficher le formulaire sauf si il a bien été envoyé ou qu'il y a eu une erreur pendant l'envoi*/}
        {this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_ERROR &&
          this.state.emailSendingStatus !== EMAIL_SENDING_STATUS_SENT && (
            <form id="contact-form" onSubmit={this.handleSubmit}>
              <div className="field">
                <label className="label">Votre email*</label>
                <div className="control">
                  <input
                    id="email"
                    onChange={this.onEmailChange}
                    className="input is-large"
                    type="text"
                    placeholder="Email"
                    required
                  />
                </div>
              </div>

              <div className="field">
                <label className="label">Votre message</label>
                <div className="control">
                  <textarea
                    onChange={this.onMessageChange}
                    id="message"
                    className="textarea"
                    placeholder="Votre message"
                  />
                </div>
              </div>

              <div className="field is-grouped is-grouped-right">
                <div className="control">
                  <input
                    type="submit"
                    value="envoyer"
                    className="button is-link is-large is-primary"
                  />
                </div>
              </div>
            </form>
          )}
      </div>
    );
  }
}
