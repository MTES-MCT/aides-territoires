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

/**
 *
 * @param {} param0
 */
const SearchResults = ({ results }) => {
  return (
    <div>
      <div className="message is-info">
        <div className="message-body" style={{ border: "none" }}>
          {console.log(results)}
          <strong>{results.totalCount}</strong> aides correspondent à votre
          recherche
        </div>
      </div>
      {results.resultsGroups.map(group => {
        return <AideList key={group.type} aides={group.aides} />;
      })}
    </div>
  );
};

export default SearchResults;
