import React from "react";
import TypeDeTerritoireForm from "modules/aide/presentationals/TypeDeTerritoireForm";
import { graphql } from "react-apollo";
import gql from "graphql-tag";

class TypeDeTerritoireContainer extends React.Component {
  state = {
    formValues: []
  };
  handleSubmit = values => {
    this.props.createTypeDeTerritoire({
      variables: { name: values.name, description: values.description }
    });
  };
  render() {
    return <TypeDeTerritoireForm onSubmit={this.handleSubmit} />;
  }
}

const createTypeDeTerritoire = gql`
  mutation createTypeDeTerritoire($name: String!, $description: String!) {
    createTypeDeTerritoire(name: $name, description: $description) {
      name
      description
    }
  }
`;

export default graphql(createTypeDeTerritoire, {
  name: "createTypeDeTerritoire"
})(TypeDeTerritoireContainer);
