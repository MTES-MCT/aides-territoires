import React from "react";
import Layout from "../../common/layouts/Layout";
import Header from "../../common/presentationals/Header";
import Benefices from "../presentationals/Benefices";
import CommentCaMarche from "../presentationals/CommentCaMarche";
import Chronophage from "../presentationals/Chronophage";
import graphcms from "../../../services/graphcms";

class HomePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      Pagedaccueil: {}
    };
  }
  componentWillMount() {
    const query = `{
      Pagedaccueil(id:"cjfdxk4tpcy3v016424h68se6") {
        commentcamarchetitre
        commentcamarchebloc1
        commentcamarchebloc2
        commentcamarchebloc3
        commentcamarchebloc1titre
        commentcamarchebloc2titre
        commentcamarchebloc3titre
        header
        headercalltoaction
        headertitre
        probleme
        benefices
        texteduformulaireaideecoquartiers
        texteduformulairedecontact
      }
    }
    `;
    graphcms.request(query).then(Pagedaccueil => {
      this.setState(Pagedaccueil);
    });
  }
  render() {
    const Pagedaccueil = this.state.Pagedaccueil;
    return (
      <Layout>
        <Header data={Pagedaccueil} />
        <CommentCaMarche data={Pagedaccueil} />
        <Chronophage data={Pagedaccueil} />
        <Benefices data={Pagedaccueil} />
      </Layout>
    );
  }
}

export default HomePage;
