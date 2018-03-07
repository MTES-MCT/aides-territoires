import React from "react";
import PropTypes from "prop-types";
import AutoComplete from "material-ui/AutoComplete";
import RaisedButton from "material-ui/RaisedButton";

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
      <div className="search-form container">
        <form onSubmit={this.onSubmit}>
          <AutoComplete
            floatingLabelText="Code postal, ville, département, région ..."
            fullWidth={true}
            dataSource={this.props.suggestions}
            filter={AutoComplete.noFilter}
            onUpdateInput={this.onUpdateInput}
            onNewRequest={this.onNewRequest}
          />
          <RaisedButton onClick={this.onSubmit} label="OK" />
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
