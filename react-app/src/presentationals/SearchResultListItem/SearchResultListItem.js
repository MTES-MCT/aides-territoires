import React from "react";
import PropTypes from "prop-types";
// import { Link } from "react-router-dom";

class SearchResultListItem extends React.Component {
  static propTypes = {
    result: PropTypes.array.isRequired
  };
  render() {
    const { result } = this.props;
    return (
      <div className="search-result-list-item box">
        <h2 className="title is-4">{result.intitulé}</h2>
        <p className="content">
          <em>{result.objectifs}</em>
        </p>
        <table className="table">
          <tbody>
            <tr>
              <td>Lien vers le site</td>
              <td>
                <a target="_blank" href={result.lienVersLeSite}>
                  Lien vers le site
                </a>
              </td>
            </tr>
            {/*
          <tr>
            <td>Dotation</td>
            <td>{result.dotation}</td>
          </tr>
          */}
            <tr>
              <td>Date de clotûre </td>
              <td>{result.dateDeClôture}</td>
            </tr>
            <tr>
              <td>Bénéficiaires </td>
              <td>{result.bénéficiaires}</td>
            </tr>
            <tr>
              <td>Porteur du dispositif</td>
              <td>{result.porteurDuDispositif}</td>
            </tr>
            <tr>
              <td>Type d'aide</td>
              <td>{result.type}</td>
            </tr>
          </tbody>
        </table>
        {result.sousThématique.split(",").map((item, index) => {
          return (
            <div
              key={index}
              style={{ marginRight: "10px" }}
              className="tag is-success thematique"
            >
              {item}
            </div>
          );
        })}
        {result.sousThématique2.split(",").map((item, index) => {
          return (
            <div
              key={index}
              style={{ marginRight: "10px" }}
              className="tag is-info thematique"
            >
              {item}
            </div>
          );
        })}
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

export default SearchResultListItem;
