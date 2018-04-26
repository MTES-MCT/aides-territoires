import React from "react";
import AideForm from "modules/aide/presentationals/AideForm";
import { graphql } from "react-apollo";
import gql from "graphql-tag";

class AideFormContainer extends React.Component {
  state = {
    formValues: []
  };
  handleSubmit = values => {
    this.props.AideSave({
      variables: { name: values.name, description: values.description }
    });
  };
  render() {
    return <AideForm onSubmit={this.handleSubmit} />;
  }
}

const AideSave = gql`
  mutation AideSave($name: String!, $description: String!) {
    AideSave(name: $name, description: $description) {
      name
      description
    }
  }
`;

export default graphql(AideSave, { name: "AideSave" })(AideFormContainer);
