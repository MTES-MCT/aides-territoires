import React from "react";
import PropTypes from "prop-types";
import SearchResultList from "../presentationals/SearchResultList";
import { connectToSpreadsheet } from "react-google-sheet-connector";

const styles = {
  title: {
    marginTop: "50px"
  },
  groupTitle: {
    marginTop: "50px"
  }
};

class SearchResultListContainer extends React.Component {
  constructor(props) {
    super(props);
    this.sheetData = this.props.getSheet("ELISE-PROTO");
    this.codeCommune = null;
    this.codeDepartement = null;
    this.codeRegion = null;
  }
  getAidesByTypeAndCodeInsee(type, codeInsee = null) {
    let results = [];
    this.sheetData.map(row => {
      if (!codeInsee) {
        if (row.typeDePérimètre === type) {
          results.push(row);
        }
      }
      if (codeInsee) {
        if (row.typeDePérimètre === type && row.codeInsee == codeInsee) {
          results.push(row);
        }
      }
    });
    return results;
  }
  render() {
    let resultsGroups = [];
    console.log("searchedData debug : ", this.props.searchedData);
    if (this.props.searchedData.type === "commune") {
      this.codeCommune = this.props.searchedData.data.code;
      this.codeDepartement = this.props.searchedData.data.codeDepartement;
      this.codeRegion = this.props.searchedData.data.codeRegion;
    }
    if (this.props.searchedData.type === "departement") {
      this.codeDepartement = this.props.searchedData.data.code;
      this.codeRegion = this.props.searchedData.data.codeRegion;
    }
    if (this.props.searchedData.type === "region") {
      this.codeRegion = this.props.searchedData.data.code;
    }

    // afficher les aides de la communes, si il y en a
    if (this.codeCommune) {
      const aidesCommunes = this.getAidesByTypeAndCodeInsee(
        "commune",
        this.codeCommune
      );
      if (aidesCommunes.length > 0) {
        resultsGroups.push({
          title: "Communes",
          results: aidesCommunes
        });
      }
    }

    // afficher les aides des département, si il y en a
    if (this.codeDepartement) {
      const aidesDepartements = this.getAidesByTypeAndCodeInsee(
        "commune",
        this.codeCommune
      );
      if (aidesDepartements.length > 0) {
        resultsGroups.push({
          title: "Département",
          results: aidesDepartements
        });
      }
    }

    // afficher les aides de la région, si il y en a
    if (this.codeRegion) {
      const aidesRegion = this.getAidesByTypeAndCodeInsee(
        "region",
        this.codeRegion
      );
      if (aidesRegion.length > 0) {
        resultsGroups.push({
          title: "Région",
          results: aidesRegion
        });
      }
    }
    resultsGroups.push({
      title: "National",
      results: this.getAidesByTypeAndCodeInsee("national")
    });
    resultsGroups.push({
      title: "Europe",
      results: this.getAidesByTypeAndCodeInsee("europe")
    });
    // nombre total de résultats
    const totalResults = resultsGroups.reduce((total, group) => {
      return total + group.results.length;
    }, 0);
    return (
      <div className="search-result-list">
        {this.props.searchedData.text && (
          <h2 style={styles.title} className="subtitle is-3">
            Nous avons trouvé <strong>{totalResults}</strong> aides pour
            lesquelles le territoire
            <strong>{this.props.searchedData.text}</strong>
          </h2>
        )}
        {resultsGroups.map((resultsGroup, index) => {
          return (
            <div key={index} className="content">
              <h2 style={styles.groupTitle} className="subtitle is-4">
                {resultsGroup.title}
              </h2>
              {resultsGroup.results.length === 0 && <div>Pas de résultat</div>}
              {resultsGroup.results && (
                <SearchResultList
                  key={index}
                  {...this.props}
                  results={resultsGroup.results}
                />
              )}
            </div>
          );
        })}
      </div>
    );
  }
}

SearchResultListContainer.propTypes = {
  searchedData: PropTypes.shape({
    type: PropTypes.string,
    codeCommune: PropTypes.string,
    codeDepartement: PropTypes.string,
    codeRegion: PropTypes.string
  })
};

export default connectToSpreadsheet(SearchResultListContainer);
