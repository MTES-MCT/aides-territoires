import React from "react";
import AideForm from "modules/aide/presentationals/AideForm";
import { graphql } from "react-apollo";
import gql from "graphql-tag";

class AideFormContainer extends React.Component {
  state = {
    formValues: []
  };
  handleSubmit = values => {
    this.props.createAide({
      variables: { name: values.name, description: values.description }
    });
  };
  render() {
    return <AideForm onSubmit={this.handleSubmit} />;
  }
}

const createAide = gql`
  mutation createAide($name: String!, $description: String!) {
    createAide(name: $name, description: $description) {
      name
      description
    }
  }
`;

export default graphql(createAide, { name: "createAide" })(AideFormContainer);
