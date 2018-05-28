import React from "react";
import Layout from "../../common/layouts/Layout";
import SearchFormContainer from "../decorators/SearchFormContainer";
import { Redirect } from "react-router-dom";
import { change } from "redux-form";
import { connect } from "react-redux";
import classnames from "classnames";
import injectSheet from "react-jss";
import { buildUrlParamsFromFilters } from "../../../services/searchLib";

const styles = {
  title: {
    paddingBottom: "3rem"
  }
};

class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      filters: {}
    };
  }
  onSearchSubmit = values => {
    // this.props.change("searchFormFilters");
    this.setState({ filters: values });
  };
  render() {
    if (Object.keys(this.state.filters).length > 0) {
      const params = buildUrlParamsFromFilters(this.state.filters);
      return <Redirect push to={`/aides?${params}`} />;
    }
    return (
      <Layout>
        <section className="section container">
          <div className="has-text-centered">
            <h2 className={classnames("title is-2", this.props.classes.title)}>
              Je veux connaître les aides disponibles sur mon territoire :
            </h2>
            <SearchFormContainer onSearchSubmit={this.onSearchSubmit} />
          </div>
        </section>
      </Layout>
    );
  }
}

function mapStateToProps() {
  return {};
}

function mapDispatchToProps(dispatch) {
  return {
    change: (form, field, value) => {
      dispatch(change(form, field, value));
    }
  };
}

SearchPage = connect(mapStateToProps, mapDispatchToProps)(SearchPage);
export default injectSheet(styles)(SearchPage);
