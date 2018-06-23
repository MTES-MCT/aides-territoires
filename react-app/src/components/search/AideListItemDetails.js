import React from "react";
import PropTypes from "prop-types";
import injectSheet from "react-jss";
import classnames from "classnames";
import { compose } from "react-apollo";
import withEnums from "../decorators/withEnums";

class AideListItemDetails extends React.Component {
  static propTypes = {
    aide: PropTypes.object.isRequired
  };
  render() {
    const { aide, classes, getEnumValueFromId, enums } = this.props;
    return (
      <div className="AideListItemDetails">
        <table className={classnames("table", classes.table)}>
          <tbody>
            <tr>
              <td>Lien vers le site</td>
              <td>
                <a target="_blank" href={aide.lien}>
                  Lien vers le site
                </a>
              </td>
            </tr>
            {aide.beneficiaires && (
              <tr>
                <td>Bénéficiaires </td>
                <td>
                  {aide.beneficiaires
                    .map(
                      option =>
                        getEnumValueFromId("beneficiaires", option).label
                    )
                    .join(", ")}
                </td>
              </tr>
            )}
            <tr>
              <td>Porteur du dispositif</td>
              <td>{aide.structurePorteuse}</td>
            </tr>
            <tr>
              <td>Modalité de diffusion</td>
              <td>
                {aide.formeDeDiffusion
                  .map(
                    option =>
                      getEnumValueFromId("formeDeDiffusion", option).label
                  )
                  .join(", ")}
              </td>
            </tr>
            <tr>
              <td>Type d'aide</td>
              <td>{aide.type}</td>
            </tr>
            <tr>
              <td>Temporalité dans le projet</td>
              <td>
                {aide.etape
                  .map(option => getEnumValueFromId("etape", option).label)
                  .join(", ")}
              </td>
            </tr>
            <tr>
              <td>Destination de l'aide</td>
              <td>
                {aide.destination
                  .map(
                    option => getEnumValueFromId("destination", option).label
                  )
                  .join(", ")}
              </td>
            </tr>
          </tbody>
        </table>
        <div className="thematiques">
          {aide.thematiques &&
            aide.thematiques.map(thematique => {
              return (
                <div
                  key={thematique}
                  className="tag"
                  style={{ marginRight: "20px" }}
                >
                  {getEnumValueFromId("thematiques", thematique).label}
                </div>
              );
            })}
        </div>
      </div>
    );
  }
}

const styles = {
  table: {
    width: "100%",
    marginTop: "2rem",
    position: "relative",
    left: "-0.5rem",
    color: "#555"
  }
};

export default compose(
  injectSheet(styles),
  withEnums()
)(AideListItemDetails);
