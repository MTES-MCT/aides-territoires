import React from "react";
import SearchAidesQuery from "modules/search/decorators/SearchAidesQuery";
import AideList from "modules/search/presentationals/AideList";

const SearchResults = ({ filters }) => {
  console.log("filters", filters);
  return (
    <SearchAidesQuery filters={filters}>
      {({ aides }) => <div>{/*<AideList aides={aides} />*/}</div>}
    </SearchAidesQuery>
  );
};

export default SearchResults;
