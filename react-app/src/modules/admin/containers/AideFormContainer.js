import React from "react";
import AideForm from "modules/admin/presentationals/AideForm";
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
    if (values.perimetreApplication === "departement") {
      values.perimetreApplicationCode = values.departement.value;
    }
    if (values.perimetreApplication === "region") {
      values.perimetreApplicationCode = values.region.value;
    }
    console.log(values);
    this.props
      .createAide({
        variables: { ...values },
        // mettre à jour la liste des aides dans l'admin
        refetchQueries: ["adminAllAides"]
      })
      .then(r =>
        this.setState({
          submissionStatus: SUBMISSION_STATUS_FINISHED
        })
      )
      .catch(e => {
        console.error(e);
      });
  };
  render() {
    if (this.state.submissionStatus === SUBMISSION_STATUS_FINISHED) {
      return <Redirect push to="/aide/list" />;
    }
    return <AideForm onSubmit={this.handleSubmit} />;
  }
}

const createAide = gql`
  mutation createAide(
    $name: String!
    $description: String!
    $type: String!
    $perimetreDiffusion: String
    $perimetreApplication: String
    $perimetreApplicationCode: String
    $etape: String
    $structurePorteuse: String!
    $status: String!
  ) {
    createAide(
      name: $name
      description: $description
      type: $type
      perimetreDiffusion: $perimetreDiffusion
      perimetreApplication: $perimetreApplication
      perimetreApplicationCode: $perimetreApplicationCode
      etape: $etape
      structurePorteuse: $structurePorteuse
      status: $status
    ) {
      name
    }
  }
`;

export default graphql(createAide, { name: "createAide" })(AideFormContainer);
