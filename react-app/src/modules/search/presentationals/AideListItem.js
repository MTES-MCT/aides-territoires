import React from "react";
import PropTypes from "prop-types";
// import { Link } from "react-router-dom";

class AideListItem extends React.Component {
  static propTypes = {
    aide: PropTypes.object.isRequired
  };
  render() {
    const { aide } = this.props;
    return (
      <div className="search-result-list-item box">
        <h2 className="title is-4">{aide.name}</h2>
        <p className="content">
          <em>{aide.description}</em>
        </p>
        <table className="table">
          <tbody>
            <tr>
              <td>Lien vers le site</td>
              <td>
                <a target="_blank" href={aide.lien}>
                  Lien vers le site
                </a>
              </td>
            </tr>
            {/*
          <tr>
            <td>Dotation</td>
            <td>{result.dotation}</td>
          </taider>
          */}
            {aide.beneficiaires && (
              <tr>
                <td>Bénéficiaires </td>
                <td>{aide.beneficiaires}</td>
              </tr>
            )}
            <tr>
              <td>Porteur du dispositif</td>
              <td>{aide.structurePorteuse}</td>
            </tr>
            <tr>
              <td>Type d'aide</td>
              <td>{aide.type}</td>
            </tr>
          </tbody>
        </table>
        {/*
        <Link
          to={{ pathname: "/aide", state: { aide: result } }}
          className="button is-primary"
        >
          Voir la fiche
        </Link>
        */}
      </div>
    );
  }
}

export default AideListItem;
