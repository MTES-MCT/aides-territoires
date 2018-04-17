import React from "react";
import AideForm from "../presentationals/AideForm";

export default class AideFormContainer extends React.Component {
  state = {
    formValues: []
  };
  onSubmit = values => {
    console.log(values);
    // postOnRocketChatNantes(values);
  };
  render() {
    return <AideForm onSubmit={this.onSubmit} />;
  }
}
