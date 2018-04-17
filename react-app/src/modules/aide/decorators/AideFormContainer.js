import React from "react";
import AideForm from "modules/aide/presentationals/AideForm";

export default class AideFormContainer extends React.Component {
  state = {
    formValues: []
  };
  handleSubmit = values => {
    console.log(values);
    // postOnRocketChatNantes(values);
  };
  render() {
    return <AideForm onSubmit={this.handleSubmit} />;
  }
}
