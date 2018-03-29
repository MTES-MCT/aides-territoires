import React from "react";
import DefaultLayout from "../components/DefaultLayout";
import HeaderAPropos from "../components/HeaderAPropos";
import SectionCommentCaMarche from "../components/SectionCommentCaMarche";
import SectionChronophage from "../components/SectionChronophage";
import SectionBenefices from "../components/SectionBenefices";
import SectionTypeAides from "../components/SectionTypesAides";
import SendInBlueInscrivezVous from "../components/SendInBlueInscrivezVous";
import SendInBlueContactForm from "../components/SendInBlueContactForm";

class porteurAidePage extends React.Component {
  render() {
    return (
      <DefaultLayout>
        <HeaderAPropos />
      </DefaultLayout>
    );
  }
}

export default porteurAidePage;
