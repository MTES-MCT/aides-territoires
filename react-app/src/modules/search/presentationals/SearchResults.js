import React from "react";
import AllAidesQuery from "modules/search/decorators/AllAidesQuery";
import AideList from "modules/search/presentationals/AideList";
import { connect } from "react-redux";

const SearchResultsTopText = () => (
  <div className="notification">
    Par défaut, le moteur de recherche présente toutes les aides disponibles sur
    votre territoire.Vous pouvez utiliser les filtres ci-contre pour préciser
    votre recherche et sélectionner vos critères
  </div>
);

const SearchResults = ({ filters }) => {
  return (
    <AllAidesQuery filters={filters}>
      {({ aides }) => (
        <div>
          <AideList aides={aides} />
        </div>
      )}
    </AllAidesQuery>
  );
};

export default SearchResults;
