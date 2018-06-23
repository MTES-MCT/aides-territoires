import React from "react";
import PropTypes from "prop-types";
import AideListItem from "./AideListItem";
import injectSheet from "react-jss";

class SearchResultList extends React.Component {
  static propTypes = {
    aides: PropTypes.array.isRequired,
    title: PropTypes.string
  };
  render() {
    return (
      <div>
        {this.props.aides.map(aide => (
          <div
            key={this.props.groupeDeResultat.type + "-" + aide.id}
            style={{ padding: "0.5rem" }}
          >
            <AideListItem aide={aide} />
          </div>
        ))}
      </div>
    );
  }
}

const styles = {
  listItem: {
    marginBottom: "1rem"
  }
};

export default injectSheet(styles)(SearchResultList);
