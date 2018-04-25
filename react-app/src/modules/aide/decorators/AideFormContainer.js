import React from "react";
import AideForm from "modules/aide/presentationals/AideForm";
import { graphql } from "react-apollo";
import gql from "graphql-tag";

class AideFormContainer extends React.Component {
  state = {
    formValues: []
  };
  handleSubmit = values => {
    console.log(values);
  };
  render() {
    return <AideForm onSubmit={this.handleSubmit} />;
  }
}

export default graphql(gql`
  {
    allPagedaccueils {
      header
    }
  }
`)(AideFormContainer);
