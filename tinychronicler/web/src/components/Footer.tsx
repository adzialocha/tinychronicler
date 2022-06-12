type Props = {
  version: string;
};

const Footer = ({ version }: Props) => {
  return <footer>{`v${version}`}</footer>;
};

export default Footer;
