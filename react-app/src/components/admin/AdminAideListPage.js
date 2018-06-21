import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import Loader from "../ui/AppLoader";
import AdminAideList from "./AdminAideList";
import GraphQLError from "../ui/GraphQLError";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";

import withUser from "../decorators/withUser";

const AideListPage = class extends React.Component {
  state = {
    // will contain aide we want to delete
    requestAideDeletion: false
  };
  deleteAide = aide => {
    this.props.deleteAide({
      variables: { id: aide.id },
      refetchQueries: ["adminAllAides"]
    });
    this.setState({ requestAideDeletion: null });
  };
  render() {
    const { loading, allAides, error } = this.props.data;
    return (
      <AdminLayout>
        <Dialog
          title=""
          actions={[
            <FlatButton
              label="ANNULER"
              primary={true}
              onClick={() => this.setState({ requestAideDeletion: null })}
            />,
            <FlatButton
              label="SUPPRIMER"
              secondary={true}
              keyboardFocused={true}
              onClick={() => this.deleteAide(this.state.requestAideDeletion)}
            />
          ]}
          modal={false}
          open={this.state.requestAideDeletion}
          onRequestClose={this.handleClose}
        >
          <div className="has-text-centered">
            Etes vous sûr de vouloir supprimer l'aide{" "}
            {this.state.requestAideDeletion && (
              <div>
                <strong>{this.state.requestAideDeletion.nom}</strong> ? Cette
                action est irréversible
              </div>
            )}
          </div>
        </Dialog>
        <h1 className="title is-1">Liste des aides</h1>
        {error && <GraphQLError error={error} />}
        {!allAides && loading && <Loader />}
        {allAides && (
          <AdminAideList
            onDeleteClick={aide => this.setState({ requestAideDeletion: aide })}
            aides={allAides}
          />
        )}
      </AdminLayout>
    );
  }
};

const allAidesQuery = gql`
  query adminAllAides {
    allAides {
      edges {
        meta {
          userPermissions
        }
        node {
          id
          createdAt
          updatedAt
          nom
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
          destination
          destinationAutre
          formeDeDiffusion
          formeDeDiffusionAutre
          beneficiaires
          categorieParticuliere
          demandeTiersPossible
          auteur {
            id
            name
            roles
          }
        }
      }
    }
  }
`;

const deleteAideMutation = gql`
  mutation deleteAide($id: ID) {
    deleteAide(id: $id) {
      n
      ok
    }
  }
`;

export default compose(
  withUser({ mandatory: true }),
  graphql(allAidesQuery),
  graphql(deleteAideMutation, { name: "deleteAide" })
)(AideListPage);
