import React from "react";
import PropTypes from "prop-types";
import SearchFormSuggestionList from "../searchFormSuggestionList/SearchFormSuggestionList";
import "./SearchForm.css";

class SearchForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: ""
    };
  }
  onInputChange = event => {
    const value = event.target.value;
    this.setState({
      text: value
    });
    this.props.onSearchChange(value);
  };
  onUpdateInput = value => {
    this.setState({
      text: value
    });
    this.props.onSearchChange(value);
  };
  onSubmit = event => {
    event.preventDefault();
    this.props.onSearchSubmit(this.state);
  };
  onNewRequest = value => {};
  render() {
    return (
      <div className="search-form container section">
        <form onSubmit={this.onSubmit}>
          {/*
          <AutoComplete
            floatingLabelText="Code postal, ville, département, région ..."
            fullWidth={true}
            dataSource={this.props.suggestions}
            filter={AutoComplete.noFilter}
            onUpdateInput={this.onUpdateInput}
            onNewRequest={this.onNewRequest}
          />
          <RaisedButton onClick={this.onSubmit} label="OK" />
          */}
          <div className="field has-addons">
            <div className="control is-expanded">
              <input
                onChange={this.onInputChange}
                className="input is-large"
                type="text"
                placeholder="Find a repository"
              />
              {this.props.suggestions.length > 0 && (
                <div className="suggestions">
                  <SearchFormSuggestionList
                    suggestions={this.props.suggestions}
                  />
                </div>
              )}
            </div>
            <div className="control">
              <input
                type="submit"
                value="Chercher"
                className="button is-info is-large"
              />
            </div>
          </div>
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
