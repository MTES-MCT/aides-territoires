import React from "react";
import "./AideList.css";
import PropTypes from "prop-types";
import { NavLink } from "react-router-dom";

class AideList extends React.Component {
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
              <th>Supprimer</th>
              <th>Editer</th>
              <th>Nom</th>
              <th>Description</th>
              <th>type</th>
              <th>Périmètre d'application type</th>
              <th>Périmètre d'application nom</th>
              <th>Périmètre d'application (code)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {this.props.aides.map(aide => {
              return (
                <tr key={aide.id}>
                  <td>
                    <span
                      onClick={e => this.props.onDeleteClick(aide)}
                      className="button is-danger"
                    >
                      Supprimer
                    </span>
                  </td>
                  <td>
                    <NavLink
                      to={`/aide/${aide.id}/edit`}
                      className="button is-success"
                    >
                      Editer
                    </NavLink>
                  </td>
                  <td>{aide.name}</td>
                  <td>{aide.description}</td>
                  <td>{aide.type}</td>
                  <td>{aide.perimetreApplicationType}</td>
                  <td>{aide.perimetreApplicationName}</td>
                  <td>{aide.perimetreApplicationCode}</td>
                  <td>{aide.status}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
  }
}

export default AideList;
