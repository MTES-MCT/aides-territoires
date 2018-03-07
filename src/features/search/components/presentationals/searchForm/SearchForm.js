import React from "react";
import PropTypes from "prop-types";

class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: ""
    };
  }
  onSearchChange = event => {
    this.setState({
      text: event.target.value
    });
    this.props.onSearchChange(event.target.value);
  };
  onSubmit = event => {
    event.preventDefault();
    this.props.onSearchSubmit(this.state);
  };
  render() {
    return (
      <div className="search-form container">
        <form onSubmit={this.onSubmit}>
          <div className="field">
            <div className="control">
              <input
                name="text"
                placeholder="Code postal, ville, département ..."
                value={this.state.text}
                onChange={this.onSearchChange}
                className="input"
                type="text"
              />
            </div>
          </div>
          <div className="field">
            <div className="control">
              <button className="button is-primary">OK</button>
            </div>
          </div>
          {this.props.suggestions}
        </form>
      </div>
    );
  }
}

SearchForm.propTypes = {
  onSearchSubmit: PropTypes.func.isRequired,
  onSearchChange: PropTypes.func.isRequired,
  suggestions: PropTypes.array
};

export default SearchForm;
