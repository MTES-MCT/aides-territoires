import React from "react";
import "./AideList.css";
import PropTypes from "prop-types";

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
              <th>Actions</th>
              <th>Nom</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {this.props.aides.map(aide => {
              return (
                <tr key={aide.id}>
                  <td>
                    <div
                      onClick={e => this.props.onDeleteClick(aide)}
                      className="button is-danger"
                    >
                      Supprimer
                    </div>
                  </td>
                  <td>{aide.name}</td>
                  <td>{aide.description}</td>
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
