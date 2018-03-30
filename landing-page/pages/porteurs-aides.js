import React from "react";
import DefaultLayout from "../components/common/DefaultLayout";
import Header from "../components/porteurs-aides/Header";
import Content from "../components/porteurs-aides/Content";
import FormPorteurProjetToutType from "../components/porteurs-aides/FormPorteurProjetToutType";
import graphcms from "../services/graphcms";

class porteurAidePage extends React.Component {
  static async getInitialProps({ req }) {
    const query = `{
      PagePorteursdaides(id: "cjfe48qedp9ot0141zb2iaw2d") {
        titreduheader
        texteduheader
        textebloc1
        textebloc2
      }
    }       
    `;
    return graphcms.request(query);
  }
  render() {
    return (
      <DefaultLayout>
        <Header data={this.props.PagePorteursdaides} />
        <Content data={this.props.PagePorteursdaides} />
        <FormPorteurProjetToutType />
      </DefaultLayout>
    );
  }
}

export default porteurAidePage;
