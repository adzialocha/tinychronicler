import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header>
      <h1>Tiny Chronicler</h1>
      <nav>
        <ul>
          <li>
            <Link to="/">Dashboard</Link>
          </li>
          <li>
            <Link to="/chronicles">Chronicles</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
