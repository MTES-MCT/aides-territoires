import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import PropTypes from "prop-types";

const searchAidesQuery = gql`
  query searchAidesQuery(
    $etape: [searchAideEtapes]
    $type: [searchAideTypes]
    $statusPublication: [searchAideStatusPublicaton]
  ) {
    aides: searchAides(
      etape: $etape
      type: $type
      statusPublication: $statusPublication
    ) {
      id
      nom
      createdAt
      updatedAt
      description
      perimetreApplicationType
      perimetreApplicationNom
      perimetreApplicationCode
      perimetreDiffusionType
      etape
      structurePorteuse
      statusPublication
      lien
      type
      beneficiaires
    }
  }
`;

export default WrappedComponent => {
  class AidesProvider extends Component {
    static propTypes = {
      perimetreApplicationType: PropTypes.string,
      perimetreApplicationCode: PropTypes.string,
      statusPublication: PropTypes.array,
      type: PropTypes.array
    };
    constructor(props) {
      super(props);
      this.state = {};
    }
    render() {
      if (!this.props.data.aides) {
        return <AppLoader />;
      }
      return (
        <div>
          <WrappedComponent aides={this.props.data.aides} {...this.props} />
        </div>
      );
    }
  }
  return compose(
    graphql(searchAidesQuery, {
      options: props => {
        const variables = {};
        if (props.etape && props.etape.length > 0) {
          variables.etape = props.etape;
        }
        if (props.type && props.type.length > 0) {
          variables.type = props.type;
        }
        if (props.statusPublication) {
          variables.statusPublicaton = props.statusPublication;
        }
        return {
          variables
        };
      }
    })
  )(AidesProvider);
};
