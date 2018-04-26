import React from "react";
import AideForm from "modules/aide/presentationals/AideForm";
import { Redirect } from "react-router";
import { graphql } from "react-apollo";
import gql from "graphql-tag";
import allAidesQuery from "modules/admin/pages/AideListPage";

const SUBMISSION_STATUS_NOT_STARTED = "not_started";
const SUBMISSION_STATUS_PENDING = "pending";
const SUBMISSION_STATUS_FINISHED = "finished";

class AideFormContainer extends React.Component {
  state = {
    formValues: [],
    submissionStatus: SUBMISSION_STATUS_NOT_STARTED
  };
  handleSubmit = values => {
    this.setState({
      submissionStatus: SUBMISSION_STATUS_PENDING
    });
    this.props
      .createAide({
        variables: { name: values.name, description: values.description },
        // mettre à jour la liste des aides dans l'admin
        refetchQueries: ["adminAllAides"]
      })
      .then(r =>
        this.setState({
          submissionStatus: SUBMISSION_STATUS_FINISHED
        })
      );
  };
  render() {
    if (this.state.submissionStatus === SUBMISSION_STATUS_FINISHED) {
      return <Redirect push to="/aide/list" />;
    }
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
