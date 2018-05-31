import React from "react";
import AideList from "modules/search/presentationals/AideList";

function getGroupTitleFromGroupType(groupType) {
  let title = "";
  switch (groupType) {
    case "votre_commune":
      title = "Dans votre commun";
      break;
    case "votre_departement":
      title = "Dans votre département";
      break;
    case "votre_region":
      title = "Dans votre région";
      break;
    default:
      title = null;
  }
  return title;
}

const GroupeDeResultat = ({ groupeDeResultat, displayGroupLabel }) => {
  return (
    <div>
      {displayGroupLabel && (
        <div
          style={{
            textAlign: "right",
            margin: "0.5rem",
            borderBottom: "solid rgb(240,240,240) 1px"
          }}
        >
          <em>{groupeDeResultat.label}</em>
        </div>
      )}
      {groupeDeResultat.aidesParTypeDeTerritoires.map(territoire => {
        return (
          <AideList
            groupeDeResultat={groupeDeResultat}
            key={territoire.type}
            aides={territoire.aides}
          />
        );
      })}
      {/*
      {groupeDeResultat.aidesParTypeDeTerritoires.aides.map(aide => {
        return (
          <AideList
            key={groupeDeResultat.type}
            aides={aide}
          />
        );
      })}
      */}
    </div>
  );
};

/**
 */
const SearchResults = ({ results, filters }) => {
  if (!results) return null;
  return (
    <div>
      <div className="message is-info">
        <div className="message-body" style={{ border: "none" }}>
          <strong>{results.totalNombreAides}</strong> aides correspondent à
          votre recherche <strong>{filters.texte && `${filters.texte}`}</strong>
        </div>
      </div>
      {results.groupesDeResultats.map(groupeDeResultat => {
        return (
          <GroupeDeResultat
            // o naffiche les labels de groupes de résutlats si on a au moins 2 groupes de résultats
            displayGroupLabel={results.groupesDeResultats.length > 1}
            key={groupeDeResultat.type}
            groupeDeResultat={groupeDeResultat}
          />
        );
      })}
    </div>
  );
};

export default SearchResults;
