import React from "react";
import PropTypes from "prop-types";
import AideList from "../presentationals/AideList";
import SearchFilters from "../presentationals/SearchFilters";
import RaisedButton from "material-ui/RaisedButton";

class SearchResultListContainer extends React.Component {
  constructor(props) {
    super(props);
    this.codeCommune = null;
    this.codeDepartement = null;
    this.codeRegion = null;
  }
  render() {
    return (
      <div>
        <div>
          <header style={{ textAlign: "right" }}>
            <RaisedButton
              style={{ marginRight: "20px" }}
              primary={true}
              label="Imprimer mes résultats"
            />
            <RaisedButton
              style={{ marginRight: "20px" }}
              secondary={true}
              label="Partager mes résultats"
            />
            <RaisedButton
              style={{ marginRight: "20px" }}
              label="Etre alerté de nouvelles aides"
            />
          </header>
          <div className="columns">
            <div className="column is-one-quarter">
              <SearchFilters />
            </div>
            <div className="column">
              <div className="search-result-list" />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default SearchResultListContainer;
