import React from "react";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";

class AdminAideList extends React.Component {
  static propTypes = {
    aides: PropTypes.array.isRequired,
    onDeleteClick: PropTypes.func
  };
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div className="AideList">
        <table className="table">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Mis à jour</th>
              <th>type</th>
              <th>Périmètre d'application type</th>
              <th>Status</th>
              <th>Editer</th>
              <th>Supprimer</th>
            </tr>
          </thead>
          <tbody>
            {this.props.aides.map(aide => {
              return (
                <tr key={aide.id}>
                  <td>{aide.nom}</td>
                  <td>{aide.updatedAt}</td>
                  <td>{aide.type}</td>
                  <td>{aide.perimetreApplicationType}</td>
                  <td>{aide.statusPublication}</td>
                  <td>
                    <NavLink
                      to={`/aide/${aide.id}/edit`}
                      className="button is-success"
                    >
                      Editer
                    </NavLink>
                  </td>
                  <td>
                    <span
                      onClick={e => this.props.onDeleteClick(aide)}
                      className="button is-danger"
                    >
                      Supprimer
                    </span>
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

export default AdminAideList;
