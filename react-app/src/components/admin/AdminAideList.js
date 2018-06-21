import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";
import withUser from "../decorators/withUser";

class AdminAideList extends React.Component {
  static propTypes = {
    onDeleteClick: PropTypes.func
  };
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    console.log(this.props);
    return (
      <div className="AideList">
        <table className="table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Auteur</th>
              <th>Mis à jour</th>
              <th>type</th>
              <th>Périmètre d'application type</th>
              <th>Status</th>
              <th>Editer</th>
              <th>Supprimer</th>
            </tr>
          </thead>
          <tbody>
            {this.props.aides.edges.map(aide => {
              return (
                <tr key={aide.node.id}>
                  <td>{aide.node.nom}</td>
                  <td>
                    {aide.node.auteur && aide.node.auteur.name} -
                    {aide.node.auteur && aide.node.auteur.roles.join(",")}
                  </td>
                  <td>{aide.node.updatedAt}</td>
                  <td>{aide.node.type}</td>
                  <td>{aide.node.perimetreApplicationType}</td>
                  <td>{aide.node.statusPublication}</td>
                  <td>
                    {aide.meta.userPermissions.includes("edit") && (
                      <NavLink
                        to={`/aide/${aide.node.id}/edit`}
                        className="button is-success"
                      >
                        Editer
                      </NavLink>
                    )}
                  </td>
                  <td>
                    {aide.meta.userPermissions.includes("delete") && (
                      <span
                        onClick={e => this.props.onDeleteClick(aide)}
                        className="button is-danger"
                      >
                        Supprimer
                      </span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default withUser({ mandatory: true })(AdminAideList);
