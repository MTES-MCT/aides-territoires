import React from "react";
import AideList from "./AideList";

/**
 * Affiche les résultats pour la recherche par territoire.
 * Il y a en résultats des "groupes de résultats" :
 * - les résultats trouvés pres de la localisation demandées
 * - puis un groupe de résultat par type de territoire
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
    </div>
  );
};

export default SearchResults;
