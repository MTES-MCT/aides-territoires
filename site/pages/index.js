import Document, { meta } from "../content/index.md";
import Header from "../components/ui/Header";
import ButtonLink from "../components/ui/ButtonLink";
import Section from "../components/ui/Section";
import backgroundImageUrl from "../static/images/header.png";
import Layout from "../components/ui/Layout";

export default () => {
  return (
    <Layout>
      <Header
        backgroundImageUrl={backgroundImageUrl}
        title={meta.header.title}
        subtitle={meta.header.subtitle}
        callToActionText={meta.header.callToAction.text}
        callToActionLink={meta.header.callToAction.link}
      />
      <Section type="primary">Hello section !</Section>
    </Layout>
  );
};
