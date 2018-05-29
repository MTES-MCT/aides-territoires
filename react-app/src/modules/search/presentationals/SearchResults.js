import React from "react";
import AideList from "modules/search/presentationals/AideList";

/**
 *
 * @param {} param0
 */
const SearchResults = ({ results }) => {
  return (
    <div>
      <h2>Nous avons trouvé {results.totalCount} aides pour votre recherche</h2>
      {results.resultsGroups.map(group => {
        return <AideList aides={group.aides} />;
      })}
    </div>
  );
};

export default SearchResults;
