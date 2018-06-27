import React from "react";
import AdminLayout from "../layouts/AdminLayout";
import { graphql, compose } from "react-apollo";
import gql from "graphql-tag";
import AppLoader from "../ui/AppLoader";
import AdminAideList from "./AdminAideList";
import GraphQLError from "../ui/GraphQLError";
import Dialog from "material-ui/Dialog";
import FlatButton from "material-ui/FlatButton";
import AdminAllAidesQuery from "./AdminAllAidesQuery";
import withUser from "../decorators/withUser";

const AideListPage = class extends React.Component {
  state = {
    showDeleteModal: false,
    aideToDelete: null
  };
  deleteAide = aide => {
    this.props.deleteAide({
      variables: { id: aide.id },
      refetchQueries: ["adminAllAides"]
    });
    this.setState({ requestAideDeletion: null });
  };
  // quand on clique sur "supprimer", afficher la modale
  // de confirmation de suppression
  handleClickDelete = aide => {
    this.setState({
      showDeleteModal: true,
      aideToDelete: aide
    });
  };
  // quand on clique sur le bouton "annuler" de la modale de
  // confirmation de suppresion d'aide
  handleDeleteModalCancel = () => {
    this.setState({
      showDeleteModal: false,
      aideToDelete: null
    });
  };
  // quand on clique sur le bouton "supprimer" de la modale de
  // confirmation de suppression d'aide
  handleDeleteModalDelete = aide => {
    this.deleteAide({ id: aide.node.id });
    this.setState({
      showDeleteModal: false
    });
  };
  handleClickCancel = () => {
    //this.setState({ requestAideDeletion: null })
  };
  render() {
    return (
      <AdminLayout>
        <h1 className="title is-1">Liste des aides</h1>
        <DeleteModal
          show={this.state.showDeleteModal}
          aideToDelete={this.state.aideToDelete}
          onClickCancel={this.handleDeleteModalCancel}
          onClickDelete={this.handleDeleteModalDelete}
        />
        <AdminAllAidesQuery filters={{}}>
          {aides => {
            return (
              <AdminAideList
                onDeleteClick={this.handleClickDelete}
                aides={aides}
              />
            );
          }}
        </AdminAllAidesQuery>
      </AdminLayout>
    );
  }
};

/**
 * Modale de confirmation de la suppression d'une aide
 */
const DeleteModal = ({
  show,
  onClickCancel,
  onClickDelete,
  onRequestClose,
  aideToDelete
}) => (
  <Dialog
    title=""
    actions={[
      <FlatButton label="ANNULER" primary={true} onClick={onClickCancel} />,
      <FlatButton
        label="SUPPRIMER"
        secondary={true}
        keyboardFocused={true}
        onClick={() => onClickDelete(aideToDelete)}
      />
    ]}
    modal={false}
    open={show}
    onRequestClose={onRequestClose}
  >
    {aideToDelete && (
      <div className="has-text-centered">
        <p>
          Etes vous sûr de vouloir supprimer l'aide <br />
          <strong style={{ color: "black" }}> {aideToDelete.node.nom}</strong> ?
        </p>
        <p> Cette action est irréversible.</p>
      </div>
    )}
  </Dialog>
);

const mutation = gql`
  mutation deleteAide($id: ID) {
    deleteAide(id: $id) {
      n
      ok
    }
  }
`;

export default compose(
  withUser({ mandatory: true }),
  graphql(mutation, { name: "deleteAide" })
)(AideListPage);
