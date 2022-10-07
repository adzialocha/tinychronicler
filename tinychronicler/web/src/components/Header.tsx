import { AppBar, Toolbar } from 'react95';
import styled from 'styled-components';

import Link from '~/components/Link';

type Props = {
  version: string;
};

const Title = styled.h1`
  font-size: 1.3rem;
  font-weight: bold;
  font-style: italic;
  color: rgb(132, 133, 132);
  text-shadow: white 2px 2px;
  padding-left: 10px;
`;

const Version = styled.span`
  font-size: 1rem;
  font-style: italic;
  color: rgb(132, 133, 132);
  text-shadow: white 1px 1px;
  padding-right: 5px;
`;

const Emoji = styled.span`
  font-style: initial;
  text-shadow: none;
`;

const Header = ({ version }: Props) => {
  return (
    <AppBar>
      <Toolbar style={{ justifyContent: 'space-between' }}>
        <div style={{ position: 'relative', display: 'inline-block' }}>
          <Link to="/">Start</Link>
          <Link to="/chronicles">Chronicles</Link>
          <Link to="/settings">Settings</Link>
        </div>
        <Title>
          <Emoji>💌</Emoji> Tiny Chronicler <Version>v{version}</Version>
        </Title>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
