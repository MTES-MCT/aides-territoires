import React from "react";
import PropTypes from "prop-types";
import "./AideListItem.css";
// import { Link } from "react-router-dom";

class AideListItem extends React.Component {
  static propTypes = {
    aide: PropTypes.object.isRequired
  };
  render() {
    const { aide } = this.props;
    return (
      <div className="AideListItem search-result-list-item box">
        <h2 className="title is-4">{aide.nom}</h2>
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
                <td>{aide.beneficiaires.join(", ")}</td>
              </tr>
            )}
            <tr>
              <td>Porteur du dispositif</td>
              <td>{aide.structurePorteuse}</td>
            </tr>
            <tr>
              <td>Modalité de diffusion</td>
              <td>{aide.formeDeDiffusion.join(", ")}</td>
            </tr>
            <tr>
              <td>Périmètre application</td>
              <td>{aide.perimetreApplicationType}</td>
            </tr>
            <tr>
              <td>Type d'aide</td>
              <td>{aide.type}</td>
            </tr>
            <tr>
              <td>Temporalité dans le projet</td>
              <td>{aide.etape.join(", ")}</td>
            </tr>
            <tr>
              <td>Destination de l'aide</td>
              <td>{aide.destination}</td>
            </tr>
          </tbody>
        </table>
        <div className="thematiques">
          {aide.thematiques &&
            aide.thematiques.map(thematique => {
              return (
                <div className="tag is-success" style={{ marginRight: "20px" }}>
                  {thematique}
                </div>
              );
            })}
        </div>
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
