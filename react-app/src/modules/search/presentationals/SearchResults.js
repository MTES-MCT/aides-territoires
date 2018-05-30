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

const GroupeDeResultat = ({ groupeDeResultat }) => {
  return (
    <div>
      {groupeDeResultat.label}
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
const SearchResults = ({ results }) => {
  return (
    <div>
      <div className="message is-info">
        <div className="message-body" style={{ border: "none" }}>
          <strong>{results.totalNombreAides}</strong> aides correspondent à
          votre recherche
        </div>
      </div>
      {results.groupesDeResultats.map(groupeDeResultat => {
        return (
          <GroupeDeResultat
            key={groupeDeResultat.type}
            groupeDeResultat={groupeDeResultat}
          />
        );
      })}
    </div>
  );
};

export default SearchResults;
