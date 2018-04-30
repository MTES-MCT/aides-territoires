import React, { Component } from "react";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "modules/ui-kit/AppLoader";
import PropTypes from "prop-types";

const searchAidesQuery = gql`
  query searchAidesQuery($etape: [searchAideEtapes], $type: [searchAideTypes]) {
    aides: searchAides(etape: $etape, type: $type) {
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
      perimetreApplicationCode: PropTypes.string
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
        return {
          variables
        };
      }
    })
  )(AidesProvider);
};
